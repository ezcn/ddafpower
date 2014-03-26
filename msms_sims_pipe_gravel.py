import subprocess 
import os 
import shutil
import tempfile
import sys
import random 


#f=0.5; s=0.1; h=0.5; t=51000; r=1
f=float(sys.argv[1])
s=float(sys.argv[2]) 
h=float(sys.argv[3]) 
t=float(sys.argv[4])
r=int(sys.argv[5])
 
myinputparameters=(f,s,h,t,r)

myseed=random.randint(1, 999999) 
##############  myseed=819643
Ne=10000; gentime=25
time=t/float(gentime)/float(4*Ne)

twoNes=2*Ne*s
wAA=1+twoNes
wAa=1+(h*twoNes)
waa=0

tmp_dir = tempfile.mkdtemp()
print tmp_dir

myuniqname=(tmp_dir,  f*100,s*100,h*100,t/1000,r) 
# msms sims gravel 
cmdl0='../bin/msms -N %s -ms 1064 1 -seed %s  -t 240  -r 320 250000   -I 2 492  572 0  -n 1 1.4  -n 2 4.58 -g 2 192 -m 1 2 0.31  -m 2 1 0.31  -en 0.023 2 0.186100  -em 0.023000 1 2 6  -em 0.023000 2 1  6 -ej 0.051 2 1  -en 0.148 1 0.73100  -SI %s  2  %s  %s  -Smark -Sp 0.5 -Sc 0 2 %s %s  %s > %s/myout.%s.%s.%s.%s.%s.out' % (Ne ,myseed , time, f, f, wAA, wAa, waa, tmp_dir, f*100,s*100,h*100,t/1000,r )
os.system(cmdl0)


#THIS IS A TEST COMMAND LINE 
#cmdl0='../bin/msms -N %s -ms 1064 1 -seed %s  -t 2.40  -r 3.20 2500  -I 2 492  572 0  -n 1 1.4  -n 2 4.58 -g 2 192 -m 1 2 0.31  -m 2 1 0.31  -en 0.023 2 0.186100  -em 0.023000 1 2 6  -em 0.023000 2 1  6 -ej 0.051 2 1  -en 0.148 1 0.73100  -SI %s  2  %s  %s  -Smark -Sp 0.5 -Sc 0 2 %s %s  %s > %s/myout.%s.%s.%s.%s.%s.out' % (Ne ,myseed , time, f, f, wAA, wAa, waa, tmp_dir, f*100,s*100,h*100,t/1000,r )
#os.system(cmdl0)
#



# msms2xpehh haplotypes 
cmdl1='/usr/bin/python ../test/generate_haplotypefiles.py  %s/myout.%s.%s.%s.%s.%s.out ' % (myuniqname) #(tmp_dir, f*100,s*100,h*100,t/1000,r, ) 
#print cmdl1
os.system(cmdl1)

# simstats 
hdcmdl1='../test/msms_sims_stats_filter.py %s/myout.%s.%s.%s.%s.%s.out  250000 > %s/myout.%s.%s.%s.%s.%s.out.stats' % ( myuniqname + myuniqname )  #(tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r)
#print hdcmdl1
os.system(hdcmdl1)


# hd rank 
hdcmdl2='/usr/bin/python ../test/hd4_percentileatscore_msms_sims_singlefile.py  deltadaf_0-1 %s/myout.%s.%s.%s.%s.%s.out.stats >  %s/myout.%s.%s.%s.%s.%s.out.stats.extreme ' % (myuniqname + myuniqname ) #(tmp_dir, f*100,s*100,h*100,t/1000,r) 
os.system(hdcmdl2) 

              
# hd hit 
hdcmdl3='/usr/bin/python ../test/hd5_and_hit_thresh_msms_sims.py 1000 0.70 %s/myout.%s.%s.%s.%s.%s.out.stats.extreme > %s/myout.%s.%s.%s.%s.%s.out.stats.extreme.hits '  %  (myuniqname + myuniqname ) #(tmp_dir, f*100,s*100,h*100,t/1000,r)
os.system(hdcmdl3)

# msms2xpehh recombination maps 
cmdl4='/usr/bin/python ../test/generate_recombination_maps.py  %s/myout.%s.%s.%s.%s.%s.out.stats > %s/myout.%s.%s.%s.%s.%s.out.map' % (myuniqname + myuniqname ) #(tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r)
#print cmdl4
os.system(cmdl4) 

# submit ihs 
cmdl5='ihs  %s/myout.%s.%s.%s.%s.%s.out.map %s/myout.%s.%s.%s.%s.%s.out.pop2.hap > %s/myout.%s.%s.%s.%s.%s.ihs.pop2' %  (myuniqname +  myuniqname + myuniqname ) #(tmp_dir, f*100,s*100,h*100,t/1000,r,tmp_dir, f*100,s*100,h*100,t/1000,r,tmp_dir, f*100,s*100,h*100,t/1000,r)
#print cmdl5 
os.system(cmdl5)

# standardize ihs 
cmdl6='/usr/bin/python  ../test/standardize_ihs.py  ../test/ihs.tennessen %s/myout.%s.%s.%s.%s.%s.ihs.pop2  > %s/myout.%s.%s.%s.%s.%s.ihs.pop2.stdz' % (myuniqname + myuniqname) #(tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r)
os.system(cmdl6) 


# submit xpehh
cmdl7= 'xpehh -m  %s/myout.%s.%s.%s.%s.%s.out.map -h %s/myout.%s.%s.%s.%s.%s.out.pop1.hap %s/myout.%s.%s.%s.%s.%s.out.pop2.hap > %s/myout.%s.%s.%s.%s.%s.xpehh'  % (myuniqname + myuniqname + myuniqname + myuniqname) #(tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r , tmp_dir,  f*100,s*100,h*100,t/1000,r) 
os.system(cmdl7) 

# standardize xpehh 
cmdl8='/usr/bin/python  ../test/standardize_xpehh.py  ../test/xpehh.tennessen %s/myout.%s.%s.%s.%s.%s.xpehh > %s/myout.%s.%s.%s.%s.%s.xpehh.stdz' % (myuniqname + myuniqname)  #(tmp_dir, f*100,s*100,h*100,t/1000,r, tmp_dir, f*100,s*100,h*100,t/1000,r)  
os.system(cmdl8)

# summarize 
cmdl9='/usr/bin/python  ../test/msms_sims_stats_summary_singlerep.py  %s/myout.%s.%s.%s.%s.%s.out  %s/myout.%s.%s.%s.%s.%s.out.stats %s/myout.%s.%s.%s.%s.%s.ihs.pop2.stdz %s/myout.%s.%s.%s.%s.%s.xpehh.stdz  %s/myout.%s.%s.%s.%s.%s.out.stats.extreme.hits > %s/myout.%s.%s.%s.%s.%s.out.summary %s %s %s %s %s ' % (myuniqname + myuniqname + myuniqname + myuniqname + myuniqname + myuniqname + myinputparameters)
os.system(cmdl9)

cpsummary='cp  %s/myout.%s.%s.%s.%s.%s.out.summary   /lustre/scratch113/teams/tyler-smith/users/cv1/scripts/hd_snpindels/REVISION/msms/msms/simsgra' % (myuniqname)
os.system(cpsummary) 

#cpline='cp -r %s  /lustre/scratch113/teams/tyler-smith/users/cv1/scripts/hd_snpindels/REVISION/msms/msms/simsgra' % (tmp_dir) 
#os.system(cpline) 

shutil.rmtree(tmp_dir)  
