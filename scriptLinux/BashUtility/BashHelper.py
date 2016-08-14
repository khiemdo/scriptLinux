import logging
import sys
from shutil import move, copy
from os import path

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
    copy(filePath,path.join(backupDir, path.basename(filePath)+'.bk'))
