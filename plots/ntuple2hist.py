import sys 

from ntuple2hist_cff import *
from mcsample_cfi import * 
from monitors_cfi import *
from cut_cfi import *
from sysWeight_cfi import *

if len(sys.argv) < 2:
  print "Please, add the name as like followings."
  print "> python  ntuple2hist.py [1,2,3, or 4] \n"
  sys.exit()

arg = sys.argv[1]
arg2 = sys.argv[2]

ii=int(arg)
kk=int(arg2)
jj=len(mm_cuts["cut"])-2
if kk > len(mceventweight)+1 : sys.exit()

iijj = int(ii/jj)
cuti= int(ii%jj)+2

if iijj>len(monitors)+1 : sys.exit()

mm_cut=cut_maker(mm_cuts,cuti)
ee_cut=cut_maker(ee_cuts,cuti)
em_cut=cut_maker(em_cuts,cuti)

mcweight=mceventweight[kk]

mon1=[]
if iijj<len(monitors) :
  mon1 = [monitors[iijj]]
  print str(mon1)

mon2=[]
for mon22 in monitors2d.keys():
  if mon22 == ("Mon%d"%iijj) :
    mon2+=monitors2d[ ("Mon%d"%iijj) ]
    print "++"+str(mon2)+"++"


jsonMM = {
"mcsamples" : mcsamples,
"mceventweight": mcweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : mm_cut, 
"output" : "hist_mon" + arg +mm_cut["channel"]+ ".root"
}

#print " "
#print " "+str(jsonMM["mceventweight"])
#print " "+str(jsonMM["cuts"])
#sys.exit()
makehist(jsonMM)

jsonEE = {
"mcsamples" : mcsamples,
"mceventweight": mcweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : ee_cut,
"output" : "hist_mon" + arg +ee_cut["channel"]+ ".root"
}
makehist(jsonEE)

jsonEM = {
"mcsamples" : mcsamples,
"mceventweight": mcweight,
"datasamples" : datasamples,
"monitors" : mon1,
"monitors2" : mon2,
"cuts" : em_cut,
"output" : "hist_mon" + arg +em_cut["channel"]+ ".root"
}
makehist(jsonEM)

