#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess

def RunSeafileInstallMysqlScript(logger):
    #installation here
    logger.info("Run seafileInstall.sh")
    pc = subprocess.Popen("chown root:root ./seafileInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("chmod 777 ./seafileInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("/bin/bash ./seafileInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

def AddSeafileNginx(logger,filePath,destFilePath, lnFilePath):
    logger.info("Start AddApacheVirtualServer")

    cmdStr = "rm -rf " + destFilePath
    logger.info("exec {}".format(cmdStr))
    pc = subprocess.Popen(cmdStr.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    copy(filePath, destFilePath)

    cmdStr = "rm -rf " + lnFilePath
    logger.info("exec {}".format(cmdStr))
    pc = subprocess.Popen(cmdStr.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    cmdStr = "ln -s " + destFilePath + " " + lnFilePath
    logger.info("exec {}".format(cmdStr))
    pc = subprocess.Popen(cmdStr.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info("End AddApacheVirtualServer")

    logger.info("End AddApacheVirtualServer")

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('seafileInstall',"./seafileInstall.log")
    RunSeafileInstallMysqlScript(logger)
    AddSeafileNginx(logger,"./seafile","/etc/apache2/sites-available/seafile","/etc/apache2/sites-enabled/seafile")