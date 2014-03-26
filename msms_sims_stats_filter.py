#!/usr/bin/python
import sys 
import re
import math 
import numpy 
import scipy.stats

def all_pairs(seq):
    l = len(seq)
    for i in range(l):
        for j in range(i+1, l):
            yield seq[i], seq[j]



infile=sys.argv[1]
sizebp=sys.argv[2]

myfile=open(infile).readlines()

#-------------------
positions=[x.rstrip().split()[1:]  for x in myfile  if re.match('positions', x)][0]
freq={}
for site  in positions: freq[site]={}
#---------------
popsize={}
cmdl=myfile[0].split()
npop=int(cmdl[cmdl.index('-I') +1] )
for pop in range(npop): 
	popsize[pop]=int(cmdl[cmdl.index('-I')+2+pop] )

for site  in positions: 
	for pop in popsize: freq[site][pop]={}
#print freq
#----------------------------------
samplelines=[myfile.index(x)  +1  for x in myfile  if re.match('positions', x)] # initialize 
start= samplelines[0]
for p in popsize: 
	end=start+popsize[p]; start=end 
	samplelines.append(end) 
#-----------------------------------------
mypop=0
for i in samplelines[:-1]: 
	#print 'mypop', mypop 
	seqstart=i ; seqend=samplelines[samplelines.index(i)+1]
	#print seqstart, seqend, mypop
	for sequence in myfile[seqstart: seqend] : 
		count=0
		#print sequence
		for n in sequence.rstrip(): 
			if not n in freq[positions[count]][mypop] : freq[positions[count]][mypop][n]=1
			else: freq[positions[count]][mypop][n]+=1
			count+=1 
		
	mypop+=1


#-----------------



print '%s\t' %('pos'),
for pop in range(npop):print 'daf_%s\t' %(pop),
for couple  in all_pairs(popsize.keys()): print 'deltadaf_%s-%s\t' %(couple[0], couple[1]),
for couple  in all_pairs(popsize.keys()): print 'fst_%s-%s\t' %(couple[0], couple[1]),
print '%s\t%s' %('globfst', 'coeff_of_var')

for site in positions: 
	#print site, freq[site]  
	popcount=0; popfreq=[]; dafdiff=[]; fsts=[]; globfst=0
	for pop in popsize: 
		dac=0
		for n in freq[site][pop]:
			if n !='0': dac+=freq[site][pop][n]
		daf=dac/float(popsize[pop])
		popfreq.append(daf)
		#print '%.4f' % (daf) ,
	overallfreq=sum(popfreq) / float(len(popfreq))
	#print "popfreq", popfreq, overallfreq
	#if overallfreq >= 0.01: 
	if popfreq[1]>=0.01: 
		position=float(site)
        	print '%s\t' %( int(round(position*float(sizebp))))   ,
		for couple  in all_pairs(popfreq):
			dafdiff.append(math.fabs(couple[0] - couple[1]))
			fsts.append(numpy.var(couple)/float ( numpy.mean(couple) * (1-numpy.mean(couple)) ))

		for item in popfreq: print '%.4f\t' %(item),
        	for item in dafdiff: print '%.4f\t' %(item),
	        for item in fsts: print '%.4f\t' %(item),
		globfst= numpy.var(popfreq)/float ( numpy.mean(popfreq) * (1-numpy.mean(popfreq)) )
	        cv= scipy.stats.variation(popfreq)
        	print '%.4f\t%.4f' %(globfst, cv)


