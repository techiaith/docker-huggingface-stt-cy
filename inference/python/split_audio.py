import os
import srt
import pandas
import time
#import hashlib
import uuid

from pathlib import Path
from pydub import AudioSegment

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""


def split_from_srt(wav_file_path, srt_file_path, destination_dir, csv_file_path, **kwargs):
    # produce audio clips of each 'segment' in srt file and an accompanying txt file
    # that contains the transcription
    # build also a csv file in a format compatible with Common Voice (/DeepSpeech/coqui)
    #    
    Path(destination_dir).mkdir(parents=True, exist_ok=True)
    Path(csv_file_path).parent.mkdir(parents=True, exist_ok=True)
    
    wav_filename = Path(wav_file_path).name

    df = pandas.DataFrame(columns=['wav_filename', 'wav_filesize', 'transcript', 'duration', 'parent_wavfile_name'])
    
    wav_audio_file = AudioSegment.from_wav(wav_file_path)
    srt_segments = list(srt.parse(open(srt_file_path, 'r', encoding='utf-8').read()))
    
    i=0
    for s in srt_segments:

        transcript = s.content.lower()

        # pydub does things in milliseconds
        start = float(s.start.total_seconds()) * 1000
        end = float(s.end.total_seconds()) * 1000
        
        wav_segment = wav_audio_file[start:end]

        wav_segment_file_name = uuid.uuid4().hex + ".wav"
        wav_segment_file_path = os.path.join(destination_dir, wav_segment_file_name)
        wav_segment.export(wav_segment_file_path, format="wav")

        #txt_segment_file_path = wav_segment_file_path.replace(".wav", ".txt")
        #with open(txt_segment_file_path, 'w', encoding='utf-8') as txt_segment_file:
        #    txt_segment_file.write(transcript)

        duration = end - start;
        df.loc[i] = [wav_segment_file_name, os.path.getsize(wav_segment_file_path), transcript, duration, wav_filename]
        i+=1
        
    print ("Adding segments to csv file {}".format(csv_file_path))
    with open(csv_file_path, 'a') as csvfile:
        df.to_csv(csvfile, encoding='utf-8', mode='a', index=False, header=csvfile.tell()==0, sep="\t")


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--wavfile", dest="wav_file_path", required=True)
    parser.add_argument("--srtfile", dest="srt_file_path", required=True)
    parser.add_argument("--destdir", dest="destination_dir", required=True)
    parser.add_argument("--csvfile", dest="csv_file_path", required=True)

    parser.set_defaults(func=split_from_srt)
    args = parser.parse_args()
    args.func(**vars(args))
