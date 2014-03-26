#!/usr/bin/python
import numpy
import re
import gzip
import sys
import scipy
from scipy import stats

poppair=sys.argv[1]
myinputfile=sys.argv[2]

genomelist=[] # a list of all deltadafs in teh whole genome

#print 'hey'
#print '>>>>>>', chr  
infile=open(myinputfile, 'r')
for line in infile:
	#print line 
	strline=line.rstrip()
	if re.search('delta', line) :
		y=strline.split('\t')
	 	#print y.index(poppair )
	else:	
		x=strline.split('\t')
		#print x[1]
		genomelist.append(float(x[y.index(poppair )]))

infile.close()
#print genomelist
#~~~~~~~~ establish threshold ~~~~~~~~~~~~~~~~~~~~~
#print len(genomelist) , min(genomelist) , numpy.average(genomelist) ,  max(genomelist) 

thresh=scipy.stats.scoreatpercentile(genomelist, 99)
nbtotobserv=len(genomelist)
#print 'thresh %f' %( thresh)
#~~~~~~~~~~~~~~~~~~~~~~~~
tempgenome=set(genomelist)
newgenome=[]  # a list of uniq ordered dafs 
for item in tempgenome: newgenome.append(item) 

#print len(newgenome), min (newgenome), numpy.average(newgenome) , max(newgenome)
dika={} # histogram 
for item in newgenome: 
	dika[item]=genomelist.count(item)

#print newgenome
#~~~~~~~~~  analize teh test chromosome ~~~~~~~~~~~~~~~~~~~


#print thresh, len(newgenome) 


print 'pos deltaDAF percentile pval'

pfile=open(myinputfile, 'r')

countlines=0
for pline in pfile: 
	strline=pline.rstrip()
        if re.search('delta', pline) :
     		y=strline.split('\t')
               	#print y.index(poppair )
	else:
		p=strline.split('\t')
		testvalue=float(p[y.index(poppair )])
		#print testvalue
		countlines+=1
		if testvalue>= thresh:  # olny values in teh last percentile 
			#print 'yes' 
			#percentile_at=scipy.stats.percentileofscore(newgenome, float( p[y.index(poppair )] ) )
			#percentile_at= (newgenome.index(testvalue)+1) /float(len(newgenome)) *100
			#p_val= 1- ((newgenome.index(testvalue)+1) /float(len(newgenome)))
			nbsmallerobs=0
			for item in dika:
				if item<testvalue: nbsmallerobs+=dika[item] 
			
			percentile_at=(nbsmallerobs+1)/float(nbtotobserv)
			p_val= 1- (percentile_at) 
			if p_val==0: p_val=1e-10
			print '%s %.5f %.8f %.10f' % (p[0] , testvalue, percentile_at, p_val )

