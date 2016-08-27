#http://blog.hypriot.com/post/run-docker-rpi3-with-wifi/
#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update

wget https://downloads.hypriot.com/docker-hypriot_1.10.3-1_armhf.deb
sudo dpkg -i docker-hypriot*.deb
rm -f docker-hypriot*.deb
sudo sh -c 'usermod -aG docker $SUDO_USER'
sudo systemctl enable docker.service

