#!/usr/bin/python
import phpmyadminInstall
from os import path
import sys
from BashUtility import BashHelper
from shutil import move, copy

SCRIPT_DIR = path.dirname(__file__)

def TestEditApachePortConf(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    phpmyadminInstall.EditApachePortConf(logger,filePath)

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('TestPhpMyAdminInstall',"./TestPhpMyAdminInstall.log")
    TestEditApachePortConf(logger, "ports.conf")
