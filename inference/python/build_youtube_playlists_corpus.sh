#!/bin/bash

rm -rf /data/welsh-youtube-corpus/dataset
rm -rf /data/welsh-youtube-corpus/transcription_files

# techiaith pretrained
./ytpl_build.sh PLkNuNDk4pYpWpE1n-iIAPRtQNolth4pVq

# Y Babell Lên
./ytpl_build.sh PLNbPx7YxCU13Z6E_ZoFNZOFpYAPP7xMcw 

# Hansh - Straeon Stiwdio 
./ytpl_build.sh PLMUgzTukecfPY5rtNt0t8JuYZEJPPrhTi

# Hansh - Her Ffilm Fer
./ytpl_build.sh PLMUgzTukecfNycx2qxPJ0nsf5elNR--zk

# Hansh - Mae Bywydau Duon o Bwys
./ytpl_build.sh PLMUgzTukecfPQannXfBqovMTFqJGtQRST
