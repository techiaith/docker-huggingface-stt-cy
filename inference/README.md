# Sut i Ddefnyddio Modelau Adnabod Lleferydd wav2vec2.

[(click here to read the README in English)](README_en.md)

## Cefndir

Cynnigir sawl dddull i alluogi defnyddio'r modelau adnabod lleferydd y project hwn yn lleol ac/neu o fewn projectau meddalwedd eich hunain.

 - o linell gorchymun 
 - o fewn cod Python eich hunain
 - o API ar weinydd lleol - gweler [server/README.md](server/README.md)
 - o API ar weinydd gan - gweler https://api.techiaith.org
 - o fewn wefan cywiro trawsgrifiadau awtomatig er mwyn creu is-deitlau - ewch i https://trawsgrifiwr.techiaith.cymru


## Llinell gorchymyn

### Gosod 

Byddwch angen cyfrifiadur gyda system weithredu sy'n darparu llinell gorchymyn tebyg i Linux, fel Ubuntu, Mac OS X neu Windows Sub-system for Linux. Byddwch angen yn ogystal [git](https://git-scm.com/downloads) a docker ([Windows](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers),[Linux](https://docs.docker.com/desktop/install/linux-install/),[Mac OS X](https://docs.docker.com/desktop/install/mac-install/))


```
$ git clone https://github.com/techiaith/docker-wav2vec2-cy
$ cd docker-wav2vec2-cy/inference
$ make
```

Mae'r proses yn estyn ac yn gosod modelau sydd wedi'i hyfforddi eisoes gan Uned Technolegau Iaith, Prifysgol Bangor.


### Defnyddio

Er mwyn drawsgrifio un ffeil yn sydyn, mae modd defnyddio sgript `transcriber.py` mewn modd debyg i'r canlynol

`$ docker run --rm -it -v ${PWD}/:${PWD} techiaith/wav2vec2-inference python3 transcriber.py -w ${PWD}/<ffeil>.wav`

Bydd hyn yn dangos trawsgrifiad o'r sain lleferydd ar y sgrin. E.e.

```
/home/<user>$ docker run --rm -it -v ${PWD}/:${PWD} techiaith/wav2vec2-inference python3 transcriber.py -w ${PWD}/speech.wav
split_only:  False
Initialising wav2vec2 model "techiaith/wav2vec2-xls-r-1b-ft-cy" from HuggingFace model repository
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Initializing KenLM language model...
/usr/local/lib/python3.8/dist-packages/torch/cuda/__init__.py:52: UserWarning: CUDA initialization: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx (Triggered internally at  /pytorch/c10/cuda/CUDAFunctions.cpp:100.)
  return torch._C._cuda_getDeviceCount() > 0
wav2vec loaded to device cpu
Processing: /home/<user>/speech.wav
1 0.619581589958159 5.170041841004185 mae ganddynt ddau o blant mab a merch
1
00:00:00,619 --> 00:00:05,170
mae ganddynt ddau o blant mab a merch

<praatio.tgio.IntervalTier object at 0x7f10cf958430>
```

I gadw'r trawsgrifiad i ffeil `.srt` a `.TextGrid`, ychwanegwch enw ffeil allbwn:

```shell
/home/<user>$ docker run --rm -it -v ${PWD}/:${PWD} techiaith/wav2vec2-inference python3 transcriber.py -w ${PWD}/speech.wav -s ${PWD}/speech.srt
split_only:  False
Initialising wav2vec2 model "techiaith/wav2vec2-xls-r-1b-ft-cy" from HuggingFace model repository
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Initializing KenLM language model...
/usr/local/lib/python3.8/dist-packages/torch/cuda/__init__.py:52: UserWarning: CUDA initialization: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx (Triggered internally at  /pytorch/c10/cuda/CUDAFunctions.cpp:100.)
  return torch._C._cuda_getDeviceCount() > 0
wav2vec loaded to device cpu
Processing: /home/<user>/speech.wav
1 0.619581589958159 5.170041841004185 mae ganddynt ddau o blant mab a merch
srt file of transcription saved to /home/<user>/speech.srt
Textgrid of transcription saved to /home/<user>/speech.TextGrid
```

#### Trawsgrifio fideo YouTube

Er mwyn is-deitlau fideo YouTube yn lleol, defnyddiwch y sgript `yt.sh`. 

Er enghraifft ar gyfer fideo https://www.youtube.com/watch?v=OpiwHxPPqRI mae'r enghraifft isod yn creu ffeiliau `OpiwHxPPqRI.TextGrid` ac `OpiwHxPPqRI.srt` o fewn y ffolder `recordings`.


```
/home/<user>$ docker run --rm -it -v ${PWD}/recordings/:/recordings techiaith/wav2vec2-inference yt.sh OpiwHxPPqRI

+ youtube-dl --extract-audio --audio-format mp3 'https://www.youtube.com/watch?v=OpiwHxPPqRI'
[youtube] OpiwHxPPqRI: Downloading webpage
[youtube] OpiwHxPPqRI: Downloading MPD manifest
[download] Destination: Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.webm
[download] 100% of 3.51MiB in 00:54
[ffmpeg] Destination: Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3
Deleting original file Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.webm (pass -k to keep)
+ ffmpeg -i 'Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3' -vn -acodec pcm_s16le -ar 16000 -ac 1 /recordings/OpiwHxPPqRI.wav
ffmpeg version 4.2.7-0ubuntu0.1 Copyright (c) 2000-2022 the FFmpeg developers
  built with gcc 9 (Ubuntu 9.4.0-1ubuntu1~20.04.1)
  configuration: --prefix=/usr --extra-version=0ubuntu0.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-avresample --disable-filter=resample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librsvg --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-nvenc --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
Input #0, mp3, from 'Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3':
  Metadata:
    encoder         : Lavf58.29.100
  Duration: 00:03:33.67, start: 0.023021, bitrate: 101 kb/s
    Stream #0:0: Audio: mp3, 48000 Hz, stereo, fltp, 100 kb/s
    Metadata:
      encoder         : Lavc58.54
Stream mapping:
  Stream #0:0 -> #0:0 (mp3 (mp3float) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, wav, to '/recordings/OpiwHxPPqRI.wav':
  Metadata:
    ISFT            : Lavf58.29.100
    Stream #0:0: Audio: pcm_s16le ([1][0][0][0] / 0x0001), 16000 Hz, mono, s16, 256 kb/s
    Metadata:
      encoder         : Lavc58.54.100 pcm_s16le
size=    6677kB time=00:03:33.64 bitrate= 256.0kbits/s speed= 767x    
video:0kB audio:6676kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.001141%
+ rm 'Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3'
+ python3 transcriber.py -w /recordings/OpiwHxPPqRI.wav -s /recordings/OpiwHxPPqRI.srt
split_only:  False
Initialising wav2vec2 model "techiaith/wav2vec2-xls-r-1b-ft-cy" from HuggingFace model repository
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Initializing KenLM language model...
/usr/local/lib/python3.8/dist-packages/torch/cuda/__init__.py:52: UserWarning: CUDA initialization: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx (Triggered internally at  /pytorch/c10/cuda/CUDAFunctions.cpp:100.)
  return torch._C._cuda_getDeviceCount() > 0
wav2vec loaded to device cpu
Processing: /recordings/OpiwHxPPqRI.wav
1 0.0 1.630135135135135 
2 0.0 2.290714285714286 
3 0.0 2.8303846153846157 
4 3.169469387755102 8.279020408163266 fel arfer byddwn ni yn unedd technolegau iaith canolfan bedwr ym mhrifysgol bangor yn rhoi
5 8.298979591836734 12.67004081632653 ryw sesiwn fach yn yr eisteddfod genedlaethol i ddangos peth o'r gwaith
6 12.739945945945946 18.225081081081083 diweddarah a rhoed rhyw rhagflas o bethau newydd sydd ar y ffordd eleni wrth gwrs
7 18.34475675675676 20.080054054054056 chawson ni ddim steddfod
8 20.206799999999998 20.590799999999998 ond
9 20.679771428571428 24.100114285714287 roeddwn i'n dal isio roi driw flas bach iddoch chi o'n gwaith
10 24.189963099630994 28.226236162361623 dyma cysgliad os ydach chi ddim yn gwybod yn barod mwy o ymau helpu chi
11 28.266199261992618 32.7420664206642 ysgrifennu yn y gymraeg ar fformai o'n gwneud hyn ydy troi cysyll sydd ar gyfer
12 32.8419741697417 34.9600184501845 gwirio sillafu a gramadeg cymraeg
13 35.04949367088607 36.55025316455696 gan cynnwys tru glo
14 37.109240506329115 40.00006329113924 sori gan gynnwys treiglo
15 40.438983050847455 41.470169491525425 dyna wy llant
16 42.02961102106969 47.80492706645057 a cysgeir sef casgliad o eiriaduron cynhwysfawr sydd yn hawdd yw chwilio elle bwch chi'n
17 47.844894651539704 53.86001620745543 gofyn pwy sy'n gallu gael copi o'r meddalwedd anhygol yma am ddim wel y cyhoedd
18 53.080648298217184 53.86001620745543 
19 54.12941489361702 60.15335106382978 y byd addysg a chwmnïau sy'n cyflogi hydd at deg person alle gellych chi ddarganfod
20 60.17329787234042 61.39005319148936 y cysgliad
21 61.53677419354838 62.020645161290325 wel
22 62.22986631016043 68.04208556149733 cysgliad dodcom digon syml a os oes angen cymorth gyda unrhyw beth ar y wefan
23 68.44155080213903 73.29505347593582 yn ogystal â'r tudalen cymorth mae sgwrsffot ar gael i chi ofyn cwestiynau iddo unrhyw
24 73.335 77.05002673796791 bryd gan fod llawer iawn ohonom yn gweithio adraf ar hyn o bryd
25 77.26026058631922 81.68745928338762 mae 'r porth termau yn berffaith i helpu chi gyda hyn mae hwn yn gadael
26 81.72752442996743 85.35342019543974 i chi fynd ar dros ugian o eiriaduron termau gwahanol ar y we ac os
27 85.41351791530946 89.3799674267101 ydach chi eisiau fersiynhwylus i gario gwmpas gyda chi i bob man
28 89.44995735607677 94.51912579957357 yna mae'r ap guriaduron yn cynnwys nifer o'r gydiaduronmae mwy o datblygiadau newydd ar y
29 94.55904051172709 98.77004264392325 ffordd hefyd os ydych chi wedi blino gorfod siarad saesneg gyda olecsa
30 98.82 102.25005780346821 mae gyda ni brwt y teip cynorthwyydd personol cymraeg
31 102.59955719557196 107.00324723247232 macsen ma'n gweithio fo ap ar eich ffôn symudol yn daethech chi beth bynnag gyda
32 107.0231734317343 107.86007380073801 chi isio gwybod
33 107.98960975609755 111.9700975609756 rydyn ni werthu'n gwella'r ap ag yn ychwanegu pedwar sgil newydd iddo
34 112.1797159090909 115.57005681818183 yn cynnwys rhai i gael podleyddiadau rhaglenni esperd yr ek
35 115.67974137931034 117.91008620689655 dyma i chi flas ar sgil sbotsoffai
36 118.0295744680851 119.83021276595744 chware fiwsig cyrff
37 123.92523985239852 125.32007380073802 clasur
38 125.94965034965034 128.68006993006992 rydyn ni hefyd yn gwella eu lleisiau synthetig
39 128.94845070422534 131.53014084507043 a erbyn mis mawrth igian inarigian
40 131.61957446808512 133.42021276595744 bydd gyda ni pedwar llais newydd
41 133.63957894736842 135.43010526315788 fenywaidd a gwrywoedd
42 135.5798663101604 140.852807486631 de a gogledd ac bydd y datblygwyr yn medru eu rhoi nhw yn eu meddalwedd
43 141.05254010695185 145.526550802139 mae creu lleisiau synddetig yn bwysig ar gyfer pobl sy'n colli'r gallu i siarad ei
44 145.5664973262032 150.4000267379679 hun dwy flynydd ynol mi wnaethyn i ddatblygu'r rhaglen lleisiwr gyda'r gwasanaeth iechyd
45 0.0 150.9109090909091 
46 151.05992163009404 155.4764576802508 a chyn bo hir mi fygyn yn nu lleisiwr dau sydd yn cynnig gwell gwasanaeth
47 155.57637931034483 160.4925235109718 i gleifion os hoffech chi i helpun ni i ddatblygu'r dechnoleg yma cofiwch gech hi
48 160.5324921630094 163.6900156739812 ddal i gyfrannu eich llais i comin foes
49 163.86974226804125 167.62005154639175 rydyn ni'n defnyddio'r recordiau hyn i wella ei'n rhaglenni adnabod lleferydd
50 167.72993927125503 171.7458704453441 ac os ydach chi yn mwynhau y broses o recordio a darllen y brawddegau hyn
51 171.76585020242914 175.9815789473684 yn uchel beth am gynnig eich hyn fel talant iais yn ni ar gyfer creu
52 176.02153846153846 177.52002024291497 lleisiau synthetig newydd
53 177.99870967741936 180.28016129032258 rydyn ni'i chwilio am bedwar talant llais
54 180.42956896551726 184.93008620689653 au gydag acen gogledd dau gydag acen deheuol dynion a merched
55 185.01988826815642 188.5300558659218 rydyn ni'n cynnig tawl bychan am gael ddefnyddio eich llais
56 188.97750000000002 190.15012499999997 diolch fawr am wylio
57 190.40071942446042 192.96992805755397 gobeithio bod y fideo yma wedi bod o gymorth i chi
58 193.29933774834436 196.18013245033112 ac eich bod chi'n mwynhau defnyddio ein cyflysterau ni
59 0.0 196.9902857142857 
60 0.0 197.74079999999998 
61 0.0 199.1203448275862 
62 0.0 202.03006993006994 
63 0.0 203.44026315789475 
64 203.50909090909093 203.89090909090908 engo
65 0.0 207.8204347826087 
66 0.0 208.6308 
srt file of transcription saved to /recordings/OpiwHxPPqRI.srt
Textgrid of transcription saved to /recordings/OpiwHxPPqRI.TextGrid
```

Ewch i'r ffolder `recordings` i ganfod ffeil `.srt` (`.wav` a `.TextGrid`) ar gyfer y fideo:

```shell
/home/<user>$ cd recordings/
/home/<user>/recordings$ ls -l
total 6708
-rw-r--r-- 1 root root    4737 Oct  5 17:01 OpiwHxPPqRI.srt
-rw-r--r-- 1 root root   17766 Oct  5 17:01 OpiwHxPPqRI.TextGrid
-rw-r--r-- 1 root root 6836776 Oct  5 17:00 OpiwHxPPqRI.wav
```

## Scriptiau Python

Mae modd defnyddio'r modelau o fewn sgript Python syml fel y canlynol. **D.S.** nid yw'r enghraifft yma yn defnyddio model iaith i wella cywirdeb canlyniadau adnabod lleferydd o'r model acwstig.

### Dibyniaethau

```shell
$ python3 -m pip install -r python/requirments.txt
```

### Cod Python Enghreifftiol

```python
import torch
import librosa
import torchaudio

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("techiaith/wav2vec2-xlsr-ft-cy")
model = Wav2Vec2ForCTC.from_pretrained("techiaith/wav2vec2-xlsr-ft-cy")

audio, rate = librosa.load(<path/to/wav/audiofile>, sr=16000)

inputs = processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True)

with torch.no_grad():
  logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

# greedy decoding
predicted_ids = torch.argmax(logits, dim=-1)

print("Prediction:", processor.batch_decode(predicted_ids))

```
