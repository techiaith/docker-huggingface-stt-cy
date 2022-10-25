#!/bin/bash

## Script written by Leena Sarah Farhat and Dewi Bryn Jones

help()
{
    echo
    echo "Llwytho i lawr playlist fideo YouTube a chreu ffeil srt gyda segmentau"
    echo
    echo "Download videos from a YouTube playlist and create SRT files with segments"
    echo
    echo "Usage: $ ./`basename $0` [OPTIONS] "
    echo
    echo "Options:"
    echo 
    echo " <YouTube playlist id>"
    echo
    echo "Example: "
    echo
    echo "$ ytpl_download.sh PLZ8Xx5GjMhRqs1O-PuINm4gbDr1SKFSjn"
    echo
}

if [ -z "$1" ]; then
    help
    exit 1
fi

echo
echo "#### Downloading and processing audio from playlist $1 ####"
echo

set -x

CORPUS_ROOT_DIR='/data/welsh-youtube-corpus'

DOWNLOADS_DIR=${CORPUS_ROOT_DIR}/downloads/$1
mkdir -p ${DOWNLOADS_DIR}

# download videos...
youtube-dl --download-archive ${DOWNLOADS_DIR}/downloaded.txt --rm-cache-dir -cwi --no-post-overwrites -o ${DOWNLOADS_DIR}'/%(playlist_index)s - %(title)s.%(ext)s' --cookies=cookies.txt --extract-audio --audio-format mp3 https://www.youtube.com/playlist?list=$1

# convert, transcribe and save as clips...
TRANSCRIPTION_FILES_DIR=${CORPUS_ROOT_DIR}/transcription_files

DATA_ROOT_DIR=${CORPUS_ROOT_DIR}/dataset

CLIPS_DIR=${DATA_ROOT_DIR}/clips
CSV_FILE=${DATA_ROOT_DIR}/clips.tsv

mkdir -p ${TRANSCRIPTION_FILES_DIR}
mkdir -p ${CLIPS_DIR}

for filepath in ${DOWNLOADS_DIR}/*.mp3
do 
    if [ -f "$filepath" ]; then
    
        filename_ext=${filepath##*/}
        filename=${filename_ext%.*}
        wavfile_path=$TRANSCRIPTION_FILES_DIR/${filename}.wav

        ffmpeg -i "${filepath}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${wavfile_path}"

        #             
        python3 transcriber.py --split_only \
                                -w "${wavfile_path}" \
                                -s "${TRANSCRIPTION_FILES_DIR}/${filename}.srt" 
        
        #
        python3 split_audio.py --wavfile "${wavfile_path}" \
                                --srt "${TRANSCRIPTION_FILES_DIR}/${filename}.srt" \
                                --destdir ${CLIPS_DIR} \
                                --csvfile ${CSV_FILE}       

    fi
done
