import os
import time
import json

import punctuation_client

from pathlib import Path
from celery import Celery

from audio import prepare_audio
from persist import save_as_json, save_as_srt, save_as_csv

from speech_to_text_task import SpeechToTextTask

# Wait for rabbitmq to be started
time.sleep(15)

#
app = Celery(
    'postman',
    broker='pyamqp://user:bitnami@rabbitmq',
    backend='redis://redis:6379/0',
)


@app.task(name='speech_to_text',
          ignore_result=False,
          bind=True,
          base=SpeechToTextTask,
          serializer='json')
def speech_to_text(self, audio_file_path, max_segment_length, max_segment_words):
    print("Task speech_to_text for %s started" % audio_file_path)
    audio_file_path = prepare_audio(audio_file_path)
  
    print ("Using model :", self.model.get_model_name(), self.model.get_model_version())

    success = True 
    transcripts = []
    try:
        for transcript, time_start, time_end, alignment in self.model.transcribe(audio_file_path, max_segment_length, max_segment_words):
            print ("{}-{} {}".format(time_start, time_end, transcript))
 
            transcript = punctuation_client.restore_punctuation_and_truecase(transcript)
            transcripts.append({'text': transcript, 'start':time_start, 'end':time_end, 'alignment':alignment})

    except Exception as e:
        print("Error during transcribing %s" % audio_file_path)
        print(e)
        success=False
    else:
        print("Transcribing %s succesful." % audio_file_path)
 
    save_as_json(audio_file_path, transcripts)
    save_as_srt(audio_file_path, transcripts)
    save_as_csv(audio_file_path, transcripts)
    
    return transcripts


