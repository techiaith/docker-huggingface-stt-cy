#!/bin/bash
set -e

help()
{
    echo
    echo "Trawsgrifio fideo YouTube a chreu ffeil srt er mwyn ei gywiro"
    echo
    echo "Usage: $ ./`basename $0` [OPTIONS] "
    echo
    echo "Options:"
    echo 
    echo " <YouTube video id>"
    echo
    echo "Example: "
    echo
    echo "$ yt.sh 6z8klxzufx8"
    echo
}

if [ -z "$1" ]; then
    help
    exit 1
fi

set -x

youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=$1
ffmpeg -i *.mp3 -vn -acodec pcm_s16le -ar 16000 -ac 1 /recordings/$1.wav
rm *.mp3
python3 transcriber.py -w /recordings/$1.wav


