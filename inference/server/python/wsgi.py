import os
import sys
import glob
import wave
import cherrypy
import numpy as np

import models

from packaging import version
from datetime import datetime
from pathlib import Path

from speech_to_text import SpeechToText

STATIC_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static_html')

class StaticRoot(object): pass

class SpeechToTextAPI(object):


    def __init__(self):
        self.tmp_dir = '/recordings'
        self.stt=SpeechToText()        

        cherrypy.log("Loading wav2vec2 and KenLM models completed")


    @cherrypy.expose
    def index(self):
        msg = "<h1>wav2vec2 xlsr-ft-cy Server</h1>\n"
        return msg 


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self):
        result = {
            'version': 1,
            'model_name': self.stt.get_model_name(),
            'language_model_name': self.stt.get_language_model(),
            'model_version': self.stt.get_model_version(),
            'device': self.stt.get_device()
        }
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def speech_to_text(self, soundfile, max_segment_length=5, max_segment_words=14, **kwargs):
        upload_tmp_filepath = os.path.join(self.tmp_dir, 'ds_request_' + datetime.now().strftime('%y-%m-%d_%H%M%S') + '.wav')
        with open(upload_tmp_filepath, 'wb') as wavfile:
            while True:
                data = soundfile.file.read(8192)
                if not data:
                    break
                wavfile.write(data)

        cherrypy.log("tmp file written to %s" % upload_tmp_filepath)

        result = {
            'version':1
        }

        #
        success = True
        transcripts=list() 

        fin = wave.open(upload_tmp_filepath, 'rb')
        fs = fin.getframerate()
        if fs != 16000:
            success = False
        fin.close()

        if success:
            cherrypy.log("Transcribing %s" % upload_tmp_filepath)

            try:
                for transcript, time_start, time_end, alignment in self.stt.transcribe(upload_tmp_filepath, max_segment_length=max_segment_length, max_segment_words=max_segment_words):
                    transcripts.append({'text': transcript, 'start':time_start, 'end':time_end, 'alignment':alignment})
            except Exception as e:
                cherrypy.log("Error during transcribing %s" % upload_tmp_filepath)
                cherrypy.log(e)
                success=False
            else:
                cherrypy.log("Transcribing %s succesful." % upload_tmp_filepath)


        result.update({
            'success': success,
            'transcripts': transcripts 
        })

        cherrypy.log(str(result))

        #Path(upload_tmp_filepath).unlink()

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

