#!/bin/bash

eval ARR=("$(ls /images/ --quoting-style=shell)")
mkdir -p ./temp
rm temp/*
cp /images/${ARR[-1]}/* ./temp/

ls ./temp/*.jpg | awk '{ printf "mv %s ./temp/source%04d.jpg\n", $0, NR }' | sh

ffmpeg \
  -pattern_type glob \
  -i './temp/*.jpg' \
  -vf 'zoompan=d=(0.2+0.1)/0.1:s=800x600:fps=1/0.1,framerate=25:interp_start=0:interp_end=255:scene=100' \
  -c:v mpeg4 \
  -q:v 1 \
  video.mp4


