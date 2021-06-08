# Welsh language wav2vec2 Speech Recognition Server

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

## Background

If you would like to install and use a wav2vec2 speech recognition engine locally
on your own computer, instead of using the API service at https://api.techiaith.org/en/
then the resources in this folder can help you. 

**N.B.** - wav2vec2 models are quite large, therefore you will need plenty of memory
in your computer. If you don't have enough memory, but would still like to run locally
your own Welsh speech recognition engine, then smaller models based on Mozilla
DeepSpeech are available - https://github.com/techiaith/docker-deepspeech-cy-server

## Install

```
$ git clone https://github.com/techiaith/docker-wav2vec2-xlsr-ft-cy
$ cd docker-wav2vec2-xlsr-ft-cy/server
$ make
```

The build process fetches models that have been pretrained by Bangor University's Language Technologies Unit.

## Use

Runing the models within an APII redeg, requires only one additional command:

```
$ make run
```

To verify that your API is up and running, you can make a simple text with a sample wav file provided within the folder:
``` 
$ curl -F 'soundfile=@speech.wav' localhost:5511/speech_to_text/
{"success": true, "version": 1, "text": "mae ganddynt ddau o blant mab a merch"}
```

You can transcribe your own recordings as long as files are in wav format and 16kHz mono channel.  

Also, go to http://localhost:5511/static_html/index.hml in order to use your speech recognition
installation with sound files or microphone within a webpage.

## Warning

Please note that transcription results will not always be totally correct. We have 
measured the error rate to be 15%, which is higher than error rates for English and other 
larger languages that have error rates below 8%.

The work on measuring and improving the models' capabilities is ongoing work. 

In the meantime, if you would like to see the models improve, then record some Welsh
sentences on the Mozilla Common Voice (https://voice.mozilla.org/cy) website, so that
we will have more training data. Or use our voice assistant app - Macsen (http://techiaith.cymru/macsen)
