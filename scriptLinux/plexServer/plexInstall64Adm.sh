#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error

set -e 
wget -O - http://shell.ninthgate.se/packages/shell.ninthgate.se.gpg.key | sudo apt-key add -
echo "deb http://www.deb-multimedia.org wheezy main non-free" | sudo tee -a /etc/apt/sources.list.d/deb-multimedia.list
echo "deb http://shell.ninthgate.se/packages/debian wheezy main" | sudo tee -a /etc/apt/sources.list.d/plex.list
sudo apt-get update && sudo apt-get install deb-multimedia-keyring --force-yes
sudo apt-get update && sudo apt-get install plexmediaserver -y