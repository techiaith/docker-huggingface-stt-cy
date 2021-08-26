# How to Use the wav2vec2 Welsh Language Speech Recognition Models.

[(cliciwch yma os hoffwch ddarllen y README Cymraeg)](README.md)

## Background

If you would like to install and use a wav2vec2 speech recognition engine locally
on your own computer, instead of using the API service at https://api.techiaith.org/en/ or the [Trawsgrifiwr Ar-lein transcription service website](https://trawsgrifiwr.techiaith.cymru) then the resources in this folder can help you. 

There are two possible ways to use the speech recognition locally, ether from the command line or as a server. Visit [server/README_en.md](server/README_en.md) to read how to install your own speech recognition server. This README will explain how to use the speech recognition machine from the command line.

**N.B.** - wav2vec2 models are quite large, therefore you will need plenty of memory
in your computer. If you don't have enough memory, but would still like to run locally
your own Welsh speech recognition engine, then smaller models based on Mozilla
DeepSpeech are available - https://github.com/techiaith/docker-deepspeech-cy-server

## Install

```
$ git clone https://github.com/techiaith/docker-wav2vec2-xlsr-ft-cy
$ cd docker-wav2vec2-xlsr-ft-cy/inference
$ make
```

The build process fetches models that have been pretrained by Bangor University's Language Technologies Unit.

## Use

Get started by using..

```
$ make run
```

A new command line prompt will appear where you can use the scripts `decode.py` or `transcribe.py` to convert files of speech audio into text. For example...

```shell
root@a20d8f23cb0f:/wav2vec2# python3 decode.py --wav speech.wav 
Downloading kenlm.tar.gz version 21.08
kenlm.tar.gz: 455MB [00:40, 11.2MB/s]                                                                                             
Extracting...
Initialising processor...
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████| 214/214 [00:00<00:00, 129kB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████| 437/437 [00:00<00:00, 284kB/s]
Downloading: 100%|████████████████████████████████████████████████████████████████████████████████| 181/181 [00:00<00:00, 123kB/s]
Downloading: 100%|█████████████████████████████████████████████████████████████████████████████| 85.0/85.0 [00:00<00:00, 58.5kB/s]
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Initialising wav2vec ctc model...
Downloading: 100%|███████████████████████████████████████████████████████████████████████████| 1.85k/1.85k [00:00<00:00, 1.29MB/s]
Downloading: 100%|███████████████████████████████████████████████████████████████████████████| 1.26G/1.26G [01:50<00:00, 11.5MB/s]
Initialising vocab...
Initialising ctc with lm decoder...
mae ganddynt ddau o blant mab a merch 0.6109205020920503 5.169916317991632 [{'word': 'mae', 'start': 0.6109205020920503, 'end': 0.7715899581589959}, {'word': 'ganddynt', 'start': 0.8117573221757324, 'end': 1.4544351464435148}, {'word': 'ddau', 'start': 1.6151046025104603, 'end': 2.077029288702929}, {'word': 'o', 'start': 2.137280334728034, 'end': 2.17744769874477}, {'word': 'blant', 'start': 2.2376987447698746, 'end': 2.820125523012553}, {'word': 'mab', 'start': 3.1816317991631804, 'end': 3.623472803347281}, {'word': 'a', 'start': 3.9648953974895402, 'end': 4.18581589958159}, {'word': 'merch', 'start': 4.246066945606695, 'end': 5.169916317991632}]
```

Use the `yt.sh` script to create locally subtitles for YouTube videos. For example for the video https://www.youtube.com/watch?v=OpiwHxPPqRI. The script creates new `.TextGrid` and `.srt` files in the `/recordings` folder.


```shell
root@413c6994d668:/wav2vec2# ./yt.sh OpiwHxPPqRI

+ youtube-dl --extract-audio --audio-format mp3 'https://www.youtube.com/watch?v=OpiwHxPPqRI'
[youtube] OpiwHxPPqRI: Downloading webpage
[youtube] OpiwHxPPqRI: Downloading MPD manifest
[download] Destination: Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.webm
[download] 100% of 3.51MiB in 00:00
[ffmpeg] Destination: Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3
Deleting original file Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.webm (pass -k to keep)
+ ffmpeg -i 'Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3' -vn -acodec pcm_s16le -ar 16000 -ac 1 /recordings/OpiwHxPPqRI.wav
ffmpeg version 4.2.4-1ubuntu0.1 Copyright (c) 2000-2020 the FFmpeg developers
  built with gcc 9 (Ubuntu 9.3.0-10ubuntu2)
  configuration: --prefix=/usr --extra-version=1ubuntu0.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-avresample --disable-filter=resample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librsvg --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-nvenc --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared
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
File '/recordings/OpiwHxPPqRI.wav' already exists. Overwrite ? [y/N] y
Stream mapping:
  Stream #0:0 -> #0:0 (mp3 (mp3float) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, wav, to '/recordings/OpiwHxPPqRI.wav':
  Metadata:
    ISFT            : Lavf58.29.100
    Stream #0:0: Audio: pcm_s16le ([1][0][0][0] / 0x0001), 16000 Hz, mono, s16, 256 kb/s
    Metadata:
      encoder         : Lavc58.54.100 pcm_s16le
size=    6677kB time=00:03:33.64 bitrate= 256.0kbits/s speed= 288x    
video:0kB audio:6676kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.001141%
+ rm 'Cynnyrch Uned Technolegau Iaith Prifysgol Bangor 2020-OpiwHxPPqRI.mp3'
+ python3 transcriber.py -w /recordings/OpiwHxPPqRI.wav
Model file /models/techiaith/wav2vec2-xlsr-ft-cy/21.08/kenlm.tar.gz already downloaded.
Initialising processor...
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
Initialising wav2vec ctc model...
Initialising vocab...
Initialising ctc with lm decoder...
srt file of transcription saved to /recordings/OpiwHxPPqRI.srt
Textgrid of transcription saved to /recordings/OpiwHxPPqRI.TextGrid
root@413c6994d668:/wav2vec2# 
```

## Warning

Please note that transcription results will not always be totally correct. We have 
measured the error rate to be 15%, which is higher than error rates for English and other 
larger languages that have error rates below 8%.

The work on measuring and improving the models' capabilities is ongoing work. 

In the meantime, if you would like to see the models improve, then record some Welsh
sentences on the Mozilla Common Voice (https://voice.mozilla.org/cy) website, so that
we will have more training data. Or use our voice assistant app - Macsen (http://techiaith.cymru/macsen)
