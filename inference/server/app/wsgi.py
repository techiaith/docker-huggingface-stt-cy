import os
import sys
import uuid
import time
import glob
import json
import cherrypy
import tempfile

from celery import Celery
from celery.result import AsyncResult
from pydub import AudioSegment

from datetime import datetime
from pathlib import Path
from utils_srt import to_srt_from_jsonstring


# wait for rabbitmq to startup
time.sleep(20)

STATIC_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static_html')

class StaticRoot(object): pass

class SpeechToTextAPI(object):


    def __init__(self):
        self.tmp_dir = '/recordings'
        self.tasks = dict()
        self.celery = Celery('postman', 
                             broker='pyamqp://user:bitnami@rabbitmq', 
                             backend='redis://redis:6379/0')


    @cherrypy.expose
    def index(self):
        cherrypy.log("Request index page")
        msg = "<h1>wav2vec2 xlsr-ft-cy Server</h1>\n"
        return msg 


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self):
        cherrypy.log("Request versions page")
        result = {
            'version': 1,
        }
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_status(self, stt_id, **kwargs):
        cherrypy.log("Request status")
        if stt_id in self.tasks:
            task_result = AsyncResult(self.tasks[stt_id])
            task_status = task_result.status
        else:
            task_status = 'UNKNOWN'
            
        #
        result = {
            'version': 1,
            'status': task_status
        }

        return result
        

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_json(self, stt_id, **kwargs):
        cherrypy.log("Request json file")
        jsonobj = ''

        json_file_path = Path(os.path.join(self.tmp_dir, stt_id + ".json"))
        if json_file_path.is_file():
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                jsonobj = json.load(json_file)
        
        return jsonobj
        
        
    @cherrypy.expose
    def get_srt(self, stt_id, **kwargs):
        cherrypy.log("Request srt file")
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        srt = ''

        srt_file_path = Path(os.path.join(self.tmp_dir, stt_id + ".srt"))
        if srt_file_path.is_file():
            with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
                srt = srt_file.read()
        
        return srt
 

    @cherrypy.expose
    def get_csv(self, stt_id, **kwargs):
        cherrypy.log("Request csv file")
        cherrypy.response.headers['Content-Type'] = 'text/csv'
        csv = ''

        csv_file_path = Path(os.path.join(self.tmp_dir, stt_id + ".csv"))
        if csv_file_path.is_file():
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv = csv_file.read()
        
        return csv


    @cherrypy.expose
    def get_audio(self, stt_id, start=0, end=0, **kwargs):
        cherrypy.log("Request audio for stt_id %s" % stt_id)
        cherrypy.response.headers["Content-Type"] = "audio/wav"
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="%s_%s_%s.wav"' % (stt_id, start, end)
        
        start_ts = float(start)
        end_ts = float(end)
        
        wav_segment = None
        audio_file_path = os.path.join(self.tmp_dir, stt_id + ".wav")
        wav_audio_file = AudioSegment.from_file(audio_file_path, "wav")
        if start_ts==0.0 and end_ts==0.0:
            wav_segment = wav_audio_file
        else:
            # pydub does things in milliseconds
            wav_segment = wav_audio_file[start_ts * 1000:end_ts * 1000]
        
        audio_bytes = None
        
        with tempfile.TemporaryFile() as temp_file:
            wav_segment.export(out_f=temp_file, format="wav")
            temp_file.seek(0)
            audio_bytes = temp_file.read()    	
        
        return audio_bytes
               
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def speech_to_text(self, soundfile, max_segment_length=5, max_segment_words=14, **kwargs):
        success = True
        stt_id = str(uuid.uuid4())
         
        audio_file_path = os.path.join(self.tmp_dir, stt_id)
        with open(audio_file_path, 'wb') as audiofile:
            while True:
                data = soundfile.file.read(8192)
                if not data:
                    break
                audiofile.write(data)

        #
        cherrypy.log("tmp file written to %s" % audio_file_path)

        #
        cherrypy.log("sent task stt for %s" % audio_file_path)
        transcription_task = self.celery.send_task('speech_to_text', args=(audio_file_path, max_segment_length, max_segment_words))
        self.tasks.setdefault(stt_id, transcription_task.task_id)
 
        #
        result = {
            'version':1,
            'success':success,
            'id':stt_id,
        }

        return result


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.access_file': '/var/log/wav2vec2/access.log',
    'log.error_file': '/var/log/wav2vec2/error.log',
})


cherrypy.tree.mount(StaticRoot(), '/static', config={
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': STATIC_PATH,
        'tools.staticdir.index': 'index.html',
         },
    })


cherrypy.tree.mount(SpeechToTextAPI(), '/')
application = cherrypy.tree

