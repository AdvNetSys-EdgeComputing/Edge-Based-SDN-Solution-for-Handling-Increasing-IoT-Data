#!/bin/bash

ls /root/fromEdge.d | grep -w "rawData.o" > /dev/null
if [ $? == 0 ]
then
	while [ 1 ]
	do
		inotifywait /root/fromEdge.d/rawData.o > /dev/null && echo "IOT Raw data received from edge."
		./pressureFunction.py
		./tempFunction.py
		scp /root/fromEdge.d/pressureProcessed.o 10.0.0.1:/root/fromCloud.d/pressureProcessed.o
		scp /root/fromEdge.d/tempProcessed.o 10.0.0.1:/root/fromCloud.d/tempProcessed.o
	done
else
	echo "Raw data missing."
fi
