import re 
import sys 

#f=0.5; s=0.1; h=0.5; t=51000; r=1

simsoutfile=sys.argv[1]
fstfile=sys.argv[2]
ihspop2file=sys.argv[3]
xpehhfile=sys.argv[4]
hdhitsfile=sys.argv[5]

f=float(sys.argv[6])
s=float(sys.argv[7])
h=float(sys.argv[8])
t=float(sys.argv[9])
r=int(sys.argv[10])

myres=[f,s,h,t,r]

####################################################
file0=open(simsoutfile).readlines()
cmdl=file0[0].split()
myseed=int(cmdl[cmdl.index('-seed')+1] )
myres.append(myseed) 


###########################################

file1=open(fstfile, 'r')
fst={}
for line in file1:  
	x=line.split()
	if not re.search ('fst', line): fst[int(x[0])]=float(x[5])  	
	if not re.search ('pos', line) : 
		if int(x[0]) ==125000: myres.append('1'); myres.append(x[2]);  myres.append(x[3]);

if 125000 in fst: 
	for fi in fst: 
		if fst[fi]== max(fst.values()) : 
			if int(fi)==125000: myres.append('y') 
			else: myres.append('n')
else: quit()
		

###################################  conta quante volte ihs e max a 125000 #####################

file4=open(ihspop2file, 'r') 
ihs2={}
for line in file4:
	x=line.rstrip().split(); ihs2[int(x[1])]=float(x[-1]) 
	if int(x[1]) ==125000: myres.append('1'); myres.append(x[-1])
if 125000 in ihs2: 
	for ih in ihs2:
        	if ihs2[ih]== max(ihs2.values()) :
                	if int(ih)==125000:  myres.append('y')
                        else: myres.append(x[-1]); myres.append('n')
else: myres.append('null'); myres.append('null') ;  myres.append('null') 

########################################################################################################

file5=open(xpehhfile, 'r')
xpehh={}
for line in file5:
	x=line.rstrip().split(); xpehh[int(x[1])]=float(x[-1])
	if int(x[1]) ==125000: myres.append('1'); myres.append(x[-1]);
if 125000 in xpehh:
	for xp in xpehh:
        	if xpehh[xp]== max(xpehh.values()) :
                	if int(xp)==125000:  myres.append('y')
			else:  myres.append('n')

else: myres.append('null'); myres.append('null') ;  myres.append('null')
#else: print 'nononononono'


####################################   conta quante volte hdsite e a 1250000 ###############

file2=open(hdhitsfile, 'r')
count=0
for line in file2: 
	if re.match('125000', line): count+=1

if count>0: myres.append('y')
else: myres.append('n')	

###################################### print!! ##################################################

print "\t".join(['f', 's' ,'h', 't', 'r','seed', 'accepted', 'frqpop2','ddaf', 'fstmax' ,'ihsacc', 'ihs',  'ihsmax', 'xpehhacc', 'xpehh', 'xpehhmax', 'hd'])
print "\t".join(str(i) for i in myres) 
			 
