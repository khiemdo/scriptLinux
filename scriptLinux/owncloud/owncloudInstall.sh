#!/usr/bin/env bash
BASE_FOLDER=$1
MYSQL_PASSWORD=root
#stop and exit on first error
set -e 
set -x
#install dependencies
apt-get update

#/home/seafile/haiwen/seafile-server-*
adduser --disabled-login --gecos 'owncloud' owncloud
cd /home/owncloud

wget -nv https://download.owncloud.org/download/repositories/stable/Debian_8.0/Release.key -O Release.key
apt-key add - < Release.key

echo \'deb http://download.owncloud.org/download/repositories/stable/Debian_8.0/ /\' >> /etc/apt/sources.list.d/owncloud.list
apt-get update
apt-get install -y owncloud-files

service mysql start
#nginx config

cp owncloud /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/owncloud /etc/nginx/sites-enabled/owncloud
