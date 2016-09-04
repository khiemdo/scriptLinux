#!/usr/bin/env bash
#dependency: 
#	gogsInstall

BASE_FOLDER=$1
#stop and exit on first error
set -e 
WORKING_FOLDER=$(pwd)

#install dependencies
echo 'install dependencies'
apt-get -y update
apt-get -y install git wget nano nginx openssl php5-fpm php5-json php5-ldap libapache2-mod-php5

echo 'download codiad github and install'
rm -rf /var/www/codiad
git clone https://github.com/Codiad/Codiad /var/www/codiad
cp $WORKING_FOLDER/config.php /var/www/codiad/config.php
mkdir -p /var/www/codiad/workspace
chown www-data:www-data -R /var/www/codiad/
chmod go+w /var/www/codiad/config.php /var/www/codiad/workspace /var/www/codiad/plugins /var/www/codiad/themes /var/www/codiad/data
usermod -G git www-data
usermod -G www-data git

#generate codiad.pem key
echo 'Generate codiad openssl key'
mkdir /etc/nginx/ssl
cd /etc/nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout codiad.key -out codiad.crt -subj "/C=SG/ST=Singapore/L=Singapore/O=fnick2812/OU=fnick2812/CN=fnick2812"

#replace  php5-fpm config
echo 'replace php5-fpm config'
mv /etc/php5/fpm/php-fpm.conf /var/www/codiad/php-fpm.conf.bk
mv $WORKING_FOLDER/php-fpm.conf /etc/php5/fpm/php-fpm.conf

mv /etc/php5/fpm/pool.d/www.conf /var/www/codiad/www.conf.bk
mv $WORKING_FOLDER/www.conf /etc/php5/fpm/pool.d/www.conf

#edit nginx sites-available, ln sites-enabled
echo 'edit nginx sites-available, ln sites-enabled'
rm -rf /etc/nginx/sites-available/default
rm -rf /etc/nginx/sites-enabled/default
rm -rf /etc/nginx/sites-available/codiadSSL
cp $WORKING_FOLDER/codiadSSL /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/codiadSSL /etc/nginx/sites-enabled/codiadSSL

service php5-fpm restart
service nginx restart