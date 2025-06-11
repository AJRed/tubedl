#!/bin/sh

for e in ../new_videos/*; do
	echo Output name for $e
	read name
	echo INPUT: "$e"
	echo OUTPUT: "$name"
	ffmpeg -i "$e" -q:a 0 -map a "$name"
done
