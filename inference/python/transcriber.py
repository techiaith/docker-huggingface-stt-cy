#!/bin/env python
import glob
import srt
from praatio import tgio
from datetime import timedelta

import models

from speech_to_text import SpeechToText

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""

WORDS_PER_SEGMENT=14
SECONDS_PER_SEGMENT=8


class Transcriber:

    def __init__(self):
        pass        



    def to_srt_file(self, transcriptions, srt_file_path):
        i = 0
        srt_segments = []            
        for transcript, time_start, time_end, alignments in transcriptions:           
            i = i+1            
            start_delta = timedelta(seconds=time_start)
            end_delta = timedelta(seconds=time_end)
            srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content=transcript))

        str_string = srt.compose(srt_segments)
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(str_string)

        print("srt file of transcription saved to %s" % srt_file_path)



    def to_textgrid_file(self, transcriptions, wav_file_path, textgrid_file_path):
        textgrid_entries_list = []
        for transcript, time_start, time_end, alignments in transcriptions:                        
            textgrid_entry = (time_start, time_end, transcript)
            textgrid_entries_list.append(textgrid_entry)

        utterance_tier = tgio.IntervalTier('utterance', textgrid_entries_list, 0, pairedWav=wav_file_path)
        tg = tgio.Textgrid()
        tg.addTier(utterance_tier)
        tg.save(textgrid_file_path, useShortForm=False, outputFormat='textgrid')

        print("Textgrid of transcription saved to %s" % textgrid_file_path)



def main(wav_file, **args):        
    stt=SpeechToText()
    t=Transcriber()
    transcriptions = list()
    for transcript, time_start, time_end, alignments in stt.transcribe(wav_file):
        transcriptions.append((transcript, time_start, time_end, alignments))

    t.to_srt_file(transcriptions, wav_file.replace(".wav", ".srt"))
    t.to_textgrid_file(transcriptions, wav_file, wav_file.replace(".wav", ".TextGrid"))


#
if __name__ == "__main__":    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)    
    parser.add_argument("-w", dest="wav_file", required=True)
    parser.add_argument("-s", dest="output_srt_file")
    parser.add_argument("-x", dest="output_textgrid_file")
    parser.add_argument("-r", dest="reference_file")
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
