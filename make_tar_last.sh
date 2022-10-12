#!/bin/bash

eval ARR=("$(ls ./images/ --quoting-style=shell)")
mkdir -p ./temp
rm temp/*
cp /images/${ARR[-1]}/* ./temp/

ls ./temp/*.jpg | awk '{ printf "mv %s ./temp/source%04d.jpg\n", $0, NR }' | sh

find ./temp/ -name *.jpg | xargs tar -cvzf ./temp/imageslast.tar.gz
