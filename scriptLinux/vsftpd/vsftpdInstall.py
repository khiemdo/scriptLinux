#!/usr/bin/python
import logging
from shutil import move
from os import path, remove
import subprocess

CONFIG_FILE_NAME = "vsftpd.conf"
CONFIG_FILE_DIR = "/etc/"

vsftpdConfigPath = ""
def SetupVsftpdLogger(fileName,fileDirName):
    logger = logging.getLogger(fileName)
    logger.setLevel(logging.DEBUG)

    logConsoleHd = logging.StreamHandler()
    logConsoleHd.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logConsoleHd.setFormatter(formatter)
    logger.addHandler(logConsoleHd)

    logFileHd = logging.FileHandler(fileDirName)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFileHd.setFormatter(formatter)
    logger.addHandler(logFileHd)
    return logger

def InstallVsfptd(logger):
    #installation here
    logger.info("Start installing vsftpd")
    ret = subprocess.call("apt-get install vsftpd")
    if(ret.find("error")!=-1):
        logger.error("Error when installing vsftpd")
    logger.info("End installing vsftpd")

def EditVsftpdConfig(logger,filePath):
    logger.info("Start editting vsftpd config")
    originFhd = open(filePath,'r+')
    #tempFile, tempAbsPath = mkstemp()
    script_dir = path.dirname(__file__)
    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
    tempFhd = open(tempAbsPath,'w+')
    lineNum = 0
    needleStr = ""

    force_dot_files_Flag = 0
    for line in originFhd:
        lineNum += 1
        #Change anonymous_enable=YES to anonymous_enable=NO,
        needleStr = "anonymous_enable"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            ret = line.replace(line,"anonymous_enable=NO\n")
        #Uncomment local_enable=YES
        needleStr = "local_enable=YES"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            ret = line.replace(line,"#local_enable=YES\n")
        #Uncomment local_enable=YES
        needleStr = "write_enable=YES"
        ret = line.find(needleStr)
        if(ret == 0):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            ret = line.replace(line,"#write_enable=YES\n")
        elif (line[0] == '#' and ret == 1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            ret = line.replace(line,"#write_enable=YES\n")
        #Uncomment force_dot_files=YES\n
        needleStr = "force_dot_files"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            ret = line.replace(line,"force_dot_files=YES\n")
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
    logger = SetupVsftpdLogger('vsftpdInstall',"./vsftpdInstall.log")

#    script_dir = path.dirname(__file__)
#    filePath = path.join(script_dir, CONFIG_FILE_NAME) 

    filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    #InstallVsfptd(logger)
    EditVsftpdConfig(logger,filePath)