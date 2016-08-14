#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move, copy
from os import remove
import subprocess

DHCP_CONFIG_FILE_PATH = "/etc/dhcp/dhcpd.conf"
ISC_DHCP_SERVER_CONFIG_FILE_PATH = "/etc/default/isc-dhcp-server"
INTERFACES_CONFIG_FILE_PATH = "/etc/network/interfaces"
HOSTAPD_CONFIG_FILE_PATH = "/etc/hostapd/hostapd.conf"
HOSTAPD_DEFAULT_FILE_PATH = "/etc/default/hostapd"
SYSCTL_CONF_PATH = "/etc/sysctl.conf"
SSID = 'fnick2812PI'
WPA_PASSPHASE = 'default1234'

def InstallWifiAccessPointPkgs(logger):
    #installation here
    logger.info("Start installing WifiAccessPointPkgs")
    pc = subprocess.Popen("apt-get install isc-dhcp-server hostapd".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

def EditDhcpConfig(logger, filePath,templatePath):
    logger.info("Start installing dhcp config")
    if(path.isfile(filePath)):
        remove(filePath)
    if(path.isfile(templatePath) is False):
        raise Exception('templatePath is not valid')
    copy(templatePath,filePath)
    logger.info("End installing dhcp config")
def EditIscDhcpServerConfig(logger, filePath):
    logger.info("Start installing IscDhcpServer config")
    originFhd = 0
    try:
        originFhd = open(filePath,'r+')
    except OSError as err:
        logger.info("No existed {}".format(filePath))
        originFhd = open(filePath,'w+')
        pass
    tmpFileName = filePath+BashHelper.GenerateRandomCharSets(5)
    tempAbsPath = path.join(SCRIPT_DIR, tmpFileName) 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass 
    tempFhd = open(tempAbsPath,'w+')
    lineNum = 0
    needleStr = ""
    replacedStr = ""

    for line in originFhd:
        lineNum += 1
        #Change domain-name,domain-name-servers
        needleStr = 'INTERFACES='
        replacedStr = 'INTERFACES="wlan0"\n'
        ret = line.find(needleStr)
        if(ret!=-1):
            if(ret == 0 or ret == 1):
                logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
                line = line.replace(line,replacedStr)#todo  
        tempFhd.write(line)      

    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End installing IscDhcpServer config")
def EditInterfacesConfig(logger, filePath):
    logger.info("Start installing interfaces config")
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
    lineNumber_iface_wlan0 = -1
    lineNumber_iface_next_after_wlan0 = -1    

    #skim through the file to look for the line number that has wlan0 iface
    for line in originFhd:
        lineNum += 1

        #remove "auto wlan0"
        needleStr = "auto wlan0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)

        #remove "up iptables-restore < /etc/iptables.ipv4.nat"
        needleStr = "iptables-restore"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)

        #remove "allow-hotplug wlan0" --> will add later
        needleStr = "allow-hotplug wlan0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            line = line.replace(line,replacedStr)  
     
        #remove "iface wlan0" --> will add later
        needleStr = "iface wlan0"
        replacedStr = "\n"
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))
            lineNumber_iface_wlan0 = lineNum
            line = line.replace(line,replacedStr)  
        
        if(lineNumber_iface_wlan0 != -1 and lineNumber_iface_next_after_wlan0 == -1):#found "iface wlan0" AND not found next "iface"
            #find next iface after wlan0
            needleStr = "iface"
            ret = line.find(needleStr)
            if(ret != -1):
                logger.info("Found next iface after wlan0: \"{}\"".format(line.rstrip()))
                lineNumber_iface_next_after_wlan0 = lineNum
        tempConfigStr+=line
    
    if (lineNumber_iface_next_after_wlan0 == -1):
        lineNumber_iface_next_after_wlan0 = lineNum
    tempConfigStr = tempConfigStr.rstrip()
    originFhd.close()

    lineNum = 0
    #loop through btw iface wlan0 and the next iface to remove all the line
    for line in tempConfigStr.splitlines():
        lineNum += 1
        if (lineNumber_iface_wlan0<=lineNum and lineNum<=lineNumber_iface_next_after_wlan0):
            pass
        else:
            line = line + '\n'
            tempConfigStr1+=line   

    iface_wlan0_config_string = """allow-hotplug wlan0
iface wlan0 inet static  
    address 172.10.10.1
    netmask 255.255.255.0
    network 172.10.10.0
    broadcast 172.10.10.255
up iptables-restore < /etc/iptables.ipv4.nat
"""
    tempConfigStr1+=iface_wlan0_config_string   
    #remove empty newline
    lineNum = 0
    for line in tempConfigStr1.splitlines():
        lineNum += 1
        if(line != '\n'):
            line = line+'\n'
            tempFhd.write(line);

    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)

    logger.info("End installing interfaces config")
def EditHostApdConfig(logger, filePath):
    logger.info("Start installing HostApd config")
    hostapd_configuration_string = """
interface=wlan0
driver=nl80211
hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=1
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
"""
    tmpFileName = filePath+BashHelper.GenerateRandomCharSets(5)
    tempAbsPath = path.join(SCRIPT_DIR, tmpFileName) 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass 
    tempFhd = open(tempAbsPath,'w+')
    tempFhd.write(hostapd_configuration_string)
    tempFhd.write('ssid='+SSID+'\n')
    tempFhd.write('wpa_passphrase='+WPA_PASSPHASE+'\n')
    tempFhd.close() 
    if (path.isfile(filePath)):
        ret = remove(filePath)  
    
    move(tempAbsPath,filePath) 
    logger.info("End installing HostApd config")
def EditHostApdDefault(logger, filePath):
    logger.info("Start installing HostApd Defautl")
    originFhd = 0
    try:
        originFhd = open(filePath,'r+')
    except OSError as err:
        logger.info("No existed {}".format(filePath))
        originFhd = open(filePath,'w+')
        pass

    tmpFileName = filePath+BashHelper.GenerateRandomCharSets(5)
    tempAbsPath = path.join(SCRIPT_DIR, tmpFileName) 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass
    tempFhd = open(tempAbsPath,'w+')

    lineNum = 0
    for line in originFhd:
        lineNum += 1
        #Change domain-name,domain-name-servers
        needleStr = 'DAEMON_CONF='
        replacedStr = 'DAEMON_CONF="/etc/hostapd/hostapd.conf"\n'
        ret = line.find(needleStr)
        if(ret == 0 or (ret ==1 and line[0] == '#')):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)#todo 
        tempFhd.write(line)      

    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("Ending installing HostApd Defautl")
def EditSysctlConfig(logger, filePath):
    logger.info("Start installing Sysctl config")
    originFhd = 0
    try:
        originFhd = open(filePath,'r+')
    except OSError as err:
        logger.info("No existed {}".format(filePath))
        originFhd = open(filePath,'w+')
        pass

    tmpFileName = filePath+BashHelper.GenerateRandomCharSets(5)
    tempAbsPath = path.join(SCRIPT_DIR, tmpFileName) 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass
    tempFhd = open(tempAbsPath,'w+')

    lineNum = 0
    needleStr = ""
    replacedStr = ""

    for line in originFhd:
        lineNum += 1
        #Change anonymous_enable=YES to anonymous_enable=NO,
        needleStr = "net.ipv4.ip_forward"
        replacedStr=""
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)

    logger.info("add net.ipv4.ip_forward=1")
    tempFhd.write("net.ipv4.ip_forward=1")
    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End installing Sysctl config")
def EditIp4_forward(logger,iptableOutput, filePath):
    needleStr = '-A POSTROUTING -o eth0 -j MASQUERADE'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
        pc = subprocess.Popen('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE'.split(),stdout = subprocess.PIPE)

    needleStr = '-A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
        pc = subprocess.Popen('iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split(),stdout = subprocess.PIPE)

    needleStr = '-A FORWARD -i wlan0 -o eth0 -j ACCEPT'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT')
        pc = subprocess.Popen('iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT'.split(),stdout = subprocess.PIPE)

    ###########################
    needleStr = '-A POSTROUTING -o wlan1 -j MASQUERADE'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE')
        pc = subprocess.Popen('iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE'.split(),stdout = subprocess.PIPE)

    needleStr = '-A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
        pc = subprocess.Popen('iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split(),stdout = subprocess.PIPE)

    needleStr = '-A FORWARD -i wlan0 -o wlan1 -j ACCEPT'
    ret = iptableOutput.find(needleStr)
    if(ret==-1):
        logger.info('iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT')
        pc = subprocess.Popen('iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT'.split(),stdout = subprocess.PIPE)

    if(path.isfile(filePath)):
        remove(filePath)
    originFhd = open(filePath,'w+')
    logger.info('iptables-save')
    pc = subprocess.Popen('iptables-save',stdout = subprocess.PIPE)
    for line in pc.stdout:  
        logger.info(line.rstrip())  
        originFhd.write(line)
    originFhd.close()


if __name__ == "__main__":
    logger = BashHelper.SetupLogger('wifiAPConfig',"./wifiAPConfig.log")
    InstallWifiAccessPointPkgs(logger)

    filePath=DHCP_CONFIG_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditDhcpConfig(logger,filePath,path.join(SCRIPT_DIR,'dhcpd.conf.template'))

    filePath=ISC_DHCP_SERVER_CONFIG_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditIscDhcpServerConfig(logger,filePath)

    filePath=INTERFACES_CONFIG_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditInterfacesConfig(logger,filePath)

    filePath=HOSTAPD_CONFIG_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditHostApdConfig(logger,filePath)

    filePath=HOSTAPD_DEFAULT_FILE_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditHostApdDefault(logger,filePath)

    filePath=SYSCTL_CONF_PATH
    BashHelper.BackupFileBfMod(filePath,SCRIPT_DIR,logger)
    BashHelper.StripAllCommentsFromScript(filePath)
    BashHelper.StripBlankLineFromScript(filePath)
    EditSysctlConfig(logger,filePath)

    logger.info('echo 1 > /proc/sys/net/ipv4/ip_forward')
    pc = subprocess.Popen('echo 1 > /proc/sys/net/ipv4/ip_forward'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    logger.info('iptables-save')
    pc = subprocess.Popen('iptables-save',stdout = subprocess.PIPE)

    iptableOutput = "";
    for line in pc.stdout:  
        logger.info(line.rstrip())  
        iptableOutput=iptableOutput+line
    EditIp4_forward(logger,iptableOutput,'/etc/iptables.ipv4.nat')
    logger.info('service hostapd start')
    pc = subprocess.Popen('service hostapd start'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('service isc-dhcp-server start')
    pc = subprocess.Popen('service isc-dhcp-server start'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
