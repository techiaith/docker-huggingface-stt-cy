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
$ cd docker-wav2vec2-xlsr-ft-cy/inference/server
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
{"version": 1, "success": true, "text": " mae ganddynt ddau o blant mab a merch ", "alignment": [["m", 0.6003829787234042], ["a", 0.640468085106383], ["e", 0.7005957446808511], [" ", 0.7607234042553191], ["g", 0.8208510638297872], ["a", 0.8809787234042553], ["n", 0.9811914893617021], ["d", 1.0413191489361702], ["d", 1.1214893617021275], ["y", 1.1816170212765957], ["n", 1.2818297872340427], ["t", 1.3820425531914893], [" ", 1.4421702127659572], ["d", 1.6025106382978722], ["d", 1.6626382978723404], ["a", 1.7428085106382978], ["u", 1.923191489361702], [" ", 2.0634893617021275], ["o", 2.1236170212765955], [" ", 2.183744680851064], ["b", 2.2438723404255314], ["l", 2.304], ["a", 2.3440851063829786], ["n", 2.5044255319148934], ["t", 2.6647659574468086], [" ", 2.7449361702127657], ["m", 3.165829787234043], ["a", 3.266042553191489], ["b", 3.5466382978723403], [" ", 3.6067659574468083], ["a", 3.9474893617021274], [" ", 4.188], ["m", 4.248127659574467], ["e", 4.348340425531915], ["r", 4.448553191489362], ["c", 4.568808510638298], ["h", 4.588851063829787], [" ", 5.10995744680851]]}
```

Mae modd defnyddio recordiadau eich hunain, cyn belled â'u bod ar ffurf wav ac yn 16kHz, un sianel. 

Ewch i http://localhost:5511/static_html/index.hml er mwyn defnyddio'r peiriant adnabod lleferydd 
o fewn dudalen we gyda ffeiliau sain eraill neu feicroffon.


## Rhybudd

Rhaid cofio *ni fydd y canlyniadau pob tro yn hollol gywir*. Rydyn wedi mesur y gyfradd gwallau yn 15%, sydd yn uwch na Saesneg ac ieithoedd mawr eraill sydd â chyfraddau o dan 8%. 

Mae mesur gallu'r peiriant yn ogystal â'i wella yn waith sy'n dal yn parhau. 

Yn y cyfamser, os hoffwch chi weld y peiriannau yn gwella, yna recordiwch rhai brawddegau wefan Mozilla CommonVoice (https://voice.mozilla.org/cy), fel bydd gennyn ni ragor o ddata hyfforddi'r peiriannau. 
Neu defnyddiwch ein hap Macsen! (http://techiaith.cymru/macsen)
