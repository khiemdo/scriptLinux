#!/usr/bin/env bash
apt-get install \
	libevent-dev \
	libcurl4-openssl-dev \
	libglib2.0-dev \
	uuid-dev \
	intltool \
	libsqlite3-dev \
	libmysqlclient-dev \
	libarchive-dev \
	libtool \
	libjansson-dev \
	valac \
	libfuse-dev

wget http://sgp1.mirrors.digitalocean.com/mariadb//connector-c-2.3.1/mariadb-connector-c-2.3.1-src.tar.gz
tar -zxf mariadb* 
cd mariadb*
cmake .
make
make install
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/mariadb

wget https://github.com/ellzey/libevhtp/archive/1.1.6.tar.gz
tar -zxf 1.1.6*
cd libevhtp*
cmake -DEVHTP_DISABLE_SSL=ON -DEVHTP_BUILD_SHARED=ON .
make
make install