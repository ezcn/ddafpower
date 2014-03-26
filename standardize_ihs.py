#!/usr/bin/python

import sys 
import numpy 
import scipy.stats


myreffile=sys.argv[1]
myfiletostandardize=sys.argv[2]

##########################################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#################################################################
ihsref=[]
f=open (myfiletostandardize, 'r')
for line in open (myreffile, 'r'): 
	x=line.split()
	#ihsref.append(float(x[5])) 
	ihsref.append(float(x[5]))
for line in f: 
	y=line.split()
	ihsref.append(float(y[5])) 
f.close()
	

ihsrefstand=scipy.stats.mstats.zscore(ihsref)
union=zip(ihsref, ihsrefstand) 

myrefdic={}
for item in union: 
	if not item[0] in myrefdic: myrefdic[item[0]]=item[1]

#print myrefdic


################################################################# 
for line in open (myfiletostandardize, 'r'):
	z=line.split()
	if is_number(z[-1]) :     
		print '%s\t%s' %(line.rstrip(), myrefdic[float(z[5])]  ) 
	else: print '%s\t%s' %(line.rstrip(), 'nan') 


