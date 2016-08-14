import logging
import sys
from shutil import move, copy
from os import remove
from os import path
import string
import random

def SetupLogger(fileName,fileDirName):
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
def CheckOutputOfCallingBash(process, logger):
    for line in process.stdout:
        logger.info(line.rstrip())
def BackupFileBfMod(filePath,backupDir,logger):
    if(path.isfile(filePath)):
        copy(filePath,path.join(backupDir, path.basename(filePath)+'.bk'))

def GenerateRandomCharSets(numChars):
    return ''.join(random.choice(string.ascii_letters) for x in range(numChars))

def StripAllCommentsFromScript(filePath):
    if(path.isfile(filePath)):
        originFhd = open(filePath,'r+')
    else:
        originFhd = open(filePath,'w+')
    
    tmpFileName = filePath+GenerateRandomCharSets(5)
    try:
        ret = remove(tmpFileName)  
    except OSError as err:
        pass  
    tempFhd = open(tmpFileName,'w+')
    lineNum = 0
    needleStr = "" 

    for line in originFhd:
        lineNum += 1
        needleStr = '#'
        ret = line.find(needleStr)
        if(ret != 0):
            tempFhd.write(line)  
        
    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tmpFileName,filePath) 

def StripBlankLineFromScript(filePath):
    if(path.isfile(filePath)):
        originFhd = open(filePath,'r+')
    else:
        originFhd = open(filePath,'w+')
    tmpFileName = filePath+GenerateRandomCharSets(5)
    try:
        ret = remove(tmpFileName)  
    except OSError as err:
        pass  
    tempFhd = open(tmpFileName,'w+')
    lineNum = 0
    needleStr = "" 

    for line in originFhd:
        lineNum += 1
        line = line.rstrip()
        if(line != ''):
            tempFhd.write(line+'\n')  

    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tmpFileName,filePath) 
