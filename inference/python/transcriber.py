#!/bin/env python
import glob
import srt
from praatio import tgio
from datetime import timedelta

import models

from speech_to_text import SpeechToText

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

(c) Prifysgol Bangor University

"""

WORDS_PER_SEGMENT=14
SECONDS_PER_SEGMENT=8


class Transcriber:

    def __init__(self):
        pass        


    def to_srt_file(self, transcriptions, srt_file_path, split_only):
        i = 0
        srt_segments = []            
        for transcript, time_start, time_end, alignments in transcriptions:           
            i = i+1            
            start_delta = timedelta(seconds=time_start)
            end_delta = timedelta(seconds=time_end)
            if split_only==True:
                srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content="..."))
            else:
                srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content=transcript))
        
        str_string = srt.compose(srt_segments)
        if len(srt_file_path) > 0:
            with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(str_string)
            print("srt file of transcription saved to %s" % srt_file_path)
        else:
            print (str_string)


   

    def to_textgrid_file(self, transcriptions, wav_file_path, textgrid_file_path):
        textgrid_entries_list = []
        for transcript, time_start, time_end, alignments in transcriptions:                        
            textgrid_entry = (time_start, time_end, transcript)
            textgrid_entries_list.append(textgrid_entry)

        utterance_tier = tgio.IntervalTier('utterance', textgrid_entries_list, 0, pairedWav=wav_file_path)
        tg = tgio.Textgrid()
        tg.addTier(utterance_tier)
        if len(textgrid_file_path) > 0:
            tg.save(textgrid_file_path, useShortForm=False, outputFormat='textgrid')
            print("Textgrid of transcription saved to %s" % textgrid_file_path)
        else:
            print (utterance_tier)

    

def main(wav_file, output_srt_file, with_lm, split_only, **args):

    output_textgrid_file=output_srt_file.replace(".srt", ".TextGrid")

    stt=SpeechToText(split_only=split_only)
    t=Transcriber()

    #
    i = 0
    transcriptions = list()
    for transcript, time_start, time_end, alignments in stt.transcribe(wav_file, withlm=with_lm):
        i += 1
        print (i, time_start, time_end, transcript)
        transcriptions.append((transcript, time_start, time_end, alignments))

    t.to_srt_file(transcriptions, output_srt_file, split_only)       
    t.to_textgrid_file(transcriptions, wav_file, output_textgrid_file)

    
#
if __name__ == "__main__":    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("-w", dest="wav_file", required=True)
    parser.add_argument("-s", dest="output_srt_file", default='')
    parser.add_argument("-l", dest="with_lm", action='store_true')
    parser.add_argument("--split_only", dest="split_only", action='store_true')

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
