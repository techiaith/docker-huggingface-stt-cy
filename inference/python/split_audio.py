import os
import srt
import pandas
import time
import hashlib

from pathlib import Path
from pydub import AudioSegment

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""

def hash_wavfile_content(wav_file_path):
    hash_result=hashlib.sha256()
    with open(wav_file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_result.update(byte_block)
    return hash_result.hexdigest()

def split_from_srt(wav_file_path, srt_file_path, destination_dir, **kwargs):
    # produce audio clips of each 'segmwnt' in srt file and an accompanying txt file
    # that contains the transcription
    # build also a csv file in a format compatible with Common Voce (/DeepSpeech/coqui)
    #
    destination_clips_dir = os.path.join(destination_dir, "clips")
    Path(destination_clips_dir).mkdir(parents=True, exist_ok=True)
    
    wav_filename = Path(wav_file_path).name

    df = pandas.DataFrame(columns=['wav_filename', 'wav_filesize', 'transcript', 'parent_wavfile_name'])
    
    wav_audio_file = AudioSegment.from_wav(wav_file_path)
    srt_segments = list(srt.parse(open(srt_file_path, 'r', encoding='utf-8').read()))

    wav_content_hash = hash_wavfile_content(wav_file_path)

    i=0
    for s in srt_segments:
        transcript = s.content.lower()

        # pydub does things in milliseconds
        start = float(s.start.total_seconds()) * 1000
        end = float(s.end.total_seconds()) * 1000
        
        wav_segment = wav_audio_file[start:end]

        # use transcript and time as vectors for ensuring a unique wav filename
        #hashId = hashlib.md5((transcript + str(time.time())).encode('utf-8')).hexdigest()
        hashId = hashlib.md5((wav_content_hash + str(i)).encode('utf-8')).hexdigest()
        
        wav_segment_file_name = hashId + ".wav"
        wav_segment_file_path = os.path.join(destination_clips_dir, wav_segment_file_name)
        wav_segment.export(wav_segment_file_path, format="wav")

        txt_segment_file_path = wav_segment_file_path.replace(".wav", ".txt")
        with open(txt_segment_file_path, 'w', encoding='utf-8') as txt_segment_file:
            txt_segment_file.write(transcript)

        df.loc[i] = [wav_segment_file_name, os.path.getsize(wav_segment_file_path), transcript, wav_filename]
        i+=1
    
    with open(os.path.join(destination_dir, "clips", "clips.csv"), 'a') as csvfile:
        df.to_csv(csvfile, encoding='utf-8', mode='a', index=False, header=csvfile.tell()==0)


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--wavfile", dest="wav_file_path", required=True)
    parser.add_argument("--srtfile", dest="srt_file_path", required=True)
    parser.add_argument("--destdir", dest="destination_dir", required=True)

    parser.set_defaults(func=split_from_srt)
    args = parser.parse_args()
    args.func(**vars(args))
