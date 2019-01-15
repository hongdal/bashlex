#!/bin/bash

GetInstalledRpmPkgs ()
{
python << EOF
#!/usr/bin/python
import os
import subprocess

def GetDetailedInformationForInstalledRpmPkgs():
    stderr = ''
    exitCode = ''
    stdout = ''
    proc = subprocess.Popen (['rpm', '-qa', '--queryformat=<Package><Name>%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm</Name><Group>%{GROUP}</Group><Version>%{VERSION}</Version><VendorName>%{VENDOR}</VendorName></Package>'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    proc.wait()
    exitCode = proc.returncode
    print('<InstalledPackages>')
    print('<RawData><![CDATA[]]></RawData>')
    print('<ResultData>')
    print('<ExitStatus>'+str(exitCode)+'</ExitStatus>')
    print('<Message><![CDATA['+stderr.strip()+']]></Message>')
    print('</ResultData>')
    print('<Packages>')
    print(stdout)
    print('</Packages>')
    print('</InstalledPackages>')
    print('%&%&')

GetDetailedInformationForInstalledRpmPkgs()

EOF

}

GetInstalledDpkgPkgs ()
{
python << EOF
#!/usr/bin/python
import os
import subprocess
import platform
    
def GetDetailedInformationForDpkgPatches():
    stderr = ''
    exitCode = ''
    stdout = ''
    osName = ''
    osName = platform.dist()
    if osName[0] == 'Ubuntu':
        proc = subprocess.Popen (['dpkg-query', '-W', '-f=<Package><Name>\${Package}-\${Version}</Name><Group>\${Section}</Group><Version>\${Version}</Version><VendorName>Ubuntu</VendorName></Package>'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif osName[0] == 'debian':
        proc = subprocess.Popen (['dpkg-query', '-W', '-f=<Package><Name>\${Package}-\${Version}</Name><Group>\${Section}</Group><Version>\${Version}</Version><VendorName>Debian</VendorName></Package>'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    proc.wait()
    exitCode = proc.returncode
    print('<InstalledPackages>')
    print('<RawData><![CDATA[]]></RawData>')
    print('<ResultData>')
    print('<ExitStatus>'+str(exitCode)+'</ExitStatus>')
    print('<Message><![CDATA['+stderr.strip()+']]></Message>')
    print('</ResultData>')
    print('<Packages>')
    print(stdout)
    print('</Packages>')
    print('</InstalledPackages>')
    print('%&%&')
    
    
GetDetailedInformationForDpkgPatches()   

EOF

}

GetMacInstalledPkgs ()
{
python << EOF
#!/usr/bin/python
import subprocess
try:
    import elementtree.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import plistlib

installedPkgsList = []

def GetInstalledPackages():
    proc = subprocess.Popen(['system_profiler', '-xml', 'SPApplicationsDataType'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    proc.wait()
    exitCode = proc.returncode
    if (exitCode == 0):
        root = ET.fromstring(stdout)
        nodes = root.findall('array/dict/array/dict')
        for node in nodes:
            items = node.findall('*')
            result = ''
            result += '<Package>'	
            result += CollectInformationsFromXML(items)
            result += '</Package>'
            installedPkgsList.append(result)
    PrintOutputResult(stderr, exitCode)

def GetApplicationCategory(filepath):
    category = ''
    try:
        content = plistlib.readPlist(filepath)
        category = content['LSApplicationCategoryType']
        lastOccurence = category.rfind('.')
        category = category[lastOccurence + 1:len(category)]
    except:
        pass
    return category

def CollectInformationsFromXML(items):
    result = ''
    vendor = ''
    for index in range(len(items)):
        if items[index].text == '_name':
            result += '<Name>' + items[index+1].text.encode('utf-8') + '</Name>'
        if items[index].text == 'version':
            result += '<Version>' + items[index+1].text.encode('utf-8') + '</Version>'
        if items[index].text == 'path':
            filepath = items[index+1].text.encode('utf-8') + '/Contents/Info.plist'
            result += '<Group>' + GetApplicationCategory(filepath) + '</Group>'
        if items[index].text == 'info':
            vendorInfo = items[index+1].text.encode('utf-8')
            if (vendorInfo.find('Apple') != -1):
                vendor = 'Apple Inc.'
    result += '<VendorName>' + vendor + '</VendorName>'
    return result
 

    
def PrintOutputResult(stderr, exitCode):
    print('<InstalledPackages>')
    print('<RawData><![CDATA[]]></RawData>')
    print('<ResultData>')
    print('<ExitStatus>'+str(exitCode)+'</ExitStatus>')
    print('<Message><![CDATA['+stderr.strip()+']]></Message>')
    print('</ResultData>')
    print('<Packages>')
    for index in range(len(installedPkgsList)):
        print installedPkgsList[index]
    print('</Packages>')
    print('</InstalledPackages>')
    print('%&%&')
    
GetInstalledPackages()

EOF

}

echo 'TRUE:'
echo 'sshlog: starting installed packages scan'
echo '%&%&'

osType=$(uname -s)
if [ $osType == "Linux" ]; then
    Which=$(which rpm)
    Result=$?
    if [ $Result -eq 0 ]; then
        GetInstalledRpmPkgs
    else
        Which=$(which dpkg)
        Result=$?
        if [ $Result -eq 0 ]; then
            GetInstalledDpkgPkgs
        else
            echo "RPM and DPKG not found"
	fi
    fi
elif [ $osType == "Darwin" ]; then
    GetMacInstalledPkgs
fi

echo "!!SCRIPT_FINISHED!!"

# Self delete.
#rm -rf $0
