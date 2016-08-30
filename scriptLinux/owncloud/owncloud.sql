create database owncloud;
create user ownclouduser@localhost identified by 'password';
grant all privileges on owncloud.* to ownclouduser@localhost identified by 'password';
flush privileges;
exit;