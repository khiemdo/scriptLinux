#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update

adduser --disabled-login --gecos 'Gogs' git
su - git
cd ~
mkdir local
wget https://storage.googleapis.com/golang/go1.7.linux-armv6l.tar.gz
tar -C /home/git/local -xzf go*.tar.gz

cd ~
echo 'export GOROOT=$HOME/local/go' >> $HOME/.bashrc
echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc
source $HOME/.bashrc

go get -u github.com/gogits/gogs
cd $GOPATH/src/github.com/gogits/gogs
go build

cd $GOPATH/src/github.com/gogits/gogs
./gogs web