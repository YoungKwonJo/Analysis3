from ROOT import *

import sys
sys.path.append('../ntuple2hist')
from mcsample_cfi import fileList,ttbarSelections,ttbarMCsamples,mAND,op_
from cut_cfi import cut_maker,ll_cuts

def getIt(tree,htemp, weight, sel):
  htemp.Reset()
  #tree.Project("htempD","1",weight+"*"+sel,"",10000)
  tree.Project("htempD","1",weight+"*"+sel)
  return htemp.Integral()

def loadTree(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  return chain
def ttbarSelectionsFPS():
   fullphase ="(NaddJets20 >= 2 && diLeptonicP1==1)"
   #TTJJ = "(NaddJets20 >= 2 && diLeptonicM1==1)"
   ttbb = "(NaddbJets20 >= 2 && diLeptonicP1==1)"
   ttb = "(NaddJets20 >= 2 && diLeptonicP1==1 && NaddbJets20 == 1  && !(genTtbarId%100==52))"
   tt2b = "(NaddJets20 >= 2 && diLeptonicP1==1 && NaddbJets20 == 1 && (genTtbarId%100==52))"
   ttcc = "(NaddJets20 >= 2 && diLeptonicP1==1 && NaddcJets20 >= 2 && NaddbJets20==0 )"
   ttlf = "( !"+ttbb+" && !"+ttb+" && !"+tt2b+" && !"+ttcc+"  && NaddJets20 >= 2  && diLeptonicP1==1 )"
   ##ttlf = "( !"+ttbb+" && !"+ttb+" && !"+ttcc+"  && NaddJets20 >= 2 && diLeptonicM1==1)"
   ttot = op_(fullphase)
   return ttbb,ttb,tt2b,ttcc,ttlf,ttot

def ntuple2entries(filename,weight):
  #####selection
  hadronic,semileptonic,dileptonic     = "(allHadronic==1)", "(semiLeptonicM1==1)","(diLeptonicM1==1)"
  dileptonicP1,dileptonicP1not = "(semiLeptonicP1==1)","(semiLeptonicP1!=1)"
  #etc = "(!("+hadronic+"||"+semileptonic+"||"+dileptonic+"))"
  etc = "(!"+hadronic+"&& !"+semileptonic+"&& !"+dileptonic+")"
  #allttbar = {"hadroic":hadronic, "semileptonic":semileptonic, "dileptonic":dileptonic,"etc":etc }
  allttbar = {"dileptonicP1":dileptonicP1, "dileptonicP1not":dileptonicP1not }

  ttbb,ttb,tt2b,ttcc,ttlf,ttot = ttbarSelections(True)

  ttbbF,ttbF,tt2bF,ttccF,ttlfF,ttotF = ttbarSelectionsFPS()
  ttNN = { 
     "ttbb":ttbb, "ttb":ttb,  "tt2b":tt2b, "ttcc":ttcc, "ttlf":ttlf, "ttot":ttot, 
     "ttbbF":ttbbF,"ttbF":ttbF, "tt2bF":tt2bF, "ttccF":ttccF, "ttlfF":ttlfF, "ttotF":ttotF, 
  }
  S0,S6,S7=cut_maker(ll_cuts,0)['cut']["S0"],cut_maker(ll_cuts,6)['cut']["S6"],cut_maker(ll_cuts,7)['cut']["S7"]
  #ttEff = {"S0":S0,"S6":S6,"S7":S7}
  ttEff = {"S0":S0}#,"S6":S6,"S7":S7}

  tree = loadTree(fileList[filename])
  htemp = TH1D("htempD","",1,-20,20)
  
  summary = {}
  for x in allttbar.keys():
    summary[x] = getIt(tree,htemp,weight,allttbar[x])

  for x in ttEff.keys():
    summary2 = {}
    for y in ttNN.keys():
      #print x+y+": ("+str(ttEff[x])+"*"+str(ttNN[y])+")"
      summary2[y] =  getIt(tree,htemp,weight,"(("+ttEff[x]+")*("+ttNN[y]+"))")
    summary[x] = summary2
 
  return summary


#########################################################
#########################################################
allsummary = {}
weights = {"nom":"weight"
#  ,"Q2_Up1":"scaleWeightsUp[0]"
#  ,"Q2_Up2":"scaleWeightsUp[1]"
#  ,"Q2_Up3":"scaleWeightsUp[2]"
#  ,"Q2_Dw1":"scaleWeightsDown[0]"
#  ,"Q2_Dw2":"scaleWeightsDown[1]"
#  ,"Q2_Dw3":"scaleWeightsDown[2]"
}
weights2 = {"nom":"1","weight":"weight"}
#ttbarMCsamples = {  "MG5":"TTJets_MG5",         "AMC":"TTJets_aMC",            "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp" ,"upPOW":"TT_powheg_scaleup", "dwPOW":"TT_powheg_scaledown" }
#ttbarMCs=['dwPOW', 'POW', 'AMC', 'POHP', 'MG5', 'upPOW']
#ttbarMCs=['dwPOW', 'POW', 'upPOW']
ttbarMCs=['POW']
#ttbarMCs=['POW', 'AMC', 'MG5']

import sys
if len(sys.argv) < 2:
  print "no argument.."
  sys.exit()
xx = int(sys.argv[1])
yy = int(sys.argv[2])
x = ttbarMCs[xx]

#if x.find("MG5")>-1 : weights=weights2

for y,yyy in enumerate(weights.keys()):
  if y==yy:
    allsummaryA = {}
    #for x in ttbarMCsamples.keys():
    allsummaryA[x] = ntuple2entries(ttbarMCsamples[x],weights[yyy])
    allsummary[yyy]=allsummaryA

print x+"="+str(allsummary)


