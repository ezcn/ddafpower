#!/usr/bin/python
import sys 
import re
import math 
import numpy 
import scipy.stats



infile=sys.argv[1]
#outdir=sys.argv[2]
myfile=open(infile).readlines()

#-------------------
popsize={}
cmdl=myfile[0].split()
npop=int(cmdl[cmdl.index('-I') +1] )
for pop in range(npop): 
	popsize[pop]=int(cmdl[cmdl.index('-I')+2+pop] )

#----------------------------------
samplelines=[myfile.index(x)  +1  for x in myfile  if re.match('positions', x)] # initialize 
start= samplelines[0]
for p in popsize: 
	end=start+popsize[p]; start=end 
	samplelines.append(end) 
#print samplelines
#-----------------------------------------
mypop=1

for i in samplelines[:-1]: 
	#myout=open( '%s/%s.pop%s.hap' %(outdir, infile, mypop), 'w')
	myout=open( '%s.pop%s.hap' %(infile, mypop), 'w')
	sys.stdout=myout 
	#print 'mypop', mypop 
	seqstart=i ; seqend=samplelines[samplelines.index(i)+1]
	#print seqstart, seqend, mypop
	for sequence in myfile[seqstart: seqend] : 
		count=0
		#print mypop,  "\t", sequence #.rstrip()
		print " ".join(sequence.rstrip()) 
	mypop+=1
