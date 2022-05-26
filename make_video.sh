#!/bin/bash

eval ARR=("$(ls /images/ --quoting-style=shell)")
mkdir -p ./temp
rm temp/*
cp /images/${ARR[-1]}/* ./temp/

ls ./temp/*.jpg | awk '{ printf "mv %s ./temp/source%04d.jpg\n", $0, NR }' | sh
ffmpeg -f image2 -r 15 -i ./temp/source%04d.jpg -r 15 -an -vcodec libx264 -pix_fmt yuv420p ./temp/video.mp4
