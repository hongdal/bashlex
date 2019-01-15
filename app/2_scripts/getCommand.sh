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

CURRENT_DIR=$(pwd)/0_data/nodeData/
OUTPUT_DIR=$(pwd)/0_data/commandData
COUNT_DIR=$(pwd)/0_data/commandCount

function get_bash_command {
  cd $CURRENT_DIR
  FILES=$(ls $CURRENT_DIR | grep node )

  for file in $FILES; do
    echo $file
    temp=$(echo $file | cut -d "." -f1)
    output=$OUTPUT_DIR/$temp.command
    echo $output
    pcregrep -M  'Command.*\n.*,' $file | grep -oE "WordNode.*" | grep -oE "'.*'" | cut -d "'" -f2 | grep -oE "[[:alpha:] \.[:digit:]]*$" >> $output
    # pcregrep -M  'Command.*\n.*,' $file | grep -oE "WordNode.*" | grep -oE "'.*'" | cut -d "'" -f2 >> test.log
    # echo $command
  done
}

function get_command_count {
 
  cd $OUTPUT_DIR
  FILES=$(ls $OUTPUT_DIR | grep command )

  for file in $FILES; do
    echo $file
    temp=$(echo $file | cut -d "." -f1)
    output=$COUNT_DIR/$temp.count
    echo $output
    sort $file | uniq -c | sort -nr > $output
  done
  # grep -E -o "\b[[:alpha:]]+\b" $filename | awk ' { count[$0]++ } 
  # END{printf("%-20s%s\n","Word","Count");
  # for(word in count)
  #   {printf("%-20s%s\n",word,count[word])}
  # }'
}

main() 
{
  # get_bash_command
  # get_command_count "$CURRENT_DIR"/test.log
  get_command_count
}

main
