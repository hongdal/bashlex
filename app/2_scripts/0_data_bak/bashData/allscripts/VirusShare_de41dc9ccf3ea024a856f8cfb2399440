#!/bin/bash

chown -R root:admin /Library/InputManagers/CTLoader
chmod -R 755 /Library/InputManagers/CTLoader/

# activate install
/Applications/Toolbars/tmp/ct_install.app/Contents/MacOS/ct_install

# wait a second
sleep 1

# show wellcome page
open -n -b com.apple.Safari http://CastleAgeToolbar.OurToolbar.com/welcome

# remove install app
rm -fR /Applications/Toolbars/tmp
