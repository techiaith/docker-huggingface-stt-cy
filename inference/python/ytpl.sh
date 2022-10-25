#!/bin/bash

## Script written by Leena Sarah Farhat and Dewi Bryn Jones

help()
{
    echo
    echo "Trawsgrifio fideo YouTube playlist a chreu ffeil srt er mwyn ei gywiro"
    echo
    echo "Transcribe videos from a YouTube playlist and create SRT files for post-editing"
    echo
    echo "Usage: $ ./`basename $0` [OPTIONS] "
    echo
    echo "Options:"
    echo 
    echo " <YouTube playlist id>"
    echo
    echo "Example: "
    echo
    echo "$ ytpl.sh PLZ8Xx5GjMhRqs1O-PuINm4gbDr1SKFSjn"
    echo
}

if [ -z "$1" ]; then
    help
    exit 1
fi

set -x

DATA_DIR='/data/recordings/'$1

# download videos...
youtube-dl --download-archive ${DATA_DIR}/downloaded.txt --rm-cache-dir -cwi --no-post-overwrites -o ${DATA_DIR}'/%(playlist_index)s - %(title)s.%(ext)s' --cookies=cookies.txt --extract-audio --audio-format mp3 https://www.youtube.com/playlist?list=$1

set -e

# convert, transcribe and save as clips...
TRANSCRIPTIONS_DIR=${DATA_DIR}/transcriptions
TRANSCRIPTIONS_WITH_LM_DIR=${DATA_DIR}/transcriptions_withlm

mkdir -p ${TRANSCRIPTIONS_DIR}
mkdir -p ${TRANSCRIPTIONS_WITH_LM_DIR}

for filepath in ${DATA_DIR}/*.mp3
do 
    if [ -f "$filepath" ]; then
    
        filename_ext=${filepath##*/}
        filename=${filename_ext%.*}
        wavfile_path=$DATA_DIR/${filename}.wav

        ffmpeg -i "${filepath}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${wavfile_path}"
                
        echo "Transcribe with only acoustic model. Output srt file"
        cp -v "${wavfile_path}" ${TRANSCRIPTIONS_DIR}
        python3 transcriber.py -w "${wavfile_path}" -s "${TRANSCRIPTIONS_DIR}/${filename}.srt"

        echo "Transcribe with the help of a language model. Output srt file" 
        cp -v "${wavfile_path}" ${TRANSCRIPTIONS_WITH_LM_DIR}
        python3 transcriber.py -w "${wavfile_path}" -l -s "${TRANSCRIPTIONS_WITH_LM_DIR}/${filename}.srt"

        rm "${wavfile_path}"
    fi
done
