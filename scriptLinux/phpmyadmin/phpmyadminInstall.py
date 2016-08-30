#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess

APACHE_PORT_CONFIG_FILE_PATH = "/etc/apache2/ports.conf"
REPLACEMENT_OF_DEFAULT_SSL_PORT="1443"
REPLACEMENT_OF_DEFAULT_SHTTP_PORT="1080"

def RunPhpMyAdminInstallScript(logger):
    #installation here
    logger.info("Run phpmyadminInstall.sh")
    pc = subprocess.Popen("chown root:root ./phpmyadminInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("chmod 777 ./phpmyadminInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("/bin/bash ./phpmyadminInstall.sh".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
def EditApachePortConf(logger, filePath):
    logger.info("Start EditApachePortConf")
    originFhd = open(filePath,'r+')
    tmpFileName = filePath+BashHelper.GenerateRandomCharSets(5)
    tempAbsPath = path.join(SCRIPT_DIR, tmpFileName) 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        pass  

    tempFhd = open(tempAbsPath,'w+')
    tempConfigStr = ""
    tempConfigStr1 = ""
    needleStr = ""
    replacedStr = ""

    lineNum = 0
    lineIfStart = 0
    lineIfEnd = 0

    for line in originFhd:
        tempConfigStr+=line

    for line in tempConfigStr.splitlines():
        lineNum += 1
        needleStr = "<IfModule ssl_module>"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            lineIfStart = lineNum

        needleStr = "</IfModule>"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            lineIfEnd = lineNum
            break;

            
    lineNum = 0
    for line in tempConfigStr.splitlines():
        lineNum += 1
        if(lineNum>lineIfStart and lineNum<lineIfEnd):
            needleStr = "Listen"
            replacedStr = "\tListen " + REPLACEMENT_OF_DEFAULT_SSL_PORT
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                line = line.replace(line,replacedStr)
        line = line + '\n'
        tempConfigStr1+=line
    tempConfigStr = tempConfigStr1
    tempConfigStr1 = ""



    for line in tempConfigStr.splitlines():
        lineNum += 1
        needleStr = "<IfModule mod_gnutls.c>"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            lineIfStart = lineNum

        needleStr = "</IfModule>"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            lineIfEnd = lineNum
            break;

    lineNum = 0
    for line in tempConfigStr.splitlines():
        lineNum += 1
        if(lineNum>lineIfStart and lineNum<lineIfEnd):
            needleStr = "Listen"
            replacedStr = "\tListen " + REPLACEMENT_OF_DEFAULT_SSL_PORT
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                line = line.replace(line,replacedStr)
        line = line + '\n'
        tempConfigStr1+=line
    tempConfigStr = tempConfigStr1
    tempConfigStr1 = ""

    lineNum = 0
    replaceFlag = 1
    for line in tempConfigStr.splitlines():
        lineNum += 1
        if(replaceFlag>0):
            needleStr = "Listen"
            replacedStr = "\tListen " + REPLACEMENT_OF_DEFAULT_SHTTP_PORT
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                line = line.replace(line,replacedStr)
                replaceFlag-=1

        line = line + '\n'
        tempConfigStr1+=line
    tempConfigStr = tempConfigStr1
    tempConfigStr1 = ""

    tempFhd.write(tempConfigStr)
    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)

    logger.info("End EditApachePortConf")
def AddApacheVirtualServer(logger,filePath,destFilePath, lnFilePath):
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

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('phpmyadminnstall',"./phpmyadminnstall.log")
    RunPhpMyAdminInstallScript(logger)

    pc = subprocess.Popen("rm /etc/apache2/sites-available/*default*".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    filePath=APACHE_PORT_CONFIG_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditApachePortConf(logger,filePath)

    pc = subprocess.Popen("cp /etc/apache2/sites-available/000-default.conf .".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("rm -rf /etc/apache2/sites-available/000-default.conf".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("cp /etc/apache2/sites-enabled/default-ssl.conf .".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    pc = subprocess.Popen("rm -rf /etc/apache2/sites-enabled/default-ssl.conf".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    AddApacheVirtualServer(logger,"./phpmyadmin","/etc/apache2/sites-available/phpmyadmin","/etc/apache2/sites-enabled/phpmyadmin")
