#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess

MYSQL_PASSWORD='root'


def InstallMySQLPython(logger):
    logger.info("Install PexpectPython")
    pc = subprocess.Popen("pip install MySQL-python".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
def GenerateOpenSSLPExpect(logger, country, state,city,organization,orgUnit,name,email, nameKey, nameCrt):
    logger.info("Start GenerateOpenSSLPExpect")
    import pexpect
    logger.info('exec: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout '+ nameKey+ ' -out ' + nameCrt)
    child = pexpect.spawn('openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout '+ nameKey+ ' -out ' + nameCrt)
    child.logfile = sys.stdout
    child.expect ('Country Name (2 letter code) [AU]:')
    child.sendline (country)
    child.expect ('State or Province Name (full name) [Some-State]:')
    child.sendline (state)
    child.expect ('Locality Name (eg, city) []:')
    child.sendline (city)
    child.expect ('Organization Name (eg, company) [Internet Widgits Pty Ltd]:')
    child.sendline (organization)
    child.expect ('Organizational Unit Name (eg, section) []:')
    child.sendline (orgUnit)
    child.expect ('Common Name (e.g. server FQDN or YOUR name) []:')
    child.sendline (name)
    child.expect ('Email Address []:')
    child.sendline (email)

    child.expect(pexpect.EOF)
    logger.info("End GenerateOpenSSLPExpect")
def RunBashScript(logger, scriptPath):
    logger.info("chown root "+scriptPath)
    pc = subprocess.Popen(("chown root "+scriptPath).split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger) 
    logger.info("chmod +x "+scriptPath)
    pc = subprocess.Popen(("chmod +x "+scriptPath).split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("exe: "+scriptPath)
    pc = subprocess.Popen(scriptPath.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
def RunOwncloudSQL(logger, database,sqlScriptPath):
    cursor = database.cursor()
    for line in open(sqlFilePath):
        cursor.execute(line)
if __name__ == "__main__":
    logger = BashHelper.SetupLogger('owncloudInstall',"./owncloudInstall.log")

    pc = subprocess.Popen("apt-get install -y git wget nano elinks nginx".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("apt-get install -y php5-fpm php5-mysql openssl ssl-cert php5-cli php5-common php5-cgi php-pear php-apc curl libapr1 libtool php5-curl libcurl4-openssl-dev php-xml-parser php5-dev php5-gd libmemcached* memcached php5-memcached".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    GenerateOpenSSLPExpect(logger,'sg','singapore','singapore','fnick2812','fnick2812','fnick2812','fnick2812@local.com','owncloud.key','owncloud.crt')
    pc = subprocess.Popen("mkdir -p /etc/nginx/ssl".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    copy('owncloud.key','/etc/nginx/ssl/owncloud.key')
    copy('owncloud.crt','/etc/nginx/ssl/owncloud.crt')

    db = MySQLdb.connect(host="localhost",user="root",passwd="root")

    RunOwncloudSQL(logger,db,"owncloud.sql")
    RunBashScript(logger,"./owncloudInstall.sh")

    pc = subprocess.Popen("service mysql restart".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("service php5-fpm restart".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("service nginx restart".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)



