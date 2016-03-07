from ROOT import *
import copy

from hist2plot_cff import *
from mcsample_cfi import *
from monitors_cfi import *

#import sys 
gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()

mon = monitors

mon2 = []
for i,ii in enumerate(monitors2d):
  #print monitors2d[ii]
  mon2.append(monitors2d[ii])

json = {
"file": "hist_all.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
"cuts" : [
"mm_S2","mm_S3","mm_S4","mm_S5", "mm_S6",  
"ee_S2","ee_S3","ee_S4","ee_S5", "ee_S6",
"em_S2","em_S3","em_S4","em_S5", "em_S6"
   ],
"weight" : ["CEN","csvweight"],
"monitors" : mon,
"monitors2" : mon2
}

#########
def mmeeem(json):
  #TH1F
  f = json['file'] 
  ######
  for step in json['cuts']:
    for mon in json['monitors']:
      for weight in json['weight']:
        singleplotStack2(f,mon,weight,step,json['mcsamples'],json['datasamples'],False)


jsonLL = {
"file": "hist_all.root",
"mcsamples" : mcsamples,
"datasamples" : datasamples,
"cuts" : [
"S2","S3","S4","S5","S6"
   ],
"weight" : ["CEN","csvweight"],
"monitors" : mon,
"monitors2" : mon2
}

def ll(jsonLL):
  f1 = jsonLL['file'] 
  for step1 in jsonLL['cuts']:
    for mon1 in jsonLL['monitors']:
      for weight in jsonLL['weight']:
        singleplotStackLL2(f1,mon1,weight,step1,jsonLL['mcsamples'],jsonLL['datasamples'],False)

def mmee(jsonLL):
  f1 = jsonLL['file'] 
  for step1 in jsonLL['cuts']:
    for mon1 in jsonLL['monitors']:
      for weight in jsonLL['weight']:
        singleplotStackMMEE2(f1,mon1,weight,step1,jsonLL['mcsamples'],jsonLL['datasamples'],False)


import sys
if len(sys.argv) < 2:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)

if int(arg1)==0:
  mmeeem(json)
elif int(arg1)==1:
  mmee(jsonLL)
else :
  ll(jsonLL)

