import os
import csv
import srt
import json

from pathlib import Path
from datetime import timedelta


def save_as_json(audio_file_path, transcription):
    json_str = json.dumps(transcription)
    json_file_path = Path(audio_file_path).with_suffix(".json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
    return json_file_path
 
 
def save_as_srt(audio_file_path, transcription):
    i = 0

    srt_segments = []
    srt_file_path = Path(audio_file_path).with_suffix(".srt")
    
    for transcript in transcription:
        i = i+1
        time_start = transcript["start"]
        time_end = transcript["end"]
        text = transcript["text"]
        start_delta = timedelta(seconds=time_start)
        end_delta = timedelta(seconds=time_end)
        srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content=text))

    srt_string = srt.compose(srt_segments)
    with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_string)
    
    print("srt file of transcription saved to %s" % srt_file_path)

    return srt_file_path


def save_as_csv(audio_file_path, transcription):
    i=0
    rows = []
    header = ["ID", "Start", "End", "Transcript"]

    for transcript in transcription:
        i = i+1

        time_start = transcript["start"]
        time_end = transcript["end"]
        text = transcript["text"]

        rows.append({'ID': i, 'Start': time_start, 'End': time_end, 'Transcript': text})

    csv_file_path = Path(audio_file_path).with_suffix(".csv")
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, delimiter='\t', fieldnames=header, quoting=csv.QUOTE_NONE)
        csv_writer.writeheader()
        csv_writer.writerows(rows)
