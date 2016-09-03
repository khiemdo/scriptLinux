#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get update
apt-get install git wget nano python python-pip 


