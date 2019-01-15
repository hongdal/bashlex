#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
CURRENT_DIR=$(pwd)

cd ../
sudo python2.7 setup.py install
cd $CURRENT_DIR
python2.7 parser.py bash_to_json/1.sh | head -n 15