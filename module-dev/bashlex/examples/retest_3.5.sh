#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
CURRENT_DIR=$(pwd)

cd ../
sudo python3.5 setup.py install
cd $CURRENT_DIR
python3.5 commandsubstitution-remover.py  test.sh
