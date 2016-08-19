#!/usr/bin/env bash
#exe: 
set -e 

apt-get install apt-transport-https -y --force-yes  
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key  | apt-key add -  
echo "deb https://dev2day.de/pms/ jessie main" | tee /etc/apt/sources.list.d/pms.list  
apt-get update  
apt-get install -t jessie plexmediaserver -y  