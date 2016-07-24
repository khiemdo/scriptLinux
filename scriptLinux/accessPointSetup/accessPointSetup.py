#!/usr/bin/python
from os import path
import sys
SCRIPT_DIR = path.dirname(__file__)
sys.path.append(path.join(SCRIPT_DIR,'..'))
from BashUtility import BashHelper

from shutil import move
from os import remove
import subprocess

DHCP_CONFIG_FILE_PATH = "/etc/dhcp/dhcpd.conf"
ISC_DHCP_SERVER_CONFIG_FILE_PATH = "/etc/default/isc-dhcp-server"
HOSTAPD_CONFIG_FILE_PATH = "/etc/hostapd/hostapd.conf"
HOSTAPD_DEFAULT_FILE_PATH = "/etc/default/hostapd"
INTERFACES_CONFIG_FILE_PATH = "/etc/network/interfaces"

def InstallWifiAccessPointPkgs(logger):
    #installation here
    logger.info("Start installing WifiAccessPointPkgs")
    pc = subprocess.Popen("apt-get install isc-dhcp-server hostapd")
    BashHelper.CheckOutputOfCallingBash(pc,logger)

def EditDhcpConfig(logger, filePath):
    logger.info("Start installing dhcp config")
    BashHelper.BackupFileBfMod(filePath,logger)

    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass  
    tempFhd = open(tempAbsPath,'w+')
    lineNum = 0
    needleStr = ""
    replacedStr = ""

    subnet_string_dhcp_config = """subnet 192.168.42.0 netmask 255.255.255.0 {
	range 192.168.42.10 192.168.42.50;
	option broadcast-address 192.168.42.255;
	option routers 192.168.42.1;
	default-lease-time 600;
	max-lease-time 7200;
	option domain-name "local";
	option domain-name-servers 8.8.8.8, 8.8.4.4;
}"""
    subnet_string_dhcp_config_flag = 0
    for line in originFhd:
        lineNum += 1
        #Change domain-name,domain-name-servers
        needleStr = 'option domain-name "example.org";'
        replacedStr='#option domain-name "example.org";\n'
        ret = line.find(needleStr)
        if(ret == 0):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)
        elif(ret != 1 or line[0] != '#'):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)

        needleStr = 'option domain-name-servers ns1.example.org, ns2.example.org;'
        replacedStr='#option domain-name-servers ns1.example.org, ns2.example.org;'
        ret = line.find(needleStr)
        if(ret == 0):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)
        elif(ret != 1 or line[0] != '#'):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)
    
        needleStr = 'authoritative;\n'
        replacedStr='authoritative;\n'
        ret = line.find(needleStr)
        if(ret == 1 and line[0]=='#'):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)
        tempFhd.write(line)      

        needleStr = subnet_string_dhcp_config
        ret = line.find(needleStr)
        if(ret != -1):
            logger.info("Found {} at line {}: \"{}\"".format(needleStr.strip(),lineNum,line.rstrip()))
            subnet_string_dhcp_config_flag=1

    if(subnet_string_dhcp_config_flag == 0):
        tempFhd.write(subnet_string_dhcp_config)   
    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End installing dhcp config")
def EditIscDhcpServerConfig(logger, filePath):
    logger.info("Start installing IscDhcpServer config")
    BashHelper.BackupFileBfMod(filePath)

    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
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
        if(ret == 0 or ret == 1):
            logger.info("Found {} at line {}: \"{}\"-->\"{}\"".format(needleStr.strip(),lineNum,line.rstrip(),replacedStr.rstrip()))#todo
            line = line.replace(line,replacedStr)#todo  
        tempFhd.write(line)      

    originFhd.close()
    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)
    logger.info("End installing IscDhcpServer config")
def EditHostApdConfig(logger, filePath):
    logger.info("Start installing HostApd config")
    hostapd_configuration_string = """
# This is the name of the WiFi interface we configured above
interface=wlan0
# Use the nl80211 driver with the brcmfmac driver
driver=nl80211
# This is the name of the network
ssid=PiTester-AP
# Use the 2.4GHz band
hw_mode=g
# Use channel 6
channel=6
# Enable 802.11n
ieee80211n=1
# Enable WMM
wmm_enabled=1
# Enable 40MHz channels with 20ns guard interval
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
# Accept all MAC addresses
macaddr_acl=0
# Use WPA authentication
auth_algs=1
# Require clients to know the network name
ignore_broadcast_ssid=0
# Use WPA2
wpa=2
# Use a pre-shared key
wpa_key_mgmt=WPA-PSK
# The network passphrase
wpa_passphrase=default
# Use AES, instead of TKIP
rsn_pairwise=CCMP
"""

    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass 
    tempFhd = open(tempAbsPath,'w+')
    tempFhd.write(hostapd_configuration_string) 
    ret = remove(filePath)  
    move(tempAbsPath,filePath) 
    logger.info("End installing HostApd config")
def EditHostApdDefault(logger, filePath):
    logger.info("Start installing HostApd Defautl")
    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpVsftpd") 
    try:
        ret = remove(tempAbsPath)  
    except OSError as err:
        logger.info("No existed tempFile in the current folder")
        pass
    tempFhd = open(tempAbsPath,'w+')

    
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

def EditInterfacesConfig(logger, filePath):
    logger.info("Start installing interfaces config")

    logger.info("End installing interfaces config")
def EditSysctlConfig(logger, filePath):
    logger.info("Start installing Sysctl config")

    logger.info("End installing Sysctl config")


if __name__ == "__main__":
    logger = BashHelper.SetupLogger('wifiAPConfig',"./wifiAPConfig.log")
#    filePath = path.join(SCRIPT_DIR, CONFIG_FILE_NAME) 
    filePath = CONFIG_FILE_DIR + CONFIG_FILE_NAME
    InstallWifiAccessPointPkgs(logger)
#    EditDhcpConfig(logger,DHCP_CONFIG_FILE_PATH)
#    EditIscDhcpServerConfig(logger,ISC_DHCP_SERVER_CONFIG_FILE_PATH)
#    EditHostApdConfig(logger,HOSTAPD_CONFIG_FILE_PATH)
#    EditHostApdDefault(logger,HOSTAPD_DEFAULT_FILE_PATH)
#    EditInterfacesConfig(logger,INTERFACES_CONFIG_FILE_PATH)