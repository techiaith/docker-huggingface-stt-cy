#!/bin/bash

## Script written by Leena Sarah Farhat and Dewi Bryn Jones

set -e

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
youtube-dl --download-archive downloaded.txt --rm-cache-dir -cwi --no-post-overwrites -o ${DATA_DIR}'/%(playlist_index)s - %(title)s.%(ext)s' --cookies=cookies.txt --extract-audio --audio-format mp3 https://www.youtube.com/playlist?list=$1

# convert, transcribe and save as clips...
TRANSCRIPTIONS_DIR=${DATA_DIR}/transcriptions
TRANSCRIPTIONS_WITH_LM_DIR=${DATA_DIR}/transcriptions_withlm

mkdir -p ${TRANSCRIPTIONS_DIR}
mkdir -p ${TRANSCRIPTIONS_WITH_LM_DIR}

for filepath in ${DATA_DIR}/*.mp3
do 
    if [ -f "$filepath" ]; then
        ffmpeg -i "${filepath}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${filepath}.wav"
        
        filename_ext=${filepath##*/}
        filename=${filename_ext%.*}

        echo "Transcribing without language model, then spliting..."
        python3 transcriber.py -w "${filepath}.wav" -s "${TRANSCRIPTIONS_DIR}/${filename}.srt"
        python3 split_audio.py --wavfile "${filepath}.wav" --srt "${TRANSCRIPTIONS_DIR}/${filename}.srt" --destdir ${TRANSCRIPTIONS_DIR} 

        echo "Transcribing with language model, then spliting..."        
        python3 transcriber.py -w "${filepath}.wav" -l -s "${TRANSCRIPTIONS_WITH_LM_DIR}/${filename}.srt"
        python3 split_audio.py --wavfile "${filepath}.wav" --srt "${TRANSCRIPTIONS_WITH_LM_DIR}/${filename}.srt" --destdir ${TRANSCRIPTIONS_WITH_LM_DIR}                   
    fi
done

python3 validate_audio.py --clips_dir ${TRANSCRIPTIONS_DIR}/clips
python3 validate_audio.py --clips_dir ${TRANSCRIPTIONS_WITH_LM_DIR}/clips
