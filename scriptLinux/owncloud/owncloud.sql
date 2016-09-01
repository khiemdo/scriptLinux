create database if not exists owncloud;
grant all privileges on owncloud.* to ownclouduser@localhost identified by 'defaultPassword';
flush privileges;