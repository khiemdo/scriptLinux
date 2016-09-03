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
service mysql start
mysql -u root -p$ROOT_MYSQL_PASSWD < $SQL_SCRIPT_FILE

if !id "git" >/dev/null 2>&1;
then
	echo 'git user does not exist. create git user'
	adduser --disabled-login --gecos 'Gogs' git
fi
chown git gogsInstallByGitUser.sh
chmod +x gogsInstallByGitUser.sh
su git -c '/bin/bash ./gogsInstallByGitUser.sh'
 

cp gogs.service /lib/systemd/system
systemctl enable gogs.service
systemctl start gogs.service
