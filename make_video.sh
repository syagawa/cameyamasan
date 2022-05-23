#!/bin/bash

ls ./images/*.jpg | awk '{ printf "mv %s source%04d.jpg\n", $0, NR }' | sh
# ffmpeg -f image2 -r 15 -i source%04d.jpg -r 15 -an -vcodec libx264 -pix_fmt yuv420p video.mp4
