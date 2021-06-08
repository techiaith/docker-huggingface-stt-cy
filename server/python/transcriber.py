#!/bin/env python3
import glob
import webrtcvad
import srt
from praatio import tgio

from datetime import timedelta

import numpy as np
import torch

from vadSplit import read_frames_from_file, split
from speech_to_text import SpeechToText
from translator import Translator

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""


class Transcriber:

    def __init__(self):
        pass        


    def to_srt_subtitles(self, transcriptions, translator):
        i = 0
        for transcript, time_start, time_end in transcriptions:
            if len(transcript.strip()) == 0:
                continue
            i = i+1
            start_seconds = time_start / 1000
            end_seconds = time_end / 1000
            start_delta = timedelta(seconds=start_seconds)
            end_delta = timedelta(seconds=end_seconds)
            yield i, start_delta, end_delta, transcript, translator.translate(transcript)

    
    def write_to_srt(self, subtitles, srt_file_path):
        srt_segments = []
        for i, s, e, t, m in subtitles:
            print (i, s, e, t, '|', m)
            srt_segments.append(srt.Subtitle(i, start=s, end=e, content=t+'\n'+m))

        str_string = srt.compose(srt_segments)
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(str_string)

        print("srt file of transcription saved to %s" % srt_file_path)


    def write_to_textgrid(self, transcriptions, wav_file_path, textgrid_file_path):
        textgrid_entries_list = []
        for transcript, time_start, time_end in transcriptions:
            print (transcript)
            if len(transcript.strip()) == 0:
                continue
            start_seconds = time_start / 1000
            end_seconds = time_end / 1000
            textgrid_entry = (start_seconds, end_seconds, transcript)
            textgrid_entries_list.append(textgrid_entry)

        utterance_tier = tgio.IntervalTier('utterance', textgrid_entries_list, 0, pairedWav=wav_file_path)
        tg = tgio.Textgrid()
        tg.addTier(utterance_tier)
        tg.save(textgrid_file_path, useShortForm=False, outputFormat='textgrid')

        print("Textgrid of transcription saved to %s" % textgrid_file_path)


def main(wav_file, aggresiveness, **args):
    t=Transcriber()
    stt=SpeechToText()
    mt=Translator(engine='bangor', source_lang='cy', target_lang='en')
    t.write_to_srt(t.to_srt_subtitles(stt.transcribe(wav_file, aggresiveness), mt), wav_file.replace(".wav", ".srt"))


#
if __name__ == "__main__":    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)    
    parser.add_argument("-w", dest="wav_file", required=True)        
    parser.add_argument("-a", dest="aggresiveness", type=int, default=2)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

