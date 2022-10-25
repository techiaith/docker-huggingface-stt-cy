import os
import srt
import json

from datetime import timedelta

def to_srt_from_jsonstring(transcriptions, srt_file_path=''):
    i = 0

    srt_segments = []
    json_segments = json.loads(transcriptions)

    for transcript in json_segments["transcript"]:
        i = i+1
        time_start = transcript["start"]
        time_end = transcript["end"]
        text = transcript["text"] 
        start_delta = timedelta(seconds=time_start)
        end_delta = timedelta(seconds=time_end)
        srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content=text))

    srt_string = srt.compose(srt_segments)
    if len(srt_file_path) > 0:
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_string)
        print("srt file of transcription saved to %s" % srt_file_path)

    return srt_string

