#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get -y update
apt-get -y install git wget nano python python-pip python-mysqldb 

pip install pexpect
pip install MySQL-python

./mysqlServerInstall.py#todo
