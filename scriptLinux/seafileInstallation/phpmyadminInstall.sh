# Install MySQL Server in a Non-Interactive mode. Default root password will be "root"
DBHOST=localhost
DBNAME=raspFnick2812
DBUSER=pi
DBPASSWD=root

export DEBIAN_FRONTEND="noninteractive"
echo -e "\n--- Install MySQL specific packages and settings ---\n" >> ./phpmyadminInstall.log 2>&1
debconf-set-selections <<< "mysql-server mysql-server/root_password password $DBPASSWD"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DBPASSWD"
debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password $DBPASSWD"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password $DBPASSWD"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password $DBPASSWD"
debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect none"

apt-get -y install mysql-server phpmyadmin >> ./phpmyadminInstall.log 2>&1
apt-get -y install mysql-client php5-mysql >> ./phpmyadminInstall.log 2>&1

service mysql restart
ln -s /usr/share/phpmyadmin/ /var/www/html/

