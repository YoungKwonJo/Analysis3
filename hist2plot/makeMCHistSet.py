#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

import sys
sys.path.append('../ntuple2hist')

from loadHistograms import loadHistogramMC,loadHistogramDATA,mergesHistograms

def makeMCHistSet(histograms):
  ttV   = ["TTWlNu","TTWqq","TTZll","TTZqq"]
  ST    = ["STbt","STt","STbtW","STtW"]
  VV    = ["WW","WZ","ZZ"]
  WJets = ["WJets"]
  ZJets = ["DYJets","DYJets10"]
  ttH   = ["ttH2non","ttH2bb"]
  ######
  MG5ttbar = ["MG5ttbb","MG5ttb","MG5tt2b","MG5ttcc","MG5ttlf","MG5ttot"]
  AMCttbar = ["AMCttbb","AMCttb","AMCtt2b","AMCttcc","AMCttlf","AMCttot"]
  POWttbar = ["POWttbb","POWttb","POWtt2b","POWttcc","POWttlf","POWttot"]
  POHPttbar = ["POHPttbb","POHPttb","POHPtt2b","POHPttcc","POHPttlf","POHPttot"]
  
  upPOWttbar = ["upPOWttbb","upPOWttb","upPOWtt2b","upPOWttcc","upPOWttlf","upPOWttot"]
  dwPOWttbar = ["dwPOWttbb","dwPOWttb","dwPOWtt2b","dwPOWttcc","dwPOWttlf","dwPOWttot"]
  ###################
  Bkg1   = ST+VV+WJets+ZJets
  MCtot1 = POWttbar+Bkg1
  MCtot2 = MG5ttbar+Bkg1
  MCtot3 = AMCttbar+Bkg1
  MCtot4 = POHPttbar+Bkg1
  ttbMerge = ["POWttb","POWtt2b"]
  
  histograms2 = {}
  histograms2["ttbb"] = { "h1":histograms["POWttbb"],   "FillColor":"#660000", "LineColor":"#000000",  "label":"t#bar{t}+b#bar{b}      ",  "label2":"$t\\bar{t}+b\\bar{b}$"  }
  histograms2["ttb"]  = { "h1":mergesHistograms(ttbMerge, histograms),    "FillColor":"#ffcc00", "LineColor":"#000000",  "label":"t#bar{t}+bj        "     ,  "label2":"$t\\bar{t}+bj$"          }
  #histograms2["ttb"]  = { "h1":histograms["POWttb"],    "FillColor":"#ffcc00", "LineColor":"#000000",  "label":"t#bar{t}+b        "     ,  "label2":"$t\\bar{t}+b$"          }
  #histograms2["tt2b"] = { "h1":histograms["POWtt2b"],   "FillColor":"#ffee00", "LineColor":"#000000",  "label":"t#bar{t}+2b        "    ,  "label2":"$t\\bar{t}+2b$"         }
  histograms2["ttcc"] = { "h1":histograms["POWttcc"],   "FillColor":"#cc6600", "LineColor":"#000000",  "label":"t#bar{t}+c#bar{c}      ",  "label2":"$t\\bar{t}+c\\bar{c}$"  }
  histograms2["ttlf"] = { "h1":histograms["POWttlf"],   "FillColor":"#ff0000", "LineColor":"#000000",  "label":"t#bar{t}+lf       "     ,  "label2":"$t\\bar{t}+lf$"         }
  histograms2["ttot"] = { "h1":histograms["POWttot"],   "FillColor":"#ff6565", "LineColor":"#000000",  "label":"t#bar{t} others"        ,  "label2":"$t\\bar{t}$ others"     }
  #histograms2["ttall"] = {"h1":histograms["POWttal"],   "FillColor":"#ff6565", "LineColor":"#000000",  "label":"t#bar{t} all"          ,  "label2":"$t#bar{t$} all"            }

  histograms2["MG5ttbb"] = { "h1":histograms["MG5ttbb"],   "FillColor":"#660000", "LineColor":"#000000",  "label":"t#bar{t}+b#bar{b}      " ,  "label2":"$t\\bar{t}+b\\bar{b}$:MG5" }
  histograms2["MG5ttb"]  = { "h1":histograms["MG5ttb"],    "FillColor":"#ffcc00", "LineColor":"#000000",  "label":"t#bar{t}+b        "      ,  "label2":"$t\\bar{t}+b$:MG5"         }
  histograms2["MG5tt2b"] = { "h1":histograms["MG5tt2b"],   "FillColor":"#ffee00", "LineColor":"#000000",  "label":"t#bar{t}+2b        "     ,  "label2":"$t\\bar{t}+2b$:MG5"        }
  histograms2["MG5ttcc"] = { "h1":histograms["MG5ttcc"],   "FillColor":"#cc6600", "LineColor":"#000000",  "label":"t#bar{t}+c#bar{c}      " ,  "label2":"$t\\bar{t}+c\\bar{c}$:MG5" }
  histograms2["MG5ttlf"] = { "h1":histograms["MG5ttlf"],   "FillColor":"#ff0000", "LineColor":"#000000",  "label":"t#bar{t}+lf       "      ,  "label2":"$t\\bar{t}+lf$:MG5"        }
  histograms2["MG5ttot"] = { "h1":histograms["MG5ttot"],   "FillColor":"#ff6565", "LineColor":"#000000",  "label":"t#bar{t} others"         ,  "label2":"$t\\bar{t}$ others:MG5"    }

  histograms2["Singlet"] = {"h1":mergesHistograms(ST,    histograms),    "FillColor":"#ff00ff",  "LineColor":"#000000", "label":"Single t"            , "label2":"Single top-${\\rm t}W$"           } 
  histograms2["VV"]      = {"h1":mergesHistograms(VV,    histograms),    "FillColor":"#ffffff",  "LineColor":"#000000", "label":"VV            "      , "label2":"VV"     }
  histograms2["WJets"]   = {"h1":mergesHistograms(WJets, histograms),    "FillColor":"#33cc33",  "LineColor":"#000000", "label":"WJets      "         , "label2":"$W+jets$"        }
  histograms2["ZJets"]   = {"h1":mergesHistograms(ZJets, histograms),    "FillColor":"#3366ff",  "LineColor":"#000000", "label":"DYJets    "          , "label2":"$Z/\\gamma* \\rightarrow ll$"         }
  histograms2["ttV"]     = {"h1":mergesHistograms(ttV,   histograms),    "FillColor":"#7676ff",  "LineColor":"#000000", "label":"t#bar{t}V          " , "label2":"$t\\bar{t}+V$"}
  histograms2["ttH"]     = {"h1":mergesHistograms(ttH,   histograms),    "LineColor":"#7676ff",  "FillColor":"#ffffff", "label":"t#bar{t}H         "  , "label2":"$t\\bar{t}+H$" }
  
  histograms2["DATA"]    = {"h1":histograms["DATA"],                     "LineColor":"#000000",  "FillColor":"#ffffff", "label":"DATA "    ,"MarkerStyle":20,  "MarkerSize": 0.7, "label22":"DATA"        }

  histograms2["MCtot1"]  = {"h1":mergesHistograms(MCtot1,  histograms),  "LineColor":"#afc6c6",  "FillColor":"#afc6c6",  "label":""         ,"FillStyle": 1001,   "label2":"MC Total" } 
  histograms2["MCtot2"]  = {"h1":mergesHistograms(MCtot2,  histograms),  "LineColor":"#59d354",  "FillColor":"#ffffff",  "label":"Madgraph+PYTHIA8" ,"LineStyle": 3 ,"label2":"MC Total(MG5)"   } 
  histograms2["MCtot3"]  = {"h1":mergesHistograms(MCtot3,  histograms),  "LineColor":"#ff00ff",  "FillColor":"#ffffff",  "label":"aMC@NLO+PYTHIA8"   ,"LineStyle": 2,"label2":"MC Total(AMC)"    } 
  histograms2["MCtot4"]  = {"h1":mergesHistograms(MCtot4,  histograms),  "LineColor":"#0000ff",  "FillColor":"#ffffff",  "label":"POWHEG+HERWIG++"   ,"LineStyle": 5,"label2":"MC Total(POHP)"    } 
  #ttbarlist = ["ttbb","ttb","tt2b","ttcc","ttlf","ttot"]
  #ttbarlist = ["ttbb","tt2b","ttb","ttcc","ttlf","ttot"]
  ttbarlist = ["ttbb","ttb","ttcc","ttlf","ttot"]
  MG5ttbarlist = ["MG5ttbb","MG5ttb","MG5tt2b","MG5ttcc","MG5ttlf","MG5ttot"]
  bkglist=["ttV","Singlet","VV","WJets","ZJets"]
  fullmc =["MCtot1"]
  others =["MCtot2","MCtot4",'MCtot3']
  statlist= ttbarlist+MG5ttbarlist+bkglist+fullmc
  statlabels={}
  for x in histograms2.keys():
    if x in statlist:
      statlabels[x] = histograms2[x]["label2"]
  plotSet = {"ttbars":ttbarlist, "bkg":bkglist, "fullmc":fullmc, "others":others, "mg5":MG5ttbarlist, "labels":statlabels}
  return histograms2,plotSet

def load1stHistograms(mon,step,Weight,SFbyFitting):
  from drellYanEstimation import DYsf 
  from mcsample_cfi import mcsamples
  histograms = {}
  for mc in mcsamples:
    histograms[mc["name"]]=loadHistogramMC(mc, mon,step,Weight,DYsf,SFbyFitting)
  histograms["DATA"]=loadHistogramDATA(mon,step,Weight)

  return histograms

######################################
######################################
######################################
def main():
  from monitors_cfi import monitors,monitors2d
  mon = monitors[7]
  SFbyFitting={'ttbbSF':1.0,'ttcclfSF':1.0,'k':1.0}
  histograms=load1stHistograms(mon,"S2","csvweight",SFbyFitting)
  #c1 = TCanvas()
  #histograms["TTZqq"]["hMM"].Draw()
  #histograms["DATA"]["hEE"].Draw()
  histograms2,plotSet=makeMCHistSet(histograms)
  
  
  gROOT.SetStyle("Plain")
  gStyle.SetOptFit(1000)
  gStyle.SetOptStat("emruo")
  gStyle.SetOptStat(kFALSE)
  gStyle.SetPadTickY(1)
  gStyle.SetPadTickX(1)
  
  gROOT.ProcessLine(".L tdrStyle.C")
  setTDRStyle()
  c1 = TCanvas()
  #c1.Divide(2,2)
  c1.cd()
  histograms2["MCtot1"]["h1"]["hMM"].SetLineColor( TColor.GetColor(histograms2["MCtot1"]["LineColor"]) )
  histograms2["MCtot1"]["h1"]["hMM"].Draw()
  #c1.cd(2)
  #histograms2["MCtot1"]["h1"]["hEE"].Draw()
  #c1.cd(3)
  #histograms2["MCtot1"]["h1"]["hME"].Draw()
  return c1,histograms2

if __name__ == "__main__":
  test=main()


