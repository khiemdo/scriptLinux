#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

import logging
from shutil import move, copy
from os import path, remove
import subprocess

CONFIG_FILE_NAME = "interfaces"
CONFIG_FILE_DIR = "/etc/network/"

def EditUSBIntefaceConfig(logger, filePath):
    logger.info("Start editting interface config")
    script_dir = path.dirname(__file__)
    #copy config for backup
    copy(filePath,path.join(script_dir, path.basename(filePath)+'.bk'))

    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpUsbInterface") 
    tempFhd = open(tempAbsPath,'w+')
    tempConfigStr = ""
    tempConfigStr1 = ""
    needleStr = ""
    replacedStr = ""

    lineNum = 0
    lineNumber_iface_usb0 = -1
    lineNumber_iface_next_after_usb0 = -1

    for line in originFhd:
        lineNum += 1

        #remove "auto usb0"
        needleStr = "auto usb0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)

        #remove "allow-hotplug usb0" --> will add later
        needleStr = "allow-hotplug usb0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)  
     
        #remove "iface usb0" --> will add later
        needleStr = "iface usb0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            lineNumber_iface_usb0 = lineNum
            line = line.replace(line,replacedStr)  
        
        if(lineNumber_iface_usb0 != -1 and lineNumber_iface_next_after_usb0 == -1):#found "iface usb0" AND not found next "iface"
            #find next iface after usb0
            needleStr = "iface"
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found next iface after usb0: \"{}\"".format(line.rstrip()))
                lineNumber_iface_next_after_usb0 = lineNum
        tempConfigStr+=line

    if (lineNumber_iface_next_after_usb0 == -1):
        lineNumber_iface_next_after_usb0 = lineNum
    tempConfigStr = tempConfigStr.rstrip()
    #write to file
    originFhd.close()
    
    lineNum = 0
    for line in tempConfigStr.splitlines():
        lineNum += 1
        line = line + '\n'
        if (lineNumber_iface_usb0<=lineNum and lineNum<=lineNumber_iface_next_after_usb0): #btw the 'iface usb0' and the next 'iface'
            needleStr = "address"
            replacedStr = ""
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                lineNumber_iface_usb0 = lineNum
                line = line.replace(line,replacedStr)              
            needleStr = "netmask"
            replacedStr = ""
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                lineNumber_iface_usb0 = lineNum
                line = line.replace(line,replacedStr)  
            needleStr = "network"
            replacedStr = ""
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                lineNumber_iface_usb0 = lineNum
                line = line.replace(line,replacedStr)  
            needleStr = "gateway"
            replacedStr = ""
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                lineNumber_iface_usb0 = lineNum
                line = line.replace(line,replacedStr)    
            needleStr = "broadcast"
            replacedStr = ""
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
                lineNumber_iface_usb0 = lineNum
                line = line.replace(line,replacedStr)   
        tempConfigStr1+=line      

    iface_usb0_config_string = """allow-hotplug usb0
auto usb0 
iface usb0 inet static 
    address 192.168.42.42 
    netmask 255.255.255.0 
    network 192.168.42.0
    broadcast 192.168.42.255
"""
    tempConfigStr1+=iface_usb0_config_string   

    #remove empty newline
    lineNum = 0
    for line in tempConfigStr1.splitlines():
        lineNum += 1
        line = line+'\n'
        if(line == '\n'):
            line = ""
        tempFhd.write(line);
  
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End editting interface config")

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('usbConfigMod',"./usbConfigMod.log")

    filePath = path.join(SCRIPT_DIR, CONFIG_FILE_NAME) 
#   filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    EditUSBIntefaceConfig(logger,filePath)