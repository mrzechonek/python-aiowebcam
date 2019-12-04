#!/bin/sh

set -x

VP9_LIVE_PARAMS="-speed 6 -tile-columns 4 -frame-parallel 1 -threads 8 -static-thresh 0 -max-intra-rate 300 -deadline realtime -lag-in-frames 0 -error-resilient 1"

HOST=$1
PORT=$2
TOKEN=$3

ffmpeg \
  -f v4l2 -input_format mjpeg -r 15 -s 640x360 -i /dev/video0 \
  -map 0:0 \
  -pix_fmt yuv420p \
  -c:v libvpx-vp9 \
    -s 640x360 -keyint_min 60 -g 1 ${VP9_LIVE_PARAMS} \
    -b:v 1000k \
  -f webm_chunk \
    -method PUT \
    -header "http://$HOST:$PORT/api/v1/video/header?s=$TOKEN" \
    -chunk_start_index 1 \
    "http://$HOST:$PORT/api/v1/video/chunks?s=$TOKEN&c=%d"
