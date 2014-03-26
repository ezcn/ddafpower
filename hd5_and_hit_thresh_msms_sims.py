#!/usr/bin/python
import re 
import sys
import os 
import shlex
import gzip 


interval=int(sys.argv[1])
thresh=sys.argv[2]
d=thresh.split('.')
tname=d[1]
thresh=float(thresh)

pvalfile=sys.argv[3]


#~~~~~~~~upload the first percentile data and select hits ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
countsnps=0
a=[]
dic={}
countwindows=0
for line in open (pvalfile, 'r') :
	#print line 
	strline=line.rstrip()
	x=strline.split()
	if re.search('pos', line ): 
		for item in x: 
			if re.search('delta', item): colDDAF=x.index(item)
			elif re.search('pos', item): colpos=x.index(item)
	else: 
		if countsnps<interval: a.append(float (x[colDDAF])); dic[countsnps]=( int(x[colpos])); countsnps+=1
		else:
			countwindows+=1
			if max(a)>=thresh: 
				peak=max(a)
				peakpos=dic[a.index(peak)]
				print  peakpos, peak
                        a=[]
                        countsnps=0
	

if len(a)> 0: 
	countwindows+=1
	if max(a)>=thresh:
		peak=max(a)
		peakpos=dic[a.index(peak)]
		print peakpos, peak
a=[]
countsnps=0

print 'WINDOWS', countwindows
