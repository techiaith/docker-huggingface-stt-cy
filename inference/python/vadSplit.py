import collections
import contextlib
import wave

AudioFormat = collections.namedtuple('AudioFormat', 'rate channels width')

DEFAULT_RATE = 16000
DEFAULT_CHANNELS = 1
DEFAULT_WIDTH = 2
DEFAULT_FORMAT = AudioFormat(DEFAULT_RATE, DEFAULT_CHANNELS, DEFAULT_WIDTH)


class AudioFile:

    def __init__(self, audio_path, as_path=False, audio_format=DEFAULT_FORMAT):
        self.audio_path = audio_path
        self.audio_format = audio_format
        self.as_path = as_path
        self.open_file = None
        self.tmp_file_path = None

    def __enter__(self):
        if self.audio_path.endswith('.wav'):
            self.open_file = wave.open(self.audio_path, 'r')
            if read_audio_format_from_wav_file(self.open_file) == self.audio_format:
                if self.as_path:
                    self.open_file.close()
                    return self.audio_path
                return self.open_file
            self.open_file.close()

    def __exit__(self, *args):
        if not self.as_path:
            self.open_file.close()
        if self.tmp_file_path is not None:
            os.remove(self.tmp_file_path)


def read_audio_format_from_wav_file(wav_file):
    return AudioFormat(wav_file.getframerate(), wav_file.getnchannels(), wav_file.getsampwidth())


def get_num_samples(pcm_buffer_size, audio_format=DEFAULT_FORMAT):
    return pcm_buffer_size // (audio_format.channels * audio_format.width)


def get_pcm_duration(pcm_buffer_size, audio_format=DEFAULT_FORMAT):
    """Calculates duration in seconds of a binary PCM buffer (typically read from a WAV file)"""
    return get_num_samples(pcm_buffer_size, audio_format) / audio_format.rate


def read_frames(wav_file, frame_duration_ms=30, yield_remainder=False):
    audio_format = read_audio_format_from_wav_file(wav_file)
    frame_size = int(audio_format.rate * (frame_duration_ms / 1000.0))
    while True:
        try:
            data = wav_file.readframes(frame_size)
            if not yield_remainder and get_pcm_duration(len(data), audio_format) * 1000 < frame_duration_ms:
                break
            yield data
        except EOFError:
            break


def read_frames_from_file(audio_path, audio_format=DEFAULT_FORMAT, frame_duration_ms=30, yield_remainder=False):
    with AudioFile(audio_path, audio_format=audio_format) as wav_file:
        for frame in read_frames(wav_file, frame_duration_ms=frame_duration_ms, yield_remainder=yield_remainder):
            yield frame


def split(audio_frames,
          audio_format=DEFAULT_FORMAT,
          num_padding_frames=10,
          threshold=0.5,
          aggressiveness=3):

    from webrtcvad import Vad  # pylint: disable=import-outside-toplevel

    if audio_format.channels != 1:
        raise ValueError('VAD-splitting requires mono samples')

    if audio_format.width != 2:
        raise ValueError('VAD-splitting requires 16 bit samples')

    if audio_format.rate not in [8000, 16000, 32000, 48000]:
        raise ValueError(
            'VAD-splitting only supported for sample rates 8000, 16000, 32000, or 48000')

    if aggressiveness not in [0, 1, 2, 3]:
        raise ValueError(
            'VAD-splitting aggressiveness mode has to be one of 0, 1, 2, or 3')

    ring_buffer = collections.deque(maxlen=num_padding_frames)
    triggered = False
    vad = Vad(int(aggressiveness))
    voiced_frames = []
    frame_duration_ms = 0
    frame_index = 0
    for frame_index, frame in enumerate(audio_frames):
        frame_duration_ms = get_pcm_duration(len(frame), audio_format) * 1000
        if int(frame_duration_ms) not in [10, 20, 30]:
            raise ValueError(
                'VAD-splitting only supported for frame durations 10, 20, or 30 ms')
        is_speech = vad.is_speech(frame, audio_format.rate)
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > threshold * ring_buffer.maxlen:
                triggered = True
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > threshold * ring_buffer.maxlen:
                triggered = False
                yield b''.join(voiced_frames), \
                      frame_duration_ms * max(0, frame_index - len(voiced_frames)), \
                      frame_duration_ms * frame_index
                ring_buffer.clear()
                voiced_frames = []
    if len(voiced_frames) > 0:
        yield b''.join(voiced_frames), \
              frame_duration_ms * (frame_index - len(voiced_frames)), \
              frame_duration_ms * (frame_index + 1)

