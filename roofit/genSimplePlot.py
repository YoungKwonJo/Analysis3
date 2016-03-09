from ROOT import *

import sys
sys.path.append('../ntuple2hist')
from mcsample_cfi import fileList,ttbarSelections,ttbarMCsamples,mAND
from cut_cfi import cut_maker,ll_cuts


#######################
def getIt(tree,val, weight, sel):
  name = val["name"]
  htemp = TH1D(name,"",val["Nbin"],val["min"],val["max"])
  htemp.Reset()
  #tree.Project("htempD","1",weight+"*"+sel,"",10000)
  tree.Project(name,val["val"],weight+"*"+sel)
  return htemp #.Integral()

def loadTree(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  return chain

def makeoutput(outputname, h):
  fout = TFile(""+outputname,"RECREATE")
  for a in h.keys():
    dirA = fout.mkdir(a)
    dirA.cd()
    for b in h[a].keys():
      #dirB = dirA.mkdir(b)
      #dirB.cd()
      #for c in h[a][b]:
      h[a][b].Write()
  fout.Write()
  fout.Close()


################################
################################
################################
################################
##https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/TopQuarkAnalysis/TopTools/plugins/GenTtbarCategorizer.cc
hasCFromW="(genTtbarId>9000)"
isTtcc = "(genTtbarId%100>43 && genTtbarId%100<46)"
hadronic,semileptonic,dileptonic = "(allHadronic==1)", "(semiLeptonicM1==1)","(diLeptonicM1==1)"

ttcc={"woCW": "( !("+hasCFromW+") && "+isTtcc+" && "+semileptonic+" )",
      "wiCW": "( "+hasCFromW+" && "+isTtcc+" && "+semileptonic+" )"
     }

monitors = ["NJets20","NbJets20","NcJets20","NaddbJets20","NaddcJets20"]

filename = "TT_powheg"
tree = loadTree(fileList[filename])

if tree is not None : print "open the tree."
else                : print "fail to open the tree."

################################
################################
################################
allmons = {}
import copy
for x in monitors:
  mons = {}
  for y in ttcc.keys():
    val = {"name":"h"+x+y, "val":x, "Nbin":7, "min":0., "max":7. }
    h1=getIt(tree,val,"weight",ttcc[y])
    mons[y]=copy.deepcopy(h1)
  allmons[x]=copy.deepcopy(mons)

makeoutput("ttcc.root",allmons)


###write pickle
#import pickle
#output = open('data.pkl', 'wb')
#pickle.dump(allmons, output)
#output.close()

###read pickle
#import pprint, pickle
#pkl_file = open('data.pkl', 'rb')
#data1 = pickle.load(pkl_file)
#pkl_file.close()


