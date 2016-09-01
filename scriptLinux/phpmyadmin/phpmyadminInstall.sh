# Install MySQL Server in a Non-Interactive mode. Default root password will be "root"
DBHOST=localhost
DBNAME=raspFnick2812
DBUSER=pi
DBPASSWD=yourPassword

apt-get update

 
apt-get -y install mysql-client php5-mysql >> ./phpmyadminInstall.log 2>&1

service mysql restart
ln -s /usr/share/phpmyadmin/ /var/www/html/

