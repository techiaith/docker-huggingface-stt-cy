# Gweinydd Adnabod Lleferydd wav2vec2 Cymraeg

[(click here to read the README in English)](README_en.md)

## Cefndir

Os hoffwch chi osod a defnyddio'r peiriant adnabod lleferydd Cymraeg wav2vec2 yn 
lleol ar gyfrifiadur eich hunain, yn hytrach na defnyddio'r gwasanaeth API ar wefan 
https://api.techiaith.org/cy/ yna defnyddiwch yr adnoddau yn y ffolder hon. 

**D.S.** - mae modelau wav2vec2 yn eitha’ mawr, ac felly byddwch angen cyfrifiadur 
gyda digon o gof er mwyn eu defnyddio. Os nad oes digon o gof yn eich cyfrifiadur ond 
hoffwch chi ddal medru rhedeg peiriant adnabod lleferydd yn lleol, yna mae modelau
llai ar sail Mozilla DeepSpeech ar gael - https://github.com/techiaith/docker-deepspeech-cy-server

## Gosod

```
$ git clone https://github.com/techiaith/docker-wav2vec2-xlsr-ft-cy
$ cd docker-wav2vec2-xlsr-ft-cy/server
$ make
```

Mae'r proses gosod yn estyn modelau sydd wedi'i hyfforddi eisoes gan Uned Technolegau Iaith, Prifysgol Bangor.


## Defnyddio

I redeg, does ond angen un gorchymyn ychwanegol..

```
$ make run
```

I'w brofi'n syml, mae'n bosib gyrru'r ffeil wav enghreifftiol sydd wedi'i gynnwys o fewn y project.

``` 
$ curl -F 'soundfile=@speech.wav' localhost:5511/speech_to_text/
{"success": true, "version": 1, "text": "mae ganddynt ddau o blant mab a merch"}
```

Mae modd defnyddio recordiadau eich hunain, cyn belled â'u bod ar ffurf wav ac yn 16kHz, un sianel. 

Ewch i http://localhost:5511/static_html/index.hml er mwyn defnyddio'r peiriant adnabod lleferydd 
o fewn dudalen we gyda ffeiliau sain eraill neu feicroffon.


## Rhybudd

Rhaid cofio *ni fydd y canlyniadau pob tro yn hollol gywir*. Rydyn wedi mesur y gyfradd gwallau yn 15%, sydd yn uwch na Saesneg ac ieithoedd mawr eraill sydd â chyfraddau o dan 8%. 

Mae mesur gallu'r peiriant yn ogystal â'i wella yn waith sy'n dal yn parhau. 

Yn y cyfamser, os hoffwch chi weld y peiriannau yn gwella, yna recordiwch rhai brawddegau wefan Mozilla CommonVoice (https://voice.mozilla.org/cy), fel bydd gennyn ni ragor o ddata hyfforddi'r peiriannau. 
Neu defnyddiwch ein hap Macsen! (http://techiaith.cymru/macsen)


