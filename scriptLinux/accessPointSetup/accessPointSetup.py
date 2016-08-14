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
INTERFACES_CONFIG_FILE_PATH = "/etc/network/interfaces"
HOSTAPD_CONFIG_FILE_PATH = "/etc/hostapd/hostapd.conf"
HOSTAPD_DEFAULT_FILE_PATH = "/etc/default/hostapd"
SYSCTL_CONF_PATH = "/etc/sysctl.conf"

def InstallWifiAccessPointPkgs(logger):
    #installation here
    logger.info("Start installing WifiAccessPointPkgs")
    pc = subprocess.Popen("apt-get install isc-dhcp-server hostapd".split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

def EditDhcpConfig(logger, filePath):
    logger.info("Start installing dhcp config")

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
def EditInterfacesConfig(logger, filePath):
    logger.info("Start installing interfaces config")

    script_dir = path.dirname(__file__)

    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpAccessPointInterface") 
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
        line = line + '\n'
        if (lineNumber_iface_wlan0<=lineNum and lineNum<=lineNumber_iface_next_after_wlan0):
            line=""
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
        line = line+'\n'
        if(line == '\n'):
            line = ""
        tempFhd.write(line);

    tempFhd.close()
    ret = remove(filePath)
    move(tempAbsPath,filePath)

    logger.info("End installing interfaces config")
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
def EditSysctlConfig(logger, filePath):
    logger.info("Start installing Sysctl config")
    originFhd = open(filePath,'r+')
    tempAbsPath = path.join(script_dir, "tmpSysctlConf") 
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
def EditIp4_forward():
    logger.info('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
    pc = subprocess.Popen('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    logger.info('iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    pc = subprocess.Popen('iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    logger.info('iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT')
    pc = subprocess.Popen('iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)

    logger.info('sh -c "iptables-save > /etc/iptables.ipv4.nat"')
    pc = subprocess.Popen('sh -c "iptables-save > /etc/iptables.ipv4.nat"'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)





if __name__ == "__main__":
    logger = BashHelper.SetupLogger('wifiAPConfig',"./wifiAPConfig.log")
    InstallWifiAccessPointPkgs(logger)
    BashHelper.BackupFileBfMod(DHCP_CONFIG_FILE_PATH,SCRIPT_DIR,logger)
    EditDhcpConfig(logger,DHCP_CONFIG_FILE_PATH)
    BashHelper.BackupFileBfMod(ISC_DHCP_SERVER_CONFIG_FILE_PATH,SCRIPT_DIR,logger)
    EditIscDhcpServerConfig(logger,ISC_DHCP_SERVER_CONFIG_FILE_PATH)
    BashHelper.BackupFileBfMod(INTERFACES_CONFIG_FILE_PATH,SCRIPT_DIR,logger)
    EditInterfacesConfig(logger,INTERFACES_CONFIG_FILE_PATH)
    BashHelper.BackupFileBfMod(HOSTAPD_CONFIG_FILE_PATH,SCRIPT_DIR,logger)
    EditHostApdConfig(logger,HOSTAPD_CONFIG_FILE_PATH)
    BashHelper.BackupFileBfMod(HOSTAPD_DEFAULT_FILE_PATH,SCRIPT_DIR,logger)
    EditHostApdDefault(logger,HOSTAPD_DEFAULT_FILE_PATH)
    BashHelper.BackupFileBfMod(SYSCTL_CONF_PATH,SCRIPT_DIR,logger)
    EditSysctlConfig(logger,SYSCTL_CONF_PATH)
    logger.info('sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward')
    pc = subprocess.Popen('sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('/usr/sbin/hostapd /etc/hostapd/hostapd.conf')
    pc = subprocess.Popen('/usr/sbin/hostapd /etc/hostapd/hostapd.conf'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('service hostapd start')
    pc = subprocess.Popen('service hostapd enable'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('service isc-dhcp-server start')
    pc = subprocess.Popen('service isc-dhcp-server enable'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('service hostapd start')
    pc = subprocess.Popen('service hostapd enable'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
    logger.info('service isc-dhcp-server start')
    pc = subprocess.Popen('service isc-dhcp-server enable'.split(),stdout = subprocess.PIPE)
    BashHelper.CheckOutputOfCallingBash(pc,logger)
