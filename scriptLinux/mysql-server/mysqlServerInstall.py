#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess
ROOT_MYSQL_PASSWD='root'

def InstallPip(logger):
    logger.info("Install pip")
    pc = subprocess.Popen("apt-get -y install python-pip".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
def InstallPexpectPython(logger):
    logger.info("Install PexpectPython")
    pc = subprocess.Popen("pip install pexpect".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
def InstallMySqlServerUsingPExpect(logger, password):
    logger.info("Start InstallMySqlServerUsingPExpect")
    import pexpect
    child = pexpect.spawn('apt-get -y install mysql-server')
    child.logfile = sys.stdout
    child.expect ('New password for the MySQL "root" user:')
    child.sendline (password)
    child.expect ('Repeat password for the MySQL "root" user:')
    child.sendline (password)
    child.expect(pexpect.EOF)
    logger.info("End InstallMySqlServerUsingPExpect")

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('mysqlserver',"./mysqlserver.log")
    InstallPip(logger)
    InstallPexpectPython(logger)
    InstallMySqlServerUsingPExpect(logger,ROOT_MYSQL_PASSWD)