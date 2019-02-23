ip -4 route get 114.114.114.114 | awk {'print $7'} | tr -d '\n'
ps aux | grep "bash" | grep -v grep | awk '{print $2}' 