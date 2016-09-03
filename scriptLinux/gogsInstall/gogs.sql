DROP DATABASE IF EXISTS gogs;
CREATE DATABASE IF NOT EXISTS gogs CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

DROP DATABASE IF EXISTS owncloud;
CREATE DATABASE IF NOT EXISTS owncloud;
grant all privileges on owncloud.* to ownclouduser@localhost identified by 'defaultPassword';
flush privileges;