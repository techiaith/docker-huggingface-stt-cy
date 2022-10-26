# Gweinydd Adnabod Lleferydd wav2vec2 Cymraeg

[**(click here to read the README in English)**](README_en.md)

## Cefndir

Os ydych yn pryderu am breifatrwydd unrhyw API adnabod lleferydd Cymraeg ar-lein, fel yr un gan https://api.techiaith.org/cy, yna mae cynnwys y ffolder hwn yn eich helpu i osod a defnyddio gosodiad lleol eich hunain.

## Gosod

```
$ git clone https://github.com/techiaith/docker-wav2vec2-cy
$ cd docker-wav2vec2-cy/inference/server
$ make
```

Mae'r proses gosod yn estyn modelau sydd wedi'i hyfforddi eisoes gan Uned Technolegau Iaith, Prifysgol Bangor.


## Defnyddio

I redeg, does ond angen un gorchymyn ychwanegol..

```
$ make up
```

I'w brofi'n syml, mae'n bosib gyrru'r ffeil wav enghreifftiol sydd wedi'i gynnwys o fewn y project.

``` 
$ curl -F 'soundfile=@speech.wav' localhost:5511/speech_to_text/
{"version": 1, "success": true, "id": "e1684eab-e472-4aaa-8c4f-66c007477a7f"}
```
(gallwch drawsgrifio eich recordiadau eich hun cyn belled â bod y ffeiliau mewn fformat wav a sianel mono 16kHz.)

Byddwch yn derbyn ymateb sydd i bob pwrpas ond yn gydnabyddiaeth o'ch cais sy'n cynnwys rhif adnabod. Gan y gall gymryd peth amser i berfformio lleferydd i destun ar ffeil, gallwch wirio'r statws gyda cheisiadau ping dilynol. Os yw hyd y sain yn hirach na 5-10 eiliad, bydd yr API yn segmentu gan ddefnyddio canfod llais.

```
$ curl localhost:5511/get_status/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
{"version": 1, "status": "PENDING"}
```

pan fydd y trawsgrifiad wedi'i gwblhau, bydd yr ymateb

```
$ curl localhost:5511/get_status/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
{"version": 1, "status": "SUCCESS"}
````

Gellir cael y canlyniadau mewn fformat srt:

```
$ curl localhost:5511/get_srt/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
1
00:00:00,619 --> 00:00:05,170
mae ganddynt ddau o blant mab a merch
```

json:  ( sy'n cynnwys aliniadau ar lefel geiriau )

```
$ curl localhost:5511/get_json/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
[{"text": "mae ganddynt ddau o blant mab a merch", "start": 0.619581589958159, "end": 5.170041841004185, "alignment": [{"word": "mae", "start": 0.619581589958159, "end": 0.7992050209205022}, {"word": "ganddynt", "start": 0.8391213389121339, "end": 1.457824267782427}, {"word": "ddau", "start": 1.6973221757322177, "end": 2.096485355648536}, {"word": "o", "start": 2.1563598326359834, "end": 2.1962761506276154}, {"word": "blant", "start": 2.256150627615063, "end": 2.7950209205020924}, {"word": "mab", "start": 3.1742259414225944, "end": 3.6133054393305444}, {"word": "a", "start": 3.9725523012552304, "end": 4.17213389121339}, {"word": "merch", "start": 4.251966527196653, "end": 5.170041841004185}]}]
```

neu csv:

```
$ curl localhost:5511/get_csv/?stt_id=e1684eab-e472-4aaa-8c4f-66c007477a7f
ID      Start   End     Transcript
1       0.619581589958159       5.170041841004185       mae ganddynt ddau o blant mab a merch
```

Mae'r gweinydd yn darparu GUI HTML syml iawn hefyd er mwyn defnyddio/cefnogi'r API uchod. Ewch i http://localhost:5511/static_html/index.hml