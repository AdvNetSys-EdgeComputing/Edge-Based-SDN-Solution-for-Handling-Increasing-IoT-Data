#!/bin/bash

ls /root/MQTT | grep -w "client.d" > /dev/null
if [ $? == 0 ]
then
	ping -c 1 192.168.0.2 > /dev/null
	if [ $? == 0 ]
	then
		echo "Connectivity with edge router established"
		python3 /root/MQTT/mqttgen.py /root/MQTT/config.json > /root/MQTT/client.d/$(date +%Y%m%d%H%M%S).o
		scp /root/MQTT/client.d/* 192.168.0.2:/root/MQTTRev/rawIOT.o
		rm -rf /root/MQTT/client.d/*
		echo "Output file sent successfully"
	else
		echo "No connectivity to edge router"
	fi
else
	echo "Client directory does not exist"
fi
