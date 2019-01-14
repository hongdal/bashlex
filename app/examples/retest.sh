#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
CURRENT_DIR=$(pwd)

cd ../
sudo python2.7 setup.py install
cd $CURRENT_DIR
python commandsubstitution-remover.py  test.sh