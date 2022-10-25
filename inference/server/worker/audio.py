import os
import pydub
import shlex
import subprocess
import fleep

from pathlib import Path

def prepare_audio(audio_file_path):
    print("Task prepare_audio for %s started" % audio_file_path)
    audio_file = Path(audio_file_path)

    with open(audio_file_path, 'rb') as audio_file:
        info = fleep.get(audio_file.read(128))
        if len(info.extension) > 0 and info.extension[0] == "wav": 
            wav_file_path=audio_file_path
        else:
            wav_file_path=convert_audio(audio_file_path)

    #
    wav_normalized_audio_file_path = normalize_audio(wav_file_path)
    print ("Completed prepared audio file : %s" % wav_normalized_audio_file_path)
    return wav_normalized_audio_file_path

def convert_audio(audio_file_path):
    print ("Converting to wav")
    wav_file_path = Path(audio_file_path).with_suffix(".wav")
    convert_cmd = "ffmpeg -i {} -vn -acodec pcm_s16le -ar 16000 -ac 1 {}".format(audio_file_path, wav_file_path)
    subprocess.Popen(shlex.split(convert_cmd)).wait()
    Path(audio_file_path).unlink()
    return wav_file_path.as_posix()

def normalize_audio(wav_file_path):
    print ("Normalizing loudness")
    
    wav_file_path = Path(wav_file_path)
    wav_normalized_file_path = Path(wav_file_path).with_suffix(".n.wav")
    
    normalize_cmd = "ffmpeg-normalize {} -ar 16000 -o {}".format(wav_file_path, wav_normalized_file_path)
    subprocess.Popen(shlex.split(normalize_cmd)).wait()
    
    wav_file_path.unlink()
    wav_file_path = wav_normalized_file_path.rename(wav_file_path.with_suffix(".wav").as_posix())
    
    return wav_file_path.as_posix()

