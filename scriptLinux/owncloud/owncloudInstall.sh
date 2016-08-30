#http://manual.seafile.com/deploy/using_sqlite.html
#!/usr/bin/env bash
BASE_FOLDER=$1
#stop and exit on first error
set -e 
set -x
#install dependencies
apt-get update
apt-get install -y git wget nano elinks nginx
apt-get install -y php5-fpm php5-mysql openssl ssl-cert php5-cli php5-common php5-cgi php-pear php-apc curl libapr1 libtool php5-curl libcurl4-openssl-dev php-xml-parser php5-dev php5-gd libmemcached* memcached php5-memcached -y
apt-get install -y php5-fpm nginx -y
apt-get install -y php7.0-common php7.0-gd php7.0-json php7.0-curl  php7.0-zip php7.0-xml php7.0-mbstring

wget -nv https://download.owncloud.org/download/repositories/stable/Debian_8.0/Release.key -O Release.key
apt-key add - < Release.key

sh -c "echo 'deb http://download.owncloud.org/download/repositories/stable/Debian_8.0/ /' >> /etc/apt/sources.list.d/owncloud.list"
apt-get update
apt-get install -y owncloud-files

apt-get install -y mysql-server
#//mysql script
mysql -u root -p


#nginx config