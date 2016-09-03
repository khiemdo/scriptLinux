#!/usr/bin/env bash
#dependency: 
#	mysql-server
BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update
apt-get install git wget nano  

ROOT_MYSQL_PASSWD='root'
SQL_SCRIPT_FILE='gogs.sql'
mysql -u root -p$ROOT_MYSQL_PASSWD < $SQL_SCRIPT_FILE

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
go build
cd $GOPATH/src/github.com/gogits/gogs/scripts/systemd/gogs.service /lib/systemd/system
systemctl enable gogs.service
systemctl start gogs.service

exit