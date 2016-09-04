#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get -y update
apt-get -y install git wget nano nginx php5

git clone https://github.com/Codiad/Codiad /var/www/codiad
touch /var/www/codiad/config.php
chown www-data:www-data -R /var/www/codiad/