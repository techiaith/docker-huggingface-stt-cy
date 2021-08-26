import os
from speech_to_text import SpeechToText

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""

#
def main(audio_file, **args):
    stt=SpeechToText()      
    for transcript, time_start, time_end, alignments in stt.transcribe(audio_file):
        print (transcript, time_start, time_end, alignments)
        

if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--wav", dest="audio_file", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
