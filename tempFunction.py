#!/usr/bin/env python

import json
from pprint import pprint
import sys
import os
import subprocess

dict = {}
dict1 = {}
list = []
list_temp = []
temp = 0
val = 0

file =  open( '/root/fromEdge.d/rawData.o', 'r' ) 
timestamp = subprocess.check_output('stat /root/fromEdge.d/rawData.o | grep Modify | cut -d " " -f 2,3',shell=True)

for line in file:
	line = line.split( 'sensors:' )
	dict = line[1]
	d = json.loads( dict )
	if 'temperature' in d['type']:
		list.append( str(d['description']) )
		list_temp.append( int(d['value']) )

for i in range (0,len(list)):
        count = 1
	temp = list_temp[i]
        for j in range(i+1,len(list)):
                if list[i] == list[j]:
                        count+=1
			temp += list_temp[j]
	temp = temp/count
        if list[i] not in dict1:
		dict1.setdefault(list[i],[])
		dict1[list[i]].append(count)
		dict1[list[i]].append(temp)

sys.stdout = open ('/root/fromEdge.d/tempProcessed.o', 'w')
print 'The temperature has been recorded at the following date and time:',timestamp
for key,value in dict1.items():
	print('{}:'.format(key))
	print 'Number of readings is:',dict1[key][0]
	print 'Average Temperature is', dict1[key][1]
