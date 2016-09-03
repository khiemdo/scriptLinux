#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update
apt-get install git wget nano elinks 

adduser --disabled-login --gecos 'Gogs' git
su - git
cd /home/git
mkdir local

export VERSION_GOLANG=go1.7.linux-armv6l
export SOURCE_GOLANG=https://storage.googleapis.com/golang
wget $SOURCE_GOLANG/$VERSION_GOLANG.tar.gz
tar -C /home/git/local -xzf go*.tar.gz

cd ~
echo 'export GOROOT=$HOME/local/go' >> $HOME/.bashrc
echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc
echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc
source $HOME/.bashrc

go get -u github.com/gogits/gogs
cd $GOPATH/src/github.com/gogits/gogs
go build -tags "sqlite tidb pam cert"
cd $GOPATH/src/github.com/gogits/gogs

exit