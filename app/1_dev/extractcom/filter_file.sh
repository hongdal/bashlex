#!/bin/bash
# 
#===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
# Filename:     filter_file.sh
# Version:      V1.0
# Author:       Guoze Tang(guozet@clemson.edu)
# Date:         2018-11-06
# Description:  Analyze the bash scripting files
#===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

CURRENT_DIR=$(pwd)
SCRIPT_DIR="$(dirname "$(pwd)")"
WORK_DIR=$SCRIPT_DIR
valid_file_prefix=Virus
ip_address="\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"
download_command="[^#;]*([0-9]{1,3}\.){3}[0-9]{1,3}[^;]*"
delete_space_command="[^ ]\+\( \+[^ ]\+\)*"
short_command_re="^[^ ]*"
# UNUSED
new_download_command="\b(wget|tftp|curl|busybox wget|busybox tftp|busybox curl)[^\;\n]*"
ip_num="~ ^[[:digit:]]+$ ]]"

# Output files
OUT_DIR=$CURRENT_DIR/output
TEMP_DIR=$CURRENT_DIR/temp
OUT_DOWNLOAD_DIR=$OUT_DIR/download
MERGE_TARGE_FILE=$OUT_DIR/merged_scripts.sh
OUT_ALL_IP=$OUT_DIR/all_ip_address.txt
OUT_ALL_COMMAND_FILE=$OUT_DIR/all_download_command.txt
OUT_VALID_IP=$OUT_DIR/valid_ip_address.txt
OUT_SUCCESSFUL_PARSERED_FILE=$OUT_DIR/parse_successed.txt
OUT_FAILED_PARSERED_FILE=$OUT_DIR/parse_failed.txt


function install_dependency {
    echo "[INFO] Installing dependency: $1"
    sudo apt-get -y install "$1"
}


# This function doesn't delete the duplicate files in folder
function merge_all_files {
  find . -name "$valid_file_prefix*" -type f -exec cat {} \;  > $MERGE_TARGE_FILE
}

# Delete the duplicate files in folder and merge the other bash scripts
function merge_all_scripts {
  FILES=$(ls $TEMP_DIR/ | grep $valid_file_prefix )
  count=$(ls $TEMP_DIR/ | grep $valid_file_prefix | wc -l )
  echo "============== Merge All Scripts to $MERGE_TARGE_FILE =============="
  echo "# Merged $count bash scripts files." >> $MERGE_TARGE_FILE
  for file in $FILES; do
    echo "# [FILENAME] $file" >> $MERGE_TARGE_FILE
    echo "# [PATH] $WORK_DIR/$file" >> $MERGE_TARGE_FILE
    echo "#------------------------------------------------------" >> $MERGE_TARGE_FILE;
    cat $SCRIPT_DIR/$file >> $MERGE_TARGE_FILE
    echo " " >> $MERGE_TARGE_FILE
    echo " " >> $MERGE_TARGE_FILE
  done
}

function replace_all_ipaddress {
  cd "$TEMP_DIR"
  echo "==============Replace All IPADDRESS =============="
  FILES=$(ls $TEMP_DIR | grep $valid_file_prefix )
 
  for file in $FILES; do
    # echo "Deal with IP in the $file"
    ip_string=$(grep -oE "$ip_address" -r1 $file)
    
    for ip in $ip_string; do
      echo $ip >> $TEMP_DIR/ip_record_temp.txt
    done

    if [ -f "ip_record_temp.txt" ]; then
      ip_string=$(sort -n ip_record_temp.txt | uniq)
      for ip in $ip_string; do
        echo $ip >> $TEMP_DIR/ip_record.txt
      done
    fi
    rm -rf ip_record_temp.txt

    for ip in $ip_string; do
      sed -i "s/$ip/_IPADDRESS_/g" $file
    done
  done
  # touch $OUT_ALL_IP
  sort -n "$TEMP_DIR"/ip_record.txt | uniq >> "$OUT_ALL_IP"
}


function parser_bash_scripts {
  cd $TEMP_DIR
  echo "============== Parser ALL the Bash Files in this folder =============="
  FILES=$(ls $TEMP_DIR | grep $valid_file_prefix )
 
  count=0
  for file in $FILES; do
    # echo "Deal with IP in the $file"
    $(python2.7 $CURRENT_DIR/parser.py $file > out_$file)
    if [ $? -eq 0 ];then
      echo $file >> $OUT_SUCCESSFUL_PARSERED_FILE
      ((count++))
    else
      echo $line >> $OUT_FAILED_PARSERED_FILE
    fi
#     ip_string=$(grep -oE "$ip_address" -r1 $file)
    
#     for ip in $ip_string; do
#       echo $ip >> $TEMP_DIR/ip_record_temp.txt
#     done

#     if [ -f "ip_record_temp.txt" ]; then
#       ip_string=$(sort -n ip_record_temp.txt | uniq)
#       for ip in $ip_string; do
#         echo $ip >> $TEMP_DIR/ip_record.txt
#       done
#     fi
#     $(rm -rf ip_record_temp.txt)

#     for ip in $ip_string; do
#       sed -i "s/$ip/_IPADDRESS_/g" $file
    done
    echo $count >> $OUT_SUCCESSFUL_PARSERED_FILE
#   done
#   # touch $OUT_ALL_IP
#   sort -n $TEMP_DIR/ip_record.txt | uniq >> $OUT_ALL_IP
# }
}



function download_all_files {
  cd "$OUT_DIR"

  # Install some dependency download tools which
  # may be used in this function.
  install_dependency wget
  install_dependency tftp
  install_dependency busybox
  
  downloadCommands=$(grep -oE "$download_command" $MERGE_TARGE_FILE | grep -o "$delete_space_command" > $OUT_ALL_COMMAND_FILE)

  if [ -f "$OUT_ALL_COMMAND_FILE" ]; then
    cat $OUT_ALL_COMMAND_FILE | while read line
    do
    {
      # echo $line
      folder_name=$(echo "$line" | grep -oE "$ip_address")
      echo $folder_name
      short_command=$(echo "$line" | grep -o "$short_command_re")
      # echo $short_command
      mkdir -p "$OUT_DOWNLOAD_DIR/$folder_name"
      cd "$OUT_DOWNLOAD_DIR/$folder_name/"
      if [ "$short_command" == "tftp" ]; then
        # wget http://guozet.me/
        busybox "$line"
      else $line
      fi
    } &
    done
    wait
  fi
}

function test_download_all_files {
  # cd $OUT_DIR
  # install_dependency wget
  # install_dependency tftp
  # install_dependency busybox
  ulimit -u 65535
  MERGE_TARGE_FILE=$CURRENT_DIR/merged_scripts.sh
  OUT_DOWNLOAD_DIR=$CURRENT_DIR/output/download
  mkdir -p $OUT_DOWNLOAD_DIR
  OUT_ALL_COMMAND_FILE=$CURRENT_DIR/sort_all_command.txt
  OUT_SUCCESSFUL_COMMAND_FILE=$CURRENT_DIR/successful_command.txt
  OUT_FAILED_COMMAND_FILE=$CURRENT_DIR/failed_command.txt
  OUTPUT_FILE=$CURRENT_DIR/command_process.txt

  # Install some dependency download tools which
  # may be used in this function.

  # ip_string=$(grep -oE "$ip_address" -r1 $file)
  # downloadCommands=$(grep -oE "$new_download_command" $MERGE_TARGE_FILE | grep -o "$delete_space_command" > $OUT_ALL_COMMAND_FILE)
  wget https://github.com/guozetang/guozetang.github.io/blob/hexo/userscripts/leetcode.sh
  if [ $? -eq 0 ];then
    echo "[SUCCESSFUL TEST] $line"  >> $OUT_SUCCESSFUL_COMMAND_FILE
  else
    echo "[ERROR TEST] $line"  >> $OUT_FAILED_COMMAND_FILE
  fi

  wget https://github.com/guozetang/guozetang.github.io/blob/hexo/uscripts/leetcode.sh
  if [ $? -eq 0 ];then
    echo $line >> $OUT_SUCCESSFUL_COMMAND_FILE
  else
    echo "[ERROR TEST] $line" >> $OUT_FAILED_COMMAND_FILE
  fi

  number=0
  if [ -f "$OUT_ALL_COMMAND_FILE" ]; then
    cat $OUT_ALL_COMMAND_FILE | while read line
    do
    {
      # echo $line
      folder_name=$(echo $line | grep -oE "$ip_address")
      echo $folder_name
      short_command=$(echo $line | grep -o "$short_command_re")
      echo $short_command
      mkdir -p $OUT_DOWNLOAD_DIR/$folder_name
      cd $OUT_DOWNLOAD_DIR/$folder_name/
      if [ $short_command == "tftp" ]; then
        $(busybox $line)
        if [ $? -eq 0 ];then
          echo $line >> $OUT_SUCCESSFUL_COMMAND_FILE
        else
          echo $line >> $OUT_FAILED_COMMAND_FILE
        fi
      else 
        $($line)
        if [ $? -eq 0 ];then
          echo $line >> $OUT_SUCCESSFUL_COMMAND_FILE
        else
          echo $line >> $OUT_FAILED_COMMAND_FILE
        fi
      fi
      ((number++))
      echo "[$number] $line" >> $OUTPUT_FILE
    } &
    done
    # echo "[$cont] $line" >> $OUTPUT_FILE
  fi
}

function configure_environment {
  echo "==============Create New DIR: $TEMP_DIR =============="
  mkdir -p $TEMP_DIR
  mkdir -p $OUT_DIR
  mkdir -p $OUT_DOWNLOAD_DIR
  cp $SCRIPT_DIR/$valid_file_prefix* $TEMP_DIR/
}

function test_ip_address {
  cd $TEMP_DIR
  ip_addresses=$(cat $OUT_ALL_IP)
  ip_string=$(grep -oE "$ip_address" -r1 $file)
  for ip in $ip_addresses; do
    ping -c 5 -t 200 $ip 2>/dev/null 1>/dev/null
    if [ "$?" = 0 ]
    then
      echo "Host found: $ip"
      echo $ip >> $OUT_VALID_IP
    else
      echo "Host not found: $ip"
    fi
  done
}

function find_and_delete_dulicates {
  cd "$TEMP_DIR" || exit
  declare -A arr
  shopt -s globstar
  FILES=$(ls $TEMP_DIR | grep $valid_file_prefix )
  old_count=$(ls $TEMP_DIR | grep $valid_file_prefix | wc -l )
  for file in $FILES;   do
    [[ -f "$file" ]] || continue

    read cksm _ < <(md5sum "$file")
    if ((arr[$cksm]++)); then 
      rm $file
      # echo "Delete $file"
    fi

  done
  new_count=$(ls $TEMP_DIR | wc -l )
  echo "These are $old_count before delete the duplicate files."
  echo "These are $new_count after delete the duplicate files."
}

main() 
{
  configure_environment;
  # replace_all_ipaddress;
  # find_and_delete_dulicates;
  # merge_all_scripts;
  # test_ip_address;
  # test_download_all_files
  # download_all_files;
  parser_bash_scripts
}

main
