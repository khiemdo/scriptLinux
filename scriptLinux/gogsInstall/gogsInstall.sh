#!/usr/bin/env bash
#dependency: 
#	mysql-server
#	nginx
#	openssl
BASE_FOLDER=$1
#stop and exit on first error--> BUT this script must disable
set -e 
WORKING_FOLDER=$(pwd)

#install dependencies
apt-get update
apt-get install git wget nano 

ROOT_MYSQL_PASSWD='root'
SQL_SCRIPT_FILE='gogs.sql'

service mysql start
mysql -u root -p$ROOT_MYSQL_PASSWD < $SQL_SCRIPT_FILE

set +o errexit
getent passwd 'git' > /dev/null 2&>1
ret=$?;
if [[ $ret -ne 0 ]]; then
	echo 'git user does not exist. create git user'
	adduser --disabled-login --gecos 'Gogs' git
fi
set -o errexit

chown git gogsInstallByGitUser.sh
chmod +x gogsInstallByGitUser.sh
su git -c '/bin/bash ./gogsInstallByGitUser.sh'

echo 'Generate codiad openssl key'
mkdir /etc/nginx/ssl
cd /etc/nginx/ssl 
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout gogs.key -out gogs.crt -subj "/C=SG/ST=Singapore/L=Singapore/O=fnick2812/OU=fnick2812/CN=fnick2812"

echo 'edit gogs app.ini'




echo 'edit nginx sites-available, ln sites-enabled'
rm -rf /etc/nginx/sites-available/default
rm -rf /etc/nginx/sites-enabled/default
rm -rf /etc/nginx/sites-available/gogsSSL
cp $WORKING_FOLDER/codiadSSL /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/gogsSSL /etc/nginx/sites-enabled/gogsSSL

echo 'install gogs.service'
chmod -x gogs.service
cp gogs.service /lib/systemd/system
systemctl enable gogs.service
systemctl restart gogs.service
