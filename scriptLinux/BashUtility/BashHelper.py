import logging

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
        if(line.find("error")!=-1):
            logger.error("Error when installing vsftpd")
            sys.exit()

def BackupFileBfMod(filePath,logger):
    copy(filePath,path.join(script_dir, path.basename(filePath)+'.bk'))
