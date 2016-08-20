#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move
from os import remove, chdir
import subprocess

def InstallLavernaDependenciesAptGet(logger):
    #installation here
    logger.info("Start installing git")
    pc = subprocess.Popen("apt-get -y install git".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("Start installing nodejs, npm")
    pc = subprocess.Popen("chown root npmInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("chmod +x npmInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("./npmInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)   
    logger.info("End installing laverna dependencies: git nodejs npm")

def DownloadLavernaSource(logger):
    logger.info("Start download laverna source")
    chdir("/var/www/html")
    pc = subprocess.Popen("rm -fr /var/www/html/static-laverna".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)  
    pc = subprocess.Popen("rm -fr /var/www/html/laverna".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger) 
    pc = subprocess.Popen("git clone https://github.com/Laverna/static-laverna laverna".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("chown www-data:www-data laverna".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("End download laverna source")

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('lavernaInstall',"./lavernaInstall.log")
#    filePath = path.join(SCRIPT_DIR, CONFIG_FILE_NAME) 
#   filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
#    InstallLavernaDependenciesAptGet(logger)
    DownloadLavernaSource(logger)