from ROOT import *
from os import listdir
from os.path import isfile, join


###################################################################
loc = "/store/user/youngjo/Cattools/v7-6-6v2/"
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


def sumWeight(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  htemp = TH1D("htempSS","",1,-2,2)
  #tree.Project("htempSS","1","weight*puweight")
  #tree.Project("htempSS","1","weight*puweight*mueffweight*eleffweight*tri")
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
    elif aa["name"] in ["TTJets_MG5","TTJets_aMC","TTJets_scaleup","TTJets_scaledown","TT_powheg","TT_powheg_scaledown","TT_powheg_scaleup","TT_powheg-herwigpp","TT_powheg_pythia6","TTLL_powheg"]:
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
sumWeights['DYJets']=80118462.0
sumWeights['DYJets_10to50']=22482569.0
sumWeights['DYJets_MG']=9004328.0
sumWeights['DYJets_MG_5to50']=8771481.0
sumWeights['WJets']=16521036.0
sumWeights['TTJets_MG5']=10166612.0
sumWeights['TTJets_aMC']=12754845.0
sumWeights['TTJets_scaleup']=14150600.0
sumWeights['TTJets_scaledown']=12798823.0
sumWeights['TT_powheg']=97994442.0
sumWeights['TT_powheg_scaledown']=9932876.0
sumWeights['TT_powheg_scaleup']=9919776.0
sumWeights['TTLL_powheg']=107163544.0
sumWeights['TT_powheg-herwigpp']=19383463.0
sumWeights['SingleTbar_tW']=999400.0
sumWeights['SingleTop_tW']=1000000.0
sumWeights['SingleTbar_t']=1630900.0
sumWeights['SingleTop_t']=3299200.0
sumWeights['SingleTop_s']=621946.0
sumWeights['WW']=988418.0
sumWeights['WZ']=1000000.0
sumWeights['ZZ']=985600.0
sumWeights['ttH_bb']=3772012.0
sumWeights['ttH_nonbb']=3945824.0
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

ttbarMCsamples = {  "MG5":"TTJets_MG5",         "AMC":"TTJets_aMC",            "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp", "POLL": "TTLL_powheg" 
                   ,"upPOW":"TT_powheg_scaleup", "dwPOW":"TT_powheg_scaledown" 
                }
#ttbarMCsamples = {"MG5":"TTJets_MG5","AMC","TTJets_aMC","POW":"TT_powheg","upPOW":"TT_powheg_scaleup","dwPOW":"TT_powheg_scaledown","POHP":"TT_powheg-herwigpp","POPY6":"TT_powheg_pythia6" }
bkgMCsamples = {"TTWlNu":"ttWJetsToLNu",  "TTWqq":"ttWJetsToQQ", "TTZll":"ttZToLLNuNu",   "TTZqq":"ttZToQQ",
#bkgMCsamples = {  "TTWqq":"ttWJetsToQQ",  "TTZqq":"ttZToQQ",
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



