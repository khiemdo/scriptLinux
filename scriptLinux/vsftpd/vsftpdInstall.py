#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

import logging
from shutil import move, copy
from os import remove
import subprocess

CONFIG_FILE_NAME = "vsftpd.conf"
CONFIG_FILE_DIR = "/etc/"

vsftpdConfigPath = ""

def InstallVsfptd(logger):
    #installation here
    logger.info("Start installing vsftpd")
    
    pc = subprocess.Popen("apt-get -y install vsftpd".split(),stdout = subprocess.PIPE)#todo
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    #backup vsftpd.conf
    logger.info("Backup vsftpd.conf")
    pc = subprocess.check_call("cp /etc/vsftpd.conf ./vsftpd.conf.bk".split());
    logger.info("End installing vsftpd")

def EditVsftpdConfig(logger,filePath):
    logger.info("Start editting vsftpd config")
    originFhd = open(filePath,'r+')
    #tempFile, tempAbsPath = mkstemp()

    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
    tempFhd = open(tempAbsPath,'w+')
    lineNum = 0
    needleStr = ""
    replacedStr = ""#todo

    force_dot_files_Flag = 0

    for line in originFhd:
        lineNum += 1
        #Change anonymous_enable=YES to anonymous_enable=NO,
        needleStr = "anonymous_enable"
        replacedStr="anonymous_enable=NO\n"#todo
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)#todo
        #Uncomment local_enable=YES
        needleStr = "local_enable=YES"
        replacedStr="#local_enable=YES\n"
        line_output = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)
        #Uncomment local_enable=YES
        needleStr = "write_enable=YES"
        replacedStr="#write_enable=YES\n"#todo
        ret = line.find(needleStr)
        if(ret == 0):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)
        elif (line[0] == '#' and ret == 1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)
        #Uncomment force_dot_files=YES\n
        needleStr = "force_dot_files"
        replacedStr="force_dot_files=YES\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)
            force_dot_files_Flag = 1
        tempFhd.write(line)  

    if(force_dot_files_Flag == 0):
        logger.info("add force_dot_files")
        tempFhd.write("force_dot_files=YES\n")
    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End editting vsftpd config")


if __name__ == "__main__":
    logger = BashHelper.SetupLogger('vsftpdInstall',"./vsftpdInstall.log")
#    filePath = path.join(SCRIPT_DIR, CONFIG_FILE_NAME) 
    filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    InstallVsfptd(logger)
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    EditVsftpdConfig(logger,filePath)