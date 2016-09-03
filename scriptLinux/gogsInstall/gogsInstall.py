#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess

ROOT_MYSQL_PASSWD='root'

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('gogsInstall',"./gogsInstall.log")

    import MySQLdb
    db = MySQLdb.connect(host="localhost",user="root",passwd=ROOT_MYSQL_PASSWD)
    filePath = path.join(SCRIPT_DIR, 'gogs.sql')
    BashHelper.RunSQLScript(logger,db,filePath)