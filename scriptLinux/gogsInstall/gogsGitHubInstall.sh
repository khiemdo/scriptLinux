#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update
apt-get install git wget 

rm -rf gogs
git clone https://github.com/gogits/gogs.git && cd gogs
rm -f Dockerfile
mv Dockerfile.rpi Dockerfile
mkdir -p /data
docker build -t fnick2812/gogsraspberry:gogsGithub .
docker run --name=gogsRasp -p 10022:22 -p 3000:3000 -v /var/gogs:/data fnick2812/gogsraspberry:gogsGithub
