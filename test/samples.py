from ROOT import *
from os import listdir
from os.path import isfile, join

#def files(mypath):
#  return [mypath+"/"+f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".root") ]

#loc = "../"
#loc = "/xrootd/store/user/youngjo/Cattools/v7-4-6v2/"
loc = "/store/user/youngjo/Cattools/v7-6-2v1/"
z  ="v3" # bkg
zz ="v1" # data
zzz="v3" # ttbar


#############################################
#############################################
#############################################
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

visible="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
ttbb = mAND("(NbJets20>=4)",visible)
ttb = mAND("(NbJets20==3)",visible)
ttcc = mAND("((NcJets20>=2) && !(NbJets20>=3))",visible)
ttlf = mAND("(!(NbJets20>=4) && !(NbJets20==3) && !(NcJets20>=2))",visible)

old_definition="""
ll = " (partonInPhaseLep==1 && NgenJet>=4 )"
ttbb = mAND(" (genTtbarId%100>52) ", ll)
ttb  = mAND(" (genTtbarId%100>50 && genTtbarId%100<53) ", ll)
ttc  = mAND(" (genTtbarId%100>40 && genTtbarId%100<43) ", ll)
ttcc = mAND(" (genTtbarId%100>42 && genTtbarId%100<49) ", ll)
ttlf = mAND(" (genTtbarId%100 ==0) ", ll)
"""

def op_(aaa):
  return "!(" + aaa + ")"

ttothers = op_(visible)
#########

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
    if aa["name"] in ["TTJets_MG5","TTJets_aMC","TTJets_scaleup","TTJets_scaledown","TT_powheg","TT_powheg_scaledown","TT_powheg_scaleup"]:
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


data = loadJson('dataset.json')
cx = {}
sumWeights={}
fileList={}
##############
sumWeights['DYJets']=81241963.0
sumWeights['DYJets_10to50']=22607337.5977
sumWeights['DYJets_MG']=15979580.1392
sumWeights['DYJets_MG_5to50']=0.0
sumWeights['WJets']=16521037.0153
sumWeights['TTJets_MG5']=12823209.1143
sumWeights['TTJets_aMC']=12589035.0
sumWeights['TTJets_scaleup']=14151457.0
sumWeights['TTJets_scaledown']=12784367.0
sumWeights['TT_powheg']=97958681.0
sumWeights['TT_powheg_scaledown']=9933507.0
sumWeights['TT_powheg_scaleup']=9920425.0
sumWeights['SingleTbar_tW']=999470.0
sumWeights['SingleTop_tW']=1000071.0
sumWeights['SingleTbar_t']=1630906.0
sumWeights['SingleTop_t']=3299208.0
sumWeights['SingleTop_s']=621947.962929
sumWeights['WW']=988491.589993
sumWeights['WZ']=1000015.0
sumWeights['ZZ']=985622.0
sumWeights['ttH_bb']=3772268.0
sumWeights['ttH_nonbb']=3946498.0
sumWeights['ttWJetsToQQ']=429626.0
sumWeights['ttWJetsToLNu']=129020.0
sumWeights['ttZToLLNuNu']=0.0
sumWeights['ttZToQQ']=350131.0
#############
if len(sumWeights.keys()) is 0 : 
  cx,sumWeights,fileList = getValues(data,True)
  import sys
  sys.exit()
else : 
  cx,fileList = getValues(data,False)

ttbarSP = [ 
   {"name":"all", "selection": "(1)"},  
   {"name":"ttbb", "selection":ttbb},
   {"name":"ttb", "selection":ttb},
   {"name":"ttcc", "selection":ttcc},
   {"name":"ttlf", "selection":ttlf},
   {"name":"ttot", "selection":ttothers}
]
noSP = [
   {"name":"all", "selection": "(1)"} 
]
def mcsampleSet(sample,SP):
  return {"name":sample, "sample":fileList[sample], "cx":cx[sample],"sumWeight":sumWeights[sample], "SP": SP }
def datasampleSet(sample,files):
  ff = []
  for f in files:
    if ff is []:
      f=fileList[f]
    else:
      f.append(fileList[f])
  return {"name":sample, "file":ff, "SP":noSP }

#############################################
#############################################
mcsamples=[]
for mc in sumWeights.keys():
  if mc.find("TT")>-1:
    mcsamples.append(mcsampleSet(mc,ttbarSP)
  else:
    mcsamples.append(mcsampleSet(mc,SP)

datasample=[]
datasample.append(datasampleSet("MuMu",["DoubleMuon_Run2015C","DoubleMuon_Run2015D"] ))
datasample.append(datasampleSet("ElEl",["DoubleEG_Run2015C","DoubleEG_Run2015D"]     ))
datasample.append(datasampleSet("MuEl",["MuonEG_Run2015C","MuonEG_Run2015D"]         ))
#############################################
#############################################

