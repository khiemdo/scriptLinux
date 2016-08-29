#http://manual.seafile.com/deploy/using_sqlite.html
#!/usr/bin/env bash
BASE_FOLDER=$1
#stop and exit on first error
set -e 
set -x
#install dependencies
apt-get update
apt-get install -y git wget nano elinks 

export VERSION_SEAFILE=seafile-server_5.1.4_stable_pi
export SOURCE_SEAFILE=https://github.com/haiwen/seafile-rpi/releases/download
export VERSION_NUMBER_SEAFILE=v5.1.4

mkdir -p haiwen
cd haiwen 
wget $SOURCE_SEAFILE/$VERSION_NUMBER_SEAFILE/$VERSION_SEAFILE.tar.gz
tar -xzf $VERSION_SEAFILE.tar.gz
mkdir installed
mv $VERSION_SEAFILE installed
apt-get install python2.7 libpython2.7 python-setuptools python-imaging python-ldap python-urllib3 sqlite3
cd seafile-server-*
./setup-seafile.sh -n seafileRasp -i localhost -p 8082 -d /home/seafile/data
ulimit -n 30000
./seafile.sh start
./seahub.sh start 8000

