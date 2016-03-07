import sys 

from ntuple2hist_cff import *
from mcsample_cfi import * 
mcsamples = [ x for x in mcsamples if x["name"].find("POW")>-1 ]
#mcsamples = [ x for x in mcsamples if x["name"].find("dwPOWttbb")>-1 ]
#from monitors_cfi import *
from cut_cfi import *
from sysWeightQ2_cfi import *

if len(sys.argv) < 2:
  print "Please, add the name as like followings."
  print "> python  ntuple2hist.py [1,2,3, or 4] \n"
  sys.exit()

arg = sys.argv[1]
arg2 = sys.argv[2]

ii=int(arg)
kk=int(arg2)
jj=len(mm_cuts["cut"])-2-4

if kk > len(monitors)+1 : sys.exit()

iijj = int(ii/jj)
cuti= int(ii%jj)+2+4

if iijj>len(scaleweight)+1 : sys.exit()

mm_cut=cut_maker(mm_cuts,cuti)
ee_cut=cut_maker(ee_cuts,cuti)
em_cut=cut_maker(em_cuts,cuti)

mcweight=scaleweight[iijj]

print str(mm_cut)
print str(ee_cut)
print str(em_cut)

############
mon1=[]
mon2=[]
if kk<len(monitors) :
  mon1 = [monitors[kk]]
  print str(mon1)
else :
  mon2 = monitors2d

###########
print str(mcweight)

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

