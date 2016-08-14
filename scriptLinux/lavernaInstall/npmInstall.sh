#!/usr/bin/env bash

set -e 

VERSION_NODEJS='node-v6.3.1-linux-armv7l'
SOURCE_NODEJS='https://nodejs.org/dist/latest'
INSTALL_FOLDER='/opt'

rm -f $VERSION_NODEJS.tar.gz
wget $SOURCE_NODEJS/$VERSION_NODEJS.tar.gz
mv $VERSION_NODEJS.tar.gz $INSTALL_FOLDER
cd $INSTALL_FOLDER
tar -xzf $INSTALL_FOLDER/$VERSION_NODEJS.tar.gz
rm $INSTALL_FOLDER/$VERSION_NODEJS.tar.gz

rm -f /usr/bin/node
rm -f /usr/bin/npm
ln -s /opt/$VERSION_NODEJS/bin/node /usr/bin/node
ln -s /opt/$VERSION_NODEJS/bin/npm /usr/bin/npm