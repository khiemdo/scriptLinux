import accessPointSetup
from os import path
import sys
from BashUtility import BashHelper
from shutil import move, copy

SCRIPT_DIR = path.dirname(__file__)

CONFIG_FILE_NAME = "dhcpd.conf"

def TestStripAllCommentsFromScript(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
def TestEditDhcpConfig(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    accessPointSetup.EditDhcpConfig(logger,filePath,path.join(SCRIPT_DIR,'dhcpd.conf.template'))

def TestEditIscDhcpServerConfig(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    accessPointSetup.EditIscDhcpServerConfig(logger,filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
def TestEditInterfacesConfig(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    accessPointSetup.EditInterfacesConfig(logger,filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
def TestEditHostApdConfig(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    accessPointSetup.EditHostApdConfig(logger,filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
def TestEditHostApdDefault(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    accessPointSetup.EditHostApdDefault(logger,filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
def TestEditSysctlConfig(logger, fileName):
    filePath = path.join(SCRIPT_DIR, fileName) 
    if(path.isfile(filePath+'.bk')):
        copy(filePath+'.bk',filePath)
    accessPointSetup.EditSysctlConfig(logger,filePath)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)

if __name__ == "__main__":
    logger = BashHelper.SetupLogger('testWifiAPConfig',"./testWifiAPConfig.log")
    TestEditDhcpConfig(logger, "dhcpd.conf")
#    TestStripAllCommentsFromScript(logger,"dhcpd.conf")
#    TestEditIscDhcpServerConfig(logger, "isc-dhcp-server")
#    TestEditInterfacesConfig(logger, "interfaces")
#    TestEditHostApdConfig(logger, "hostapd.conf")
#    TestEditHostApdDefault(logger, "hostapd")
#    TestEditSysctlConfig(logger, "sysctl.conf")