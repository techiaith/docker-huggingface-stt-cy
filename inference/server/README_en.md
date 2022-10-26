# Welsh language wav2vec2 Speech Recognition Server

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

## Background

If are concerned about the privacy of any online Welsh speech recognition API, such as by techiaith at https://api.techiaith.org/en, then the contents of this folder can help you install and use your own local installation. 


## Install

```
$ git clone https://github.com/techiaith/docker-wav2vec2-cy
$ cd docker-wav2vec2-cy/inference/server
$ make
```

The build process fetches models that have been pretrained by Bangor University's Language Technologies Unit.

## Use

Runing the models within an API, requires only one additional command:

```
$ make up
```

To verify that your API is up and running, you can make a simple text with a sample wav file provided within the folder: 

``` 
$ curl -F 'soundfile=@speech.wav' localhost:5511/speech_to_text/
{"version": 1, "success": true, "id": "e1684eab-e472-4aaa-8c4f-66c007477a7f"}
```

(you can transcribe your own recordings as long as files are in wav format and 16kHz mono channel.)

You will receive a response that is effectively only an acknowledgement of your request containing an id. Since it can take some time to perform speech to text on a file, you can check on the status with subsequent ping requests. If the audio's duration is longer than 5-10 seconds, the API will segment using voice detection. 

```
$ curl localhost:5511/get_status/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
{"version": 1, "status": "PENDING"}
```

when transcription is complete, the response will be

```
$ curl localhost:5511/get_status/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
{"version": 1, "status": "SUCCESS"}
````

The results can be obtained in srt format:

```
$ curl localhost:5511/get_srt/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
1
00:00:00,619 --> 00:00:05,170
mae ganddynt ddau o blant mab a merch
```

json:  (which contain alignments at word level)

```
$ curl localhost:5511/get_json/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
[{"text": "mae ganddynt ddau o blant mab a merch", "start": 0.619581589958159, "end": 5.170041841004185, "alignment": [{"word": "mae", "start": 0.619581589958159, "end": 0.7992050209205022}, {"word": "ganddynt", "start": 0.8391213389121339, "end": 1.457824267782427}, {"word": "ddau", "start": 1.6973221757322177, "end": 2.096485355648536}, {"word": "o", "start": 2.1563598326359834, "end": 2.1962761506276154}, {"word": "blant", "start": 2.256150627615063, "end": 2.7950209205020924}, {"word": "mab", "start": 3.1742259414225944, "end": 3.6133054393305444}, {"word": "a", "start": 3.9725523012552304, "end": 4.17213389121339}, {"word": "merch", "start": 4.251966527196653, "end": 5.170041841004185}]}]
```

or csv:

```
$ curl localhost:5511/get_csv/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
ID      Start   End     Transcript
1       0.619581589958159       5.170041841004185       mae ganddynt ddau o blant mab a merch
```


The server provides a very simple HTML GUI in order to use/support the above API. Go to http://localhost:5511/static_html/index.hml

## Restore capitalization and punctuation

Results from the speech recognition model are always in lowercase letters and do not contain any type of punctuation marks such question marks, full stops, colons etc. such as in the example transcription result above - "mae ganddynt dau o blant mab a merch". Therefore, it's now possible to connect the transcription server with a punctuation server that you may have installed from our other project on GitHub - see https://github.com/techiaith/docker-atalnodi-server. 

Simply install the punctuation server and enter its web address (such as http://localhost:5555/restore) into a new file named `external_api_urls.py` in the `worker` folder. E.g.

```python
$ cat worker/external_api_urls.py
PUNCTUATION_API_URL = "http://localhost:5555/restore"
````

Restart your speech recognition server..

```shell
$ make down
$ make up
```

The result of testing the API with the `speech.wav` file will this time give a transcription that is capitalized and punctuated:

```
$ curl localhost:5511/get_srt/?stt_id=.....
1
00:00:00,619 --> 00:00:05,170
Mae ganddynt ddau o blant, mab a merch.
```
