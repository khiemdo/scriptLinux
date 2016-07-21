#!/usr/bin/python
import logging
from shutil import move
from os import path, remove
import subprocess

CONFIG_FILE_NAME = "interfaces"
CONFIG_FILE_DIR = "/etc/network/"

def SetupUSBInterfaceLogger(fileName,fileDirName):
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
def EditUSBIntefaceConfig(logger):
    logger.info("Start editting interface config")
    originFhd = open(filePath,'r+')
    script_dir = path.dirname(__file__)
    tempAbsPath = path.join(script_dir, "tmpUsbInterface") 
    tempFhd = open(tempAbsPath,'w+')
    lineNum = 0
    needleStr = ""
    for line in originFhd:
        lineNum += 1
        needleStr = "usb0"
    logger.info("End editting interface config")

if __name__ == "__main__":
    logger = SetupUSBInterfaceLogger('usbConfigMod',"./usbConfigMod.log")

    script_dir = path.dirname(__file__)
    filePath = path.join(script_dir, CONFIG_FILE_NAME) 
#   filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    EditUSBIntefaceConfig(logger,filePath)