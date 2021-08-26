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
$ cd docker-wav2vec2-xlsr-ft-cy/inference/server
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
{"version": 1, "success": true, "text": " mae ganddynt ddau o blant mab a merch ", "alignment": [["m", 0.6003829787234042], ["a", 0.640468085106383], ["e", 0.7005957446808511], [" ", 0.7607234042553191], ["g", 0.8208510638297872], ["a", 0.8809787234042553], ["n", 0.9811914893617021], ["d", 1.0413191489361702], ["d", 1.1214893617021275], ["y", 1.1816170212765957], ["n", 1.2818297872340427], ["t", 1.3820425531914893], [" ", 1.4421702127659572], ["d", 1.6025106382978722], ["d", 1.6626382978723404], ["a", 1.7428085106382978], ["u", 1.923191489361702], [" ", 2.0634893617021275], ["o", 2.1236170212765955], [" ", 2.183744680851064], ["b", 2.2438723404255314], ["l", 2.304], ["a", 2.3440851063829786], ["n", 2.5044255319148934], ["t", 2.6647659574468086], [" ", 2.7449361702127657], ["m", 3.165829787234043], ["a", 3.266042553191489], ["b", 3.5466382978723403], [" ", 3.6067659574468083], ["a", 3.9474893617021274], [" ", 4.188], ["m", 4.248127659574467], ["e", 4.348340425531915], ["r", 4.448553191489362], ["c", 4.568808510638298], ["h", 4.588851063829787], [" ", 5.10995744680851]]}
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
