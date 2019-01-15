#!/bin/bash

MEM_FREE=$(free -m |grep -i mem |awk '{if($4 < 100){ printf("1")}}')
MEM_AVAILABLE=$(free -m |grep -i mem |awk '{if($7 < 200){ printf("1")}}')
if [ $MEM_FREE == 1 ] && [ $MEM_AVAILABLE == 1 ] && [ $MEM_AVAILABLE == 2 ]; then
  now=$(date +"%Y-%m-%d-%T")
  echo 3 > /proc/sys/vm/drop_caches
  if [ $? -eq 0 ];then
    echo "Release space."
  else 
    echo "Release Error."
  fi
fi