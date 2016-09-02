#!/usr/bin/env bash
BASE_FOLDER=$1
MYSQL_PASSWORD=root
#stop and exit on first error
set -e 
set -x
#install dependencies
apt-get update
apt-get install -y git wget nano elinks nginx
apt-get install -y php5-fpm php5-mysql openssl ssl-cert php5-cli php5-common php5-cgi php-pear php-apc curl libapr1 libtool php5-curl libcurl4-openssl-dev php-xml-parser php5-dev php5-gd libmemcached* memcached php5-memcached
apt-get install -y php5-fpm nginx

#/home/seafile/haiwen/seafile-server-*
adduser --disabled-login --gecos 'owncloud' owncloud
cd /home/owncloud

wget -nv https://download.owncloud.org/download/repositories/stable/Debian_8.0/Release.key -O Release.key
apt-key add - < Release.key

sh -c "echo 'deb http://download.owncloud.org/download/repositories/stable/Debian_8.0/ /' >> /etc/apt/sources.list.d/owncloud.list"
apt-get update
apt-get install -y owncloud-files

service mysql start
#mysql script
mysql -u root -p$MYSQL_PASSWORD < owncloud.sql
#nginx config
cp owncloud /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/owncloud /etc/nginx/sites-enabled/owncloud
