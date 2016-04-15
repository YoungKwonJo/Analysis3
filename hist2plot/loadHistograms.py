#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

import sys
sys.path.append('../ntuple2hist')

#lumi = 2260.0
lumi = 2262.376
loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160415_ttbb_764/hist20160414/"

def loadHistogramMC(mc, mon, Step, Weight,DYsf):
  HN = mon["name"]
  Weight1= Weight
  if Weight is "Scale_Up":   Weight1="csvweight"
  if Weight is "Scale_Down": Weight1="csvweight"

  f = TFile.Open(loc+"/hist_"+Weight1+".root")
  name = mc['name']
  #print name+"  "+str(mc['cx'])+"   "
  scale = float(str(mc['cx']))*lumi
  #print name+"/"+Weight+"/h1_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1

  h1 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1).Clone("h1_"+name+"_"+Step+"mm"+"_"+Weight1)
  h2 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN+"_ee_"+Step+"_"+Weight1).Clone("h1_"+name+"_"+Step+"ee"+"_"+Weight1)
  h3 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN+"_em_"+Step+"_"+Weight1).Clone("h1_"+name+"_"+Step+"em"+"_"+Weight1)
  h1.AddBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX()+1))
  h2.AddBinContent(h2.GetNbinsX(),h2.GetBinContent(h2.GetNbinsX()+1))
  h3.AddBinContent(h3.GetNbinsX(),h3.GetBinContent(h3.GetNbinsX()+1))

  if h1.Integral()>0. :  h1.Scale(scale)
  if h2.Integral()>0. :  h2.Scale(scale)
  if h3.Integral()>0. :  h3.Scale(scale)
  isDY = name.find("DYJet")>-1
  if isDY : 
      h1.Scale(DYsf[Step][0])
      h2.Scale(DYsf[Step][1])


  histograms={"name":name,"hMM":copy.deepcopy(h1),"hEE":copy.deepcopy(h2),"hME":copy.deepcopy(h3)}
  f.Close()
  return histograms

def loadHistogramDATA(mon, Step, Weight):
  HN = mon["name"]
  WeightData = Weight
  WeightData2 = Weight
  #if not Weight in ["JES_Up","JES_Down"]:
  WeightData="CEN"
  WeightData2="CEN"
  f2 = TFile.Open(loc+"/hist_"+WeightData2+".root")
  for i in range(1):
    name_ = "DATA"
    #print "MuMu1/"+WeightData+"/h1_MuMu1_"+HN+"_mm_"+Step+"_"+WeightData+""

    h1 = f2.Get("MuMu1/"+WeightData+"/h1_MuMu1_"+HN+"_mm_"+Step+"_"+WeightData+"").Clone("h1_"+name_+"_"+Step+"mm"+"_"+WeightData+"")
    h2 = f2.Get("ElEl1/"+WeightData+"/h1_ElEl1_"+HN+"_ee_"+Step+"_"+WeightData+"").Clone("h1_"+name_+"_"+Step+"ee"+"_"+WeightData+"")
    h3 = f2.Get("MuEl1/"+WeightData+"/h1_MuEl1_"+HN+"_em_"+Step+"_"+WeightData+"").Clone("h1_"+name_+"_"+Step+"em"+"_"+WeightData+"")
    h1.Reset()
    h2.Reset()
    h3.Reset()
    for j in range(1,3):
      h11 = f2.Get("MuMu"+str(j)+"/"+WeightData+"/h1_MuMu"+str(j)+"_"+HN+"_mm_"+Step+"_"+WeightData+"")
      h22  = f2.Get("ElEl"+str(j)+"/"+WeightData+"/h1_ElEl"+str(j)+"_"+HN+"_ee_"+Step+"_"+WeightData+"")
      h33  = f2.Get("MuEl"+str(j)+"/"+WeightData+"/h1_MuEl"+str(j)+"_"+HN+"_em_"+Step+"_"+WeightData+"")
      h1.Add(h11)
      h2.Add(h22)
      h3.Add(h33)
  h1.AddBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX()+1))
  h2.AddBinContent(h2.GetNbinsX(),h2.GetBinContent(h2.GetNbinsX()+1))
  h3.AddBinContent(h3.GetNbinsX(),h3.GetBinContent(h3.GetNbinsX()+1))
     
  histograms = {"name":"DATA","hMM":copy.deepcopy(h1),"hEE":copy.deepcopy(h2),"hME":copy.deepcopy(h3)}
  f2.Close()
  return histograms

def mergesHistograms(selectedHists, oldHistograms):
  newHistograms = {}
  for hhh in oldHistograms.keys():
    if hhh in selectedHists:
      if len(newHistograms.keys())==0:
        import copy
        newHistograms=copy.deepcopy(oldHistograms[hhh])
      else:
        newHistograms["hMM"].Add(oldHistograms[hhh]["hMM"])
        newHistograms["hEE"].Add(oldHistograms[hhh]["hEE"])
        newHistograms["hME"].Add(oldHistograms[hhh]["hME"])
  return newHistograms





###############################
###############################
###############################
###for testing
def main():
  histograms = {}
  from mcsample_cfi import mcsamples
  from monitors_cfi import monitors,monitors2d
  from drellYanEstimation import DYsf

  mon = monitors[0]
  for mc in mcsamples:
    histograms[mc["name"]]=loadHistogramMC(mc, mon,"S6","csvweight",DYsf)
  histograms["DATA"]=loadHistogramDATA(mon,"S6","csvweight")
  #histograms["POWttbb"]["hMM"].Draw()
  c1 = TCanvas()
  c1.cd()
  histograms["DATA"]["hEE"].Draw()
  return c1,histograms

if __name__ == "__main__":
  test=main()

