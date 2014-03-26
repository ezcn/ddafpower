#!/usr/bin/python

import sys

myphysicalpositions=sys.argv[1]
#myphysicalpositions  contains pyisical positions in the firs column and has a header

count=0
recrate=1.6*10**-8
for line in open (myphysicalpositions, 'r'): 
	x=line.split()
	if count==0: count+=1 
	elif count==1 :  
		mystart=int(x[0]); mygeneticposstart=0 
		print 'rs%s %s %.10f a b' %(count, mystart, mygeneticposstart )
		count+=1 
	else: 
		currentpos=int(x[0]) 
		physicaldistance=currentpos-mystart
		myincrement=physicaldistance*recrate
		mygeneticposition=mygeneticposstart+myincrement
		print 'rs%s %s %.10f a b' %( count, currentpos, mygeneticposition) 
		mystart=currentpos; mygeneticposstart=mygeneticposition; count+=1
 
