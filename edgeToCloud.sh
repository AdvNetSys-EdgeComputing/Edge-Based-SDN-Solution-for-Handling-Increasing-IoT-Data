#!/bin/bash

ls /root/MQTTRev | grep -w "rawIOT.o" > /dev/null
if [ $? == 0 ]
then
	ping -c 1 10.0.0.2 > /dev/null
	if [ $? == 0 ]
	then
		echo "Connectvity with cloud established."
		while [ 1 ]
		do
			inotifywait /root/MQTTRev/rawIOT.o > /dev/null && echo "IOT Raw data received. Sending to cloud."
			scp /root/MQTTRev/rawIOT.o 10.0.0.2:/root/fromEdge.d/rawData.o
		done
	else
		echo "No connectivity with cloud"
	fi
else
	echo "Receiver end output file missing"
fi
