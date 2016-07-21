#!/usr/bin/env bash

BASE_FOLDER=$1
#stop and exit on first error
set -e 
#install dependencies
apt-get install -y build-essential automake libxml2-dev libxslt1-dev python-dev libgd2-dev libperl-dev

# names of latest versions of each package
export VERSION_PCRE=pcre-8.39
export VERSION_ZLIB=zlib-1.2.8
export VERSION_OPENSSL=openssl-1.0.2f
export VERSION_GEOIP=GeoIP-1.6.8
export VERSION_NGINX=nginx-1.11.2

# URLs to the source directories
export SOURCE_PCRE=ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre
export SOURCE_ZLIP=http://zlib.net
export SOURCE_OPENSSL=https://www.openssl.org/source
export SOURCE_GEOIP=https://github.com/maxmind/geoip-api-c/releases/download/v1.6.8/
export SOURCE_NGINX=http://nginx.org/download
export SOURCE_ECHO_NGINX_MODULE=https://github.com/openresty/echo-nginx-module.git
export SOURCE_HEADERS_MORE_NGINX_MODULE=https://github.com/openresty/headers-more-nginx-module.git

rm -rf $BASE_FOLDER/nginxBuild
rm -rf /etc/nginx
mkdir -p $BASE_FOLDER/nginxBuild

#download source from internet
cd $BASE_FOLDER/nginxBuild
wget --no-check-certificate $SOURCE_PCRE/$VERSION_PCRE.tar.gz
wget --no-check-certificate $SOURCE_ZLIP/$VERSION_ZLIB.tar.gz
wget --no-check-certificate $SOURCE_OPENSSL/$VERSION_OPENSSL.tar.gz
wget --no-check-certificate $SOURCE_GEOIP/$VERSION_GEOIP.tar.gz
wget --no-check-certificate $SOURCE_NGINX/$VERSION_NGINX.tar.gz
mkdir nginxModules
cd nginxModules
git clone $SOURCE_ECHO_NGINX_MODULE
git clone $SOURCE_HEADERS_MORE_NGINX_MODULE

#extract compressed file
cd $BASE_FOLDER/nginxBuild
rm -rf $VERSION_GEOIP
rm -rf $VERSION_PCRE
rm -rf $VERSION_ZLIB
rm -rf $VERSION_OPENSSL
rm -rf $VERSION_NGINX

tar zxvf $VERSION_GEOIP.tar.gz
tar zxvf $VERSION_PCRE.tar.gz
tar zxvf $VERSION_ZLIB.tar.gz
tar zxvf $VERSION_OPENSSL.tar.gz
tar zxvf $VERSION_NGINX.tar.gz

cd $BASE_FOLDER/nginxBuild
cd $VERSION_PCRE
./configure
make
make install

cd $BASE_FOLDER/nginxBuild
cd $VERSION_ZLIB 
./configure
make
make install

cd $BASE_FOLDER/nginxBuild
cd $VERSION_GEOIP
./configure
make
make install

cd $BASE_FOLDER/nginxBuild
cd $VERSION_OPENSSL
./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib shared zlib-dynamic
make depend
make
make install

#./configure --user=www-data --group=www-data --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf--pid-path=/usr/local/nginx/nginx.pid --with-pcre=/home/pi/pcre-8.39 --with-zlib=/home/pi/zlib-1.2.8 --with-http_ssl_module --with-stream --add-dynamic-module=/home/pi/nginxModules/echo-nginx-module --add-dynamic-module=/home/pi/nginxModules/headers-more-nginx-module

cd $BASE_FOLDER/nginxBuild
cd $VERSION_NGINX
./configure \
--user=www-data \
--group=www-data \
--prefix=/usr/local/nginx \
--sbin-path=/usr/local/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--pid-path=/run/nginx.pid \
--lock-path=/run/lock/subsys/nginx \
--with-file-aio \
--with-ipv6 \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_addition_module \
--with-http_xslt_module \
--with-http_image_filter_module \
--with-http_geoip_module \
--with-http_sub_module \
--with-http_dav_module \
--with-http_flv_module \
--with-http_mp4_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_random_index_module \
--with-http_secure_link_module \
--with-http_degradation_module \
--with-http_stub_status_module \
--with-http_perl_module \
--with-mail \
--with-mail_ssl_module \
--with-debug \
--with-http_ssl_module --with-stream \
--with-pcre=../pcre-8.39 \
--with-zlib=../zlib-1.2.8 \
--add-dynamic-module=../nginxModules/echo-nginx-module \
--add-dynamic-module=../nginxModules/headers-more-nginx-module
make
make install

#install startup script
cp ./nginx.service /lib/systemd/system
systemctl enable nginx.service
systemctl start nginx.service

rm -f $VERSION_GEOIP.tar.gz
rm -f $VERSION_PCRE.tar.gz
rm -f $VERSION_ZLIB.tar.gz
rm -f $VERSION_OPENSSL.tar.gz
rm -f $VERSION_NGINX.tar.gz

#rm -rf GeoIP*
#rm -rf pcre*
#rm -rf zlib*
#rm -rf openssl*
#rm -rf nginx*
