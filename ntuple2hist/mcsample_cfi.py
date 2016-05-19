from ROOT import *
from os import listdir
from os.path import isfile, join


###################################################################
loc = "/store/user/youngjo/Cattools/v7-6-4v2/"
z  ="v1" # bkg
zz ="v1" # data
zzz="v1" # ttbar


###################################################################
import os,commands
import subprocess
def files(path):
    import socket
    hostname = socket.gethostname()
    if hostname.find("sdf")==-1:
      llll = [""]
      return llll

    cmd, xrdbase = "xrd cms-xrdr.sdfarm.kr ls ","/xrd"
    size = 0
    l = set()
    for x in subprocess.check_output(cmd + xrdbase + path, shell=True).strip().split('\n'):
        xx = x.split()
        if len(xx) == 0: continue
        if xx[0][0] not in ('d', '-'): continue
        xpath = xx[-1]
        if len(xpath) == 0: continue
        xsize = int(xx[1])
        if xpath.startswith(xrdbase): xpath = xpath[len(xrdbase):]
        if xpath in l: continue
        l.add(xpath)
        size += xsize
    lll ="root://cms-xrdr.sdfarm.kr:1094///xrd" 
    llll = [ lll+l1 for l1 in l]
    #print llll
    return llll
    #return l, size

"""
def getEntries(mypath):
  lcgls="lcg-ls -v -b -T srmv2 -D srmv2 --vo cms srm://cms-se.sdfarm.kr:8443/srm/v2/server?SFN="
  aaa = (lcgls_+mypath)
  aaa2= commands.getoutput(aaa)

  bbb = (lcgls_+"/000"+str(Idx_)+"/ | grep -c catTuple ")
  #print bbb
  ddd= commands.getoutput(bbb)
  ddd2= int(ddd)
  if ddd2==999: ddd2+=getEntries(lcgls_,Idx_+1)
  return ddd2
"""

def sumWeight(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  htemp = TH1D("htempSS","",1,-2,2)
  tree.Project("htempSS","1","weight")
  return htemp.GetBinContent(1) 
 
def sumEntries(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  htemp = TH1D("htempSS","",1,-2,2)
  tree.Project("htempSS","1","1")
  return htemp.GetBinContent(1) 
  
###################################################################
###################################################################
def mAND(aaa,bbb):
  return "(" +aaa+ " && "+bbb+")"
def mAND2(aaa):
  bbb=""
  for i,ii in enumerate(aaa):
    if i==0 : 
      bbb+= ii
    else : 
      bbb=mAND(ii,bbb)
  return bbb
def op_(aaa):
  return "(!(" + aaa + "))"

def GW(sel="1"):
  return "("+sel+")"

def ttbarSelections(isVis):
  if isVis: 
    visible="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
    ttbb = mAND("(NbJets20>=4)",visible)
    ttb = mAND("(NbJets20==3 && !(genTtbarId%100==52))",visible)
    tt2b = mAND("(NbJets20==3 && (genTtbarId%100==52))",visible)
    ttcc = mAND("((NcJets20>=2) && !(NbJets20>=3))",visible)
    ttlf = mAND("(!(NbJets20>=4) && !(NbJets20==3) && !(NcJets20>=2))",visible)
    ttot = op_(visible)
    return ttbb,ttb,tt2b,ttcc,ttlf,ttot
  else : 
   #full phase
   fullphase ="(diLeptonicM1==1 && NaddJets20 >= 2)"
   #TTJJ = "(NaddJets20 >= 2 && diLeptonicM1==1)"
   ttbb = "(NaddbJets20 >= 2 && diLeptonicM1==1)"
   ttb = "(NaddJets20 >= 2 && NaddbJets20 == 1 && diLeptonicM1==1 && !(genTtbarId%100==52))"
   tt2b = "(NaddJets20 >= 2 && NaddbJets20 == 1 && diLeptonicM1==1 && (genTtbarId%100==52))"
   ttcc = "(NaddJets20 >= 2 && NaddcJets20 >= 2 && NaddbJets20==0 && diLeptonicM1==1)"
   ttlf = "( !"+ttbb+" && !"+ttb+" && !"+tt2b+" && !"+ttcc+"  && NaddJets20 >= 2 && diLeptonicM1==1)"
   ##ttlf = "( !"+ttbb+" && !"+ttb+" && !"+ttcc+"  && NaddJets20 >= 2 && diLeptonicM1==1)"
   ttot = op_(fullphase)
   return ttbb,ttb,tt2b,ttcc,ttlf,ttot

def oldttbarSelections():
  ll = " (partonInPhaseLep==1 && NgenJet>=4 )"
  ttbb = mAND(" (genTtbarId%100>52) ", ll)
  ttb  = mAND(" (genTtbarId%100>50 && genTtbarId%100<53) ", ll)
  ttc  = mAND(" (genTtbarId%100>40 && genTtbarId%100<43) ", ll)
  ttcc = mAND(" (genTtbarId%100>42 && genTtbarId%100<49) ", ll)
  ttlf = mAND(" (genTtbarId%100 ==0) ", ll)
  ttot  = op_(ll)
  return ttbb,ttb,ttc,ttcc,ttlf,ttot

###################################################################
###################################################################
###################################################################
import json
def loadJson(name):
  with open(name) as data_file:    
    data = json.load(data_file)
    return data

def getValues(data,doSumWeight):
  cx={}
  sumWeights={}
  fileList={}
  for aa in data:
    cx[aa["name"]]=aa["xsec"]
    if aa["name"] in ["DYJets_MG","DYJets_MG_5to50","TTJets_MG5"]:
      fileList[aa["name"]]   = files(loc + aa["name"] + zzz)
      if doSumWeight :
        sumWeights[aa["name"]] = sumEntries(files(loc +  aa["name"] + zzz))
        print "sumWeights['"+aa["name"]+"']="+str(sumWeights[aa["name"]])
    elif aa["name"] in ["TTJets_MG5","TTJets_aMC","TTJets_scaleup","TTJets_scaledown","TT_powheg","TT_powheg_scaledown","TT_powheg_scaleup","TT_powheg-herwigpp","TT_powheg_pythia6"]:
      fileList[aa["name"]]   = files(loc + aa["name"] + zzz)
      if doSumWeight :
        sumWeights[aa["name"]] = sumWeight(files(loc +  aa["name"] + zzz))
        print "sumWeights['"+aa["name"]+"']="+str(sumWeights[aa["name"]])
    elif aa["name"] in ["DYJets","DYJets_10to50","DYJets_MG","DYJets_MG_5to50","WJets","SingleTbar_tW","SingleTop_tW","SingleTbar_t","SingleTop_t","SingleTop_s","WW","WZ","ZZ","ttH_bb","ttH_nonbb","ttWJetsToQQ","ttWJetsToLNu","ttZToLLNuNu","ttZToQQ"]:
      fileList[aa["name"]]   = files(loc + aa["name"] + z)
      if doSumWeight :
        sumWeights[aa["name"]] = sumWeight(files(loc +  aa["name"] + z))
        print "sumWeights['"+aa["name"]+"']="+str(sumWeights[aa["name"]])
    elif aa["name"] in ["DoubleEG_Run2015C","DoubleEG_Run2015D","DoubleMuon_Run2015C","DoubleMuon_Run2015D","MuonEG_Run2015C","MuonEG_Run2015D"]:
      fileList[aa["name"]]   = files(loc + aa["name"] + zz)
  if doSumWeight : return cx,sumWeights,fileList
  else           : return cx,fileList


data = loadJson('../ntuple2hist/dataset.json')
cx = {}
sumWeights={}
fileList={}
sumWeights['DYJets']=76816262.0
sumWeights['DYJets_10to50']=22606898.5977
sumWeights['DYJets_MG']=9004328.0
sumWeights['DYJets_MG_5to50']=8771481.0
sumWeights['WJets']=16521035.0153
sumWeights['TTJets_MG5']=10215131.0
sumWeights['TTJets_aMC']=12698526.0
sumWeights['TTJets_scaleup']=14082216.0
sumWeights['TTJets_scaledown']=12798823.0
sumWeights['TT_powheg']=97994442.0
sumWeights['TT_powheg_scaledown']=9932876.0
sumWeights['TT_powheg_scaleup']=9919776.0
sumWeights['TT_powheg-herwigpp']=19383463.0
sumWeights['TT_powheg_pythia6']=0.0
sumWeights['SingleTbar_tW']=950000.0
sumWeights['SingleTop_tW']=1000000.0
sumWeights['SingleTbar_t']=0.0
sumWeights['SingleTop_t']=0.0
sumWeights['SingleTop_s']=0.0
sumWeights['WW']=988437.589993
sumWeights['WZ']=1000000.0
sumWeights['ZZ']=985600.0
sumWeights['ttH_bb']=0.0
sumWeights['ttH_nonbb']=0.0
sumWeights['ttWJetsToQQ']=429599.0
sumWeights['ttWJetsToLNu']=129001.0
sumWeights['ttZToLLNuNu']=183200.0
sumWeights['ttZToQQ']=350106.0


#############
if len(sumWeights.keys()) is 0 : 
  cx,sumWeights,fileList = getValues(data,True)
  import sys
  sys.exit()
else : 
  cx,fileList = getValues(data,False)

###################################################################
###################################################################
def ttbarMCSet(name,selections,filename):
  samples = []
  for sel in selections.keys():
    samples.append({"name":name+sel,"selection":selections[sel],"file":fileList[filename], "cx":cx[filename], "sumWeight":sumWeights[filename] })
  return samples
def bkgMCSet(name,filename):
  samples = []
  samples.append({"name":name,"selection":"(1)","file":fileList[filename], "cx":cx[filename], "sumWeight":sumWeights[filename]})
  return samples
def dataSet(name,filename):
  samples = []
  samples.append({"name":name,"selection":"(1)","file":fileList[filename] })
  return samples


isVis = True
ttbb,ttb,tt2b,ttcc,ttlf,ttot =ttbarSelections(isVis)
#ttbarSelections_={"ttbb":ttbb,"ttb":ttb,"tt2b":tt2b,"ttcc":ttcc,"ttlf":ttlf,"ttot":ttot,"All":"(1)"}
ttbarSelections_={"ttbb":ttbb,"ttb":ttb,"tt2b":tt2b,"ttcc":ttcc,"ttlf":ttlf,"ttot":ttot}

ttbarMCsamples = {  "MG5":"TTJets_MG5",         "AMC":"TTJets_aMC",            "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp" 
                   ,"upPOW":"TT_powheg_scaleup", "dwPOW":"TT_powheg_scaledown" 
                }
#ttbarMCsamples = {"MG5":"TTJets_MG5","AMC","TTJets_aMC","POW":"TT_powheg","upPOW":"TT_powheg_scaleup","dwPOW":"TT_powheg_scaledown","POHP":"TT_powheg-herwigpp","POPY6":"TT_powheg_pythia6" }
#bkgMCsamples = {"TTWlNu":"ttWJetsToLNu",  "TTWqq":"ttWJetsToQQ", "TTZll":"ttZToLLNuNu",   "TTZqq":"ttZToQQ",
bkgMCsamples = {  "TTWqq":"ttWJetsToQQ",  "TTZqq":"ttZToQQ",
                "STbt":"SingleTbar_t",    "STt":"SingleTop_t",   "STbtW":"SingleTbar_tW", "STtW":"SingleTop_tW",
                "WW":"WW",       "WZ":"WZ",         "ZZ":"ZZ",
                "WJets":"WJets", "DYJets":"DYJets", "DYJets10":"DYJets_10to50"
#                "ttH2non":"ttH_nonbb",  "ttH2bb":"ttH_bb"
               }
dataSamples = { "MuMu1":"DoubleMuon_Run2015C", "MuMu2":"DoubleMuon_Run2015D"
               ,"ElEl1":"DoubleEG_Run2015C",   "ElEl2":"DoubleEG_Run2015D"
               ,"MuEl1":"MuonEG_Run2015C",     "MuEl2":"MuonEG_Run2015D"
              }
mcsamples =[]
for ttbar in ttbarMCsamples.keys():
  mcsamples+=ttbarMCSet(ttbar,ttbarSelections_,ttbarMCsamples[ttbar])
for bkg in bkgMCsamples.keys():
  mcsamples+= bkgMCSet(bkg,bkgMCsamples[bkg])

mcsamples2 = [ mc for mc in mcsamples if mc["name"].find("DYJets")>-1 ]

#print str(mcsamples)
datasamples =[]
for data in dataSamples.keys():
  datasamples +=dataSet(data,dataSamples[data])


old="""
mcsamples=[
{"name":"MG5ttbb",  "selection": ttbb,       "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
{"name":"MG5ttb",   "selection": ttb,        "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
{"name":"MG5tt2b",  "selection": tt2b,       "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
{"name":"MG5ttcc",  "selection": ttcc,       "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
{"name":"MG5ttlf",  "selection": ttlf,       "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
{"name":"MG5ttot",  "selection": ttothers,   "file": fileList["TTJets_MG5"], "cx":cx[ttbarMG5]  ,"sumWeight": sumWeights["TTJets_MG5"]  },
                                                                                                                                         
{"name":"AMCttbb",  "selection": ttbb,       "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },
{"name":"AMCttb",   "selection": ttb,        "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },
{"name":"AMCtt2b",  "selection": tt2b,       "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },
{"name":"AMCttcc",  "selection": ttcc,       "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },
{"name":"AMCttlf",  "selection": ttlf,       "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },
{"name":"AMCttot",  "selection": ttothers,   "file": fileList["TTJets_aMC"], "cx":cx[ttbarAMC]  ,"sumWeight": sumWeights["TTJets_aMC"]  },

{"name":"upPOWAll",   "selection": "(1)",    "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"]  },
{"name":"upPOWttbb",  "selection": ttbb,     "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },
{"name":"upPOWttb",   "selection": ttb,      "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },
{"name":"upPOWtt2b",  "selection": tt2b,     "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },
{"name":"upPOWttcc",  "selection": ttcc,     "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },
{"name":"upPOWttlf",  "selection": ttlf,     "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },
{"name":"upPOWttot",  "selection": ttothers, "file": fileList["TT_powheg_scaleup"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaleup"] },

{"name":"dwPOWAll",   "selection": "(1)",    "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"]  },
{"name":"dwPOWttbb",  "selection": ttbb,     "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },
{"name":"dwPOWttb",   "selection": ttb,      "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },
{"name":"dwPOWtt2b",  "selection": tt2b,     "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },
{"name":"dwPOWttcc",  "selection": ttcc,     "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },
{"name":"dwPOWttlf",  "selection": ttlf,     "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },
{"name":"dwPOWttot",  "selection": ttothers, "file": fileList["TT_powheg_scaledown"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_scaledown"] },

{"name":"sysPOWAll","selection": "(1)",      "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWttbb",  "selection": ttbb,       "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWttb",   "selection": ttb,        "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWtt2b",   "selection": tt2b,      "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWttcc",  "selection": ttcc,       "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWttlf",  "selection": ttlf,       "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },
{"name":"POWttot",  "selection": ttothers,   "file": fileList["TT_powheg"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg"] },

{"name":"sysPOHPAll","selection": "(1)",      "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPttbb",  "selection": ttbb,       "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPttb",   "selection": ttb,        "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPtt2b",   "selection": tt2b,      "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPttcc",  "selection": ttcc,       "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPttlf",  "selection": ttlf,       "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },
{"name":"POHPttot",  "selection": ttothers,   "file": fileList["TT_powheg-herwigpp"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg-herwigpp"] },

{"name":"sysPOPY6All","selection": "(1)",      "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6ttbb",  "selection": ttbb,       "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6ttb",   "selection": ttb,        "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6tt2b",   "selection": tt2b,      "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6ttcc",  "selection": ttcc,       "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6ttlf",  "selection": ttlf,       "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },
{"name":"POPY6ttot",  "selection": ttothers,   "file": fileList["TT_powheg_pythia6"], "cx":cx[ttbarPOW]  ,"sumWeight": sumWeights["TT_powheg_pythia6"] },


{"name":"TTWlNu", "selection": "(1)", "file": fileList["ttWJetsToLNu"],  "cx":cx["ttWJetsToLNu"]   ,"sumWeight": sumWeights["ttWJetsToLNu"]   },
{"name":"TTWqq",  "selection": "(1)", "file": fileList["ttWJetsToQQ"],   "cx":cx["ttWJetsToQQ"]    ,"sumWeight": sumWeights["ttWJetsToQQ"]    },
{"name":"TTZll",  "selection": "(1)", "file": fileList["ttZToLLNuNu"],   "cx":cx["ttZToLLNuNu"]    ,"sumWeight": sumWeights["ttZToLLNuNu"]    },
{"name":"TTZqq",  "selection": "(1)", "file": fileList["ttZToQQ"],       "cx":cx["ttZToQQ"]        ,"sumWeight": sumWeights["ttZToQQ"]        },
                                                                                                                                                                                     
{"name":"STbt",   "selection": "(1)", "file": fileList["SingleTbar_t"],  "cx":cx["SingleTbar_t"]    ,"sumWeight": sumWeights["SingleTbar_t"]   },
{"name":"STt",    "selection": "(1)", "file": fileList["SingleTop_t"],   "cx":cx["SingleTop_t"]     ,"sumWeight": sumWeights["SingleTop_t"]    },
{"name":"STbtW",  "selection": "(1)", "file": fileList["SingleTbar_tW"], "cx":cx["SingleTbar_tW"]   ,"sumWeight": sumWeights["SingleTbar_tW"]  },
{"name":"STtW",   "selection": "(1)", "file": fileList["SingleTop_tW"],  "cx":cx["SingleTop_tW"]    ,"sumWeight": sumWeights["SingleTop_tW"]   },
{"name":"WW",     "selection": "(1)", "file": fileList["WW"],            "cx":cx["WW"]              ,"sumWeight": sumWeights["WW"]             },
{"name":"WZ",     "selection": "(1)", "file": fileList["WZ"],            "cx":cx["WZ"]              ,"sumWeight": sumWeights["WZ"]             },
{"name":"ZZ",     "selection": "(1)", "file": fileList["ZZ"],            "cx":cx["ZZ"]              ,"sumWeight": sumWeights["ZZ"]             },
                                                                                                                                               
{"name":"WJets",  "selection": "(1)", "file": fileList["WJets"],         "cx":cx["WJets"]           ,"sumWeight": sumWeights["WJets"]          },
                                                                                                                                               
{"name":"DYJets", "selection": "(1)", "file": fileList["DYJets"],        "cx":cx["DYJets"]          ,"sumWeight": sumWeights["DYJets"]         },
{"name":"DYJets10", "selection": "(1)","file": fileList["DYJets_10to50"],"cx":cx["DYJets_10to50"]   ,"sumWeight": sumWeights["DYJets_10to50"]  },

{"name":"ttH2non", "selection": "(1)", "file": fileList["ttH_nonbb"],  "cx":cx["ttH_nonbb"]         ,"sumWeight": sumWeights["ttH_nonbb"] },
{"name":"ttH2bb",  "selection": "(1)", "file": fileList["ttH_bb"],     "cx":cx["ttH_bb"]            ,"sumWeight": sumWeights["ttH_bb"]    },
]

#mcsamples = [ x for x in mcsamples if x["name"].find("POHP")>-1 or x["name"].find("POPY6")>-1 ]

mcsamples2=[
{"name":"DYJets", "selection": "(1)", "file": fileList["DYJets"],         "cx":cx["DYJets"]         ,"sumWeight": sumWeights["DYJets"]           },
{"name":"DYJets10", "selection": "(1)", "file": fileList["DYJets_10to50"],"cx":cx["DYJets_10to50"]  ,"sumWeight": sumWeights["DYJets_10to50"]    },
]
#datasamples=[]
datasamples=[

{"name":"MuMu1", "selection": "(1)", "file": fileList["DoubleMuon_Run2015C"]   },
{"name":"MuMu2", "selection": "(1)", "file": fileList["DoubleMuon_Run2015D"]   },

{"name":"ElEl1", "selection": "(1)", "file": fileList["DoubleEG_Run2015C"]     },
{"name":"ElEl2", "selection": "(1)", "file": fileList["DoubleEG_Run2015D"]     },

{"name":"MuEl1", "selection": "(1)", "file": fileList["MuonEG_Run2015C"]       },
{"name":"MuEl2", "selection": "(1)", "file": fileList["MuonEG_Run2015D"]       },

]
"""
