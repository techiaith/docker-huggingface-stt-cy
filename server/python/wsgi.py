#!/usr/bin/env python3
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

        self.model_domain=os.environ["MODEL_DOMAIN"]        
        self.model_version=os.environ["MODEL_VERSION"]

        self.acoustic_model = models.download(os.environ["WAV2VEC2_MODEL_NAME"])
        self.language_model = models.download(os.environ["KENLM_MODEL_NAME"])

        cherrypy.log("Loading wav2vec2 model....")
        cherrypy.log("   acoustic_model_path={}".format(self.acoustic_model))
        cherrypy.log("   language_model_path={}".format(self.language_model))

        self.stt=SpeechToText(acoustic_model_path=self.acoustic_model, language_model_path=self.language_model)        
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
            'model_name': self.acoustic_model,
            'language_model_name': self.language_model,
            'model_domain': self.model_domain,
            'model_version': self.model_version 
        }
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def speech_to_text(self, soundfile, **kwargs):
        upload_tmp_filepath = os.path.join(self.tmp_dir, 'ds_request_' + datetime.now().strftime('%y-%m-%d_%H%M%S') + '.wav')
        with open(upload_tmp_filepath, 'wb') as wavfile:
            while True:
                data = soundfile.file.read(8192)
                if not data:
                    break
                wavfile.write(data)

        #cherrypy.log("tmp file written to %s" % upload_tmp_filepath)

        result = {
                'version':1
        }

        #
        success = True
        text = ''

        fin = wave.open(upload_tmp_filepath, 'rb')
        fs = fin.getframerate()
        if fs != 16000:
            success = False            
        fin.close()

        if success:
            #cherrypy.log("Starting STT ....")

            try:
                for transcript, time_start, time_end in self.stt.transcribe(upload_tmp_filepath):
                    text = text + " " + transcript
            except Exception as e:
                cherrypy.log("STT not a success")
                cherrypy.log(e)
                success=False
            #else:
                #cherrypy.log("STT successful")


        result.update({
            'success': success,
            'text': text
        })

        Path(upload_tmp_filepath).unlink()

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

