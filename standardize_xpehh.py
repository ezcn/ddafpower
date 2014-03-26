#!/usr/bin/python

import sys 
import numpy 
import scipy.stats


myreffile=sys.argv[1]
myfiletostandardize=sys.argv[2]

#################################################################
xpehhref=[]
f=open (myfiletostandardize, 'r')
for line in open (myreffile, 'r'): 
	x=line.split()
	#ihsref.append(float(x[5])) 
	xpehhref.append(float(x[-1]))
for line in f: 
	y=line.split()
	xpehhref.append(float(y[-1])) 
f.close()
	

xpehhrefstand=scipy.stats.mstats.zscore(xpehhref)
union=zip(xpehhref, xpehhrefstand) 

myrefdic={}
for item in union: 
	if not item[0] in myrefdic: myrefdic[item[0]]=item[1]

#print myrefdic


################################################################# 
for line in open (myfiletostandardize, 'r'):
	z=line.split()     
	print '%s\t%s' %(line.rstrip(), myrefdic[float(z[-1])]  ) 

