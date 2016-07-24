#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move
from os import remove
import subprocess

def InstallLavernaDependenciesAptGet(logger):
    #installation here
    logger.info("Start installing laverna dependencies: git nodejs npm")
    pc = subprocess.Popen("apt-get -y install git nodejs npm".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("End installing laverna dependencies: git nodejs npm")

def DownloadLavernaSource(logger):
    logger.info("Start download laverna source")
    pc = subprocess.Popen("cd /var/www".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("git clone http://github.com/laverna/laverna.git".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("End download laverna source")

def InstallLavernaDependenciesNpm(logger):
    logger.info("Start installing laverna dependencies of npm")
    logger.info("Exe \"cd /var/www/laverna\"")
    pc = subprocess.Popen("cd /var/www/laverna".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("Installing laverna dependencies of npm: bower, grunt, grunt-cli")
    pc = subprocess.Popen("npm install bower".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("npm install grunt".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("npm install grunt-cli".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("Install Laverna’s dependencies")
    pc = subprocess.Popen("npm install --allow-root".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("End installing laverna dependencies of npm")


if __name__ == "__main__":
    logger = BashHelper.SetupLogger('lavernaInstall',"./lavernaInstall.log")
#    filePath = path.join(SCRIPT_DIR, CONFIG_FILE_NAME) 
#   filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    InstallLavernaDependenciesAptGet(logger)
#    DownloadLavernaSource(logger)
#    InstallLavernaDependenciesNpm(logger)