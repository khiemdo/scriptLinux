#http://manual.seafile.com/deploy/using_sqlite.html
#!/usr/bin/env bash
BASE_FOLDER=$1
#stop and exit on first error
set -e 
set -x
#install dependencies
apt-get update
apt-get install -y git wget nano elinks nginx

export VERSION_SEAFILE=seafile-server_5.1.4_stable_pi
export SOURCE_SEAFILE=https://github.com/haiwen/seafile-rpi/releases/download
export VERSION_NUMBER_SEAFILE=v5.1.4
export MYSQL_ROOT_PASSWD=khiem2812
export MYSQL_USER_PASSWD=khiem2812

#/home/seafile/haiwen/seafile-server-*
adduser --disabled-login --gecos 'Gogs' seafile
su - seafile
cd /home/seafile

mkdir -p haiwen
cd haiwen 
wget $SOURCE_SEAFILE/$VERSION_NUMBER_SEAFILE/$VERSION_SEAFILE.tar.gz
tar -xzf $VERSION_SEAFILE.tar.gz
mkdir installed
mv $VERSION_SEAFILE installed
apt-get install python2.7 libpython2.7 python-setuptools python-imaging python-ldap python-mysqldb python-memcache python-urllib3
cd seafile-server-*
./setup-seafile-mysql.sh auto \
	-n seafileRasp \
	-i www.seafile.fnick2812.com \
	-p 8082 \
	-d ./data \
	-e 0 \
	-o 127.0.0.1 \
	-t 3306 \
	-r $MYSQL_ROOT_PASSWD
	-u seafile \
	-w $MYSQL_USER_PASSWD \
	-c ccnet-db \
	-s seafile-db \
	-b seahub-db \

ln -s /home/seafile/haiwen/$VERSION_SEAFILE/seafile.sh /home/seafile/seafile.sh
ln -s /home/seafile/haiwen/$VERSION_SEAFILE/seahub.sh /home/seafile/seahub.sh
cp seafile.service /etc/systemd/system/seafile.service
cp seahub.service /etc/systemd/system/seahub.service
cp seafile-client.service /etc/systemd/system/seafile-client.service
systemctl enable seafile.service
systemctl enable seahub.service
systemctl enable seafile-client.service
systemctl daemon-reload