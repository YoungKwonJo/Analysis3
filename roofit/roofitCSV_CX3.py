#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

import sys
sys.path.append('../ntuple2hist')


#lumi = 2262.376
lumi = 2318.278305882
loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/"
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160520_ttbb_764v2/hist20160520/"
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160415_ttbb_764/hist20160418_ctag/"
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160415_ttbb_764/hist20160418_ctag/MET/"

#lumi = 2260.
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160204_ttbb_roofit/histogram/"
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160224_763/histogram20160225/"
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160224_763/histogram20160302met/"

def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0)
  leg.SetLineColor(1)
  leg.SetTextFont(62)
  leg.SetTextSize(0.03)
  #leg.SetTextSize(0.03)

  leg.SetBorderSize(1)
  leg.SetLineStyle(1)
  leg.SetLineWidth(1)
  leg.SetLineColor(0)
  leg.SetTextSizePixels(18)

  return leg

def addLegendCMS():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"Preliminary")
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.25)
  tex2.SetY(0.97)
  tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  #tex2.Draw()

  return tex2

def addLegend(GEN):
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,GEN)
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.70)
  tex2.SetY(0.97)
  #tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  #tex2.Draw()

  return tex2

def addLegend2(text, xxx, yyy):
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,text)
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(xxx)
  tex2.SetY(yyy)
  #tex2.SetTextColor(2)
  tex2.SetTextFont(62)
  tex2.SetTextSize(0.03)
  tex2.SetTextSizePixels(16)

  return tex2

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("em")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("mm")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("ee")>-1 : ll2="e^{#mp}e^{#pm} channel"

  chtitle = TLatex(-20.,50.,ll2)
  chtitle.SetNDC()
  chtitle.SetTextAlign(12)
  chtitle.SetX(0.20)
  chtitle.SetY(0.85)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)
  chtitle.SetTextSizePixels(24)

  return chtitle

gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()

def loadHistogram(arg1, arg2, Step, Weight):
  return loadHistogram2(arg1,arg2,Step,0,Weight,{"Up":[],"Down":[]})

def getTTbarNames(GEN):
  return [ GEN+'ttbb', GEN+'ttot', GEN+'ttcc', GEN+'tt2b', GEN+'ttb', GEN+'ttlf']

def loadHistogram2(arg1, arg2, Step,Q2, Weight,Variation):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
  from mcsample_cfi import mcsamples 
  
  freeTTB  = False
  freeTTCC = False
  if int(arg1)==1 : freeTTB=True
  if int(arg1)==2 : freeTTCC=True
  if int(arg1)==3 : 
    freeTTCC=True
    freeTTB=True
  
  GEN="MG5"
  if int(arg2)==1 : GEN="POW"
  if int(arg2)==2 : GEN="POHP"
  if int(arg2)==3 : GEN="POPY6"
  if int(arg2)==4 : GEN="upPOW"
  if int(arg2)==5 : GEN="dwPOW"
  if int(arg2)==6 : GEN="AMC"

  histograms = {}
  histograms2 = {}

  Weight1= Weight
  if Weight.find("Q2")>-1:   Weight1="csvweight"
  if Weight.find("pdf")>-1:   Weight1="csvweight"
  if Weight.find("Scale")>-1: Weight1="csvweight"
  #scale=""
  if Weight.find("Scale_Up")>-1:   GEN="upPOW"
  if Weight.find("Scale_Down")>-1: GEN="dwPOW"

  WeightTTbar= Weight
  if Weight.find("Scale_Up")>-1:   WeightTTbar="csvweight"
  if Weight.find("Scale_Down")>-1: WeightTTbar="csvweight"

  ttbarsamples = [x for x in mcsamples if x['name'].find('tt')>-1]
  ttbarsamples2 = {}
  for x in ttbarsamples:
    ttbarsamples2[x["name"]]=x
  ttbarNames=getTTbarNames(GEN)

  TTbarFile=Weight
  if Weight.find("Q2")>-1 or Weight.find("pdf")>-1 :  TTbarFile="Q2pdf"
  f = TFile.Open(loc+"/hist_"+TTbarFile+".root")

  #for mc in ttbarsamples:
  for name in ttbarNames:
    #name = mc['name']
    if f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar) == None : continue
    #print "FINAL2:"+name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar
    h1 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar).Clone("h2_"+name+"_"+Step+"LL"+"_"+WeightTTbar)
    h2 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_ee_"+Step+"_"+WeightTTbar)
    h3 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_em_"+Step+"_"+WeightTTbar)
  
    #if h1.Integral()>0 :  h1.Scale(ttbarsamples2[name]['cx']*lumi)
    #if h2.Integral()>0 :  h2.Scale(ttbarsamples2[name]['cx']*lumi)
    #if h3.Integral()>0 :  h3.Scale(ttbarsamples2[name]['cx']*lumi)
    if h1.Integral()>0 :  h1.Scale(lumi)
    if h2.Integral()>0 :  h2.Scale(lumi)
    if h3.Integral()>0 :  h3.Scale(lumi)


    h1.Add(h2)
    h1.Add(h3)

    h1111 = "h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1
    #print "FINAL2:"+h1111
    h11 = TH1F(h1111,"",10,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1):
      h11 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1).Clone("h11_"+name+"_"+Step+"LL"+"_"+Weight1)
      h21 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_ee_"+Step+"_"+Weight1)
      h31 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_em_"+Step+"_"+Weight1)
      
      h11.Add(h21)
      h11.Add(h31)
  
    h1222 = "h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1
    #print "FINAL2:"+h1222
    h12 = TH1F(h1222,"",10,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1):
      h12 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1).Clone("h12_"+name+"_"+Step+"LL"+"_"+Weight1)
      h22 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_ee_"+Step+"_"+Weight1)
      h32 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_em_"+Step+"_"+Weight1)
      h12.Add(h22)
      h12.Add(h32)

    if name in Variation["Up"]:
      h1.Scale(1.5)
      h11.Scale(1.5)
      h12.Scale(1.5)

    if name in Variation["Down"]:
      h1.Scale(0.5)
      h11.Scale(0.5)
      h12.Scale(0.5)

    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12)}
    #histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}

  f.Close()

  signals1= [GEN+'ttbb', GEN+'ttb',GEN+'tt2b']
  signals2= [GEN+'ttcc', GEN+'ttlf']#, GEN+'ttot']
  backgrounds1= [GEN+"ttot"]
 
  ttcclfhist = histograms[GEN+'ttot']["h1"].Clone("ttcclfhist")
  ttcclfhist.Reset()

  for hh in signals1:
    h = histograms[hh]
    #h = histograms[hh]
    histograms2[hh]=h 
 
  for hh in signals2:
    h = histograms[hh]["h1"]
    #h = histograms[hh]["h1"]
    h2 = histograms[hh]
    ttcclfhist.Add(h)
    histograms2[hh]=h2
  histograms2[GEN+"ttcclf"]={"h1":copy.deepcopy(ttcclfhist),"exp":ttcclfhist.Integral()}

  for hh in backgrounds1:
    h = histograms[hh]
    #h = histograms[hh]
    histograms2[GEN+"ttot"]=h

  return loadHistogram22(freeTTB, freeTTCC,GEN, Step,Weight1, histograms2,Variation)

def loadHistogram22(freeTTB, freeTTCC,GEN, Step,Weight1, histograms2,Variation):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
  from mcsample_cfi import mcsamples

  #dy_ee_sf,dy_mm_sf = 1.22852835616,0.914936584631
  #dy_ee_sf,dy_mm_sf = 1.19890070419,0.892877376661
  dy_ee_sf,dy_mm_sf = 1.20526185054,1.01010320942

  #print "FINAL2:--------------------"

  histograms = {}
  #ttbarsamples = [x for x in mcsamples if x['name'].find('tt')>-1]
  bkgsamples = [x for x in mcsamples if x['name'].find('tt')==-1]

  f2 = TFile.Open(loc+"/hist_"+Weight1+".root")
  for mc in bkgsamples:
    name = mc['name']
    if f2.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1) == None : continue

    h1 = f2.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1).Clone("h2_"+name+"_"+Step+"LL"+"_"+Weight1)
    h2 = f2.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_ee_"+Step+"_"+Weight1)
    h3 = f2.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_em_"+Step+"_"+Weight1)
    if h1.Integral()>0 :  h1.Scale(mc['cx']*lumi)
    if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
    if h3.Integral()>0 :  h3.Scale(mc['cx']*lumi)
    if name.find("DYJets")>-1:
      h1.Scale(dy_mm_sf)
      h2.Scale(dy_ee_sf)

    h1.Add(h2)
    h1.Add(h3)

    if name in Variation["Up"]:
      h1.Scale(2.)
    if name in Variation["Down"]:
      h1.Scale(0.5)
 
    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}

  f2.Close()

  backgrounds2= ['TTWqq', 'TTZqq','TTWlNu','TTZll', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ']
  backgrounds3= [ 'DYJets','DYJets10']
  higgs= ['ttH2non', 'ttH2bb']
 
  bkghist = histograms2[GEN+'ttot']["h1"].Clone("bkghist")
  bkghist.Reset()
  ddbkghist = histograms2[GEN+'ttot']["h1"].Clone("ddbkghist")
  ddbkghist.Reset()
  
  for hh in backgrounds2:
    h = histograms[hh]["h1"]
    bkghist.Add(h)
    #print "FINAL "+hh
  histograms2["bkg"]={"h1":copy.deepcopy(bkghist),"exp":bkghist.Integral()}

  for hh in backgrounds3:
    h = histograms[hh]["h1"]
    ddbkghist.Add(h)
    #print "FINAL "+hh
  histograms2["ddbkg"]={"h1":copy.deepcopy(ddbkghist),"exp":ddbkghist.Integral()}

  return loadHistogram23(freeTTB, freeTTCC,GEN, Step,histograms2)
  
def loadHistogram23(freeTTB, freeTTCC,GEN, Step, histograms2):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
 
  #histograms2 = {}
  #for datesmaples
  WeightData="CEN"
  WeightData2="CEN"
  f2 = TFile.Open(loc+"/hist_"+WeightData2+".root")
  for i in range(1):
    name_ = "DATA"
    #color = mc['ColorLabel']['color'] 
    print "MuMu1/"+WeightData+"/h2_MuMu1_"+HN+"_mm_"+Step+"_"+WeightData+""

    h1 = f2.Get("MuMu1/"+WeightData+"/h2_MuMu1_"+HN+"_mm_"+Step+"_"+WeightData+"").Clone("h2_"+name_+"_"+Step+"LL"+"_"+WeightData+"")
    h1.Reset()
    for j in range(1,3):
      h11 = f2.Get("MuMu"+str(j)+"/"+WeightData+"/h2_MuMu"+str(j)+"_"+HN+"_mm_"+Step+"_"+WeightData+"")
      h2  = f2.Get("ElEl"+str(j)+"/"+WeightData+"/h2_ElEl"+str(j)+"_"+HN+"_ee_"+Step+"_"+WeightData+"")
      h3  = f2.Get("MuEl"+str(j)+"/"+WeightData+"/h2_MuEl"+str(j)+"_"+HN+"_em_"+Step+"_"+WeightData+"")
      h1.Add(h11)
      h1.Add(h2)
      h1.Add(h3)
    histograms2[name_]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}
  f2.Close()
  
  return histograms2, freeTTB, freeTTCC,GEN

##############################################
##############################################










##############################################
##############################################
def fitting(histograms, freeTTB, freeTTCC, GEN, onlyPrint, isPullTest):
  res = {}
  n_ttbb = histograms[GEN+"ttbb"]["exp"]
  n_ttb  = histograms[GEN+"ttb"]["exp"]
  n_tt2b  = histograms[GEN+"tt2b"]["exp"]
  #n_tt2b = histograms[GEN+"tt2b"]["exp"]
  n_ttcc = histograms[GEN+"ttcc"]["exp"]#+histograms[GEN+"ttc"]["exp"]
  #n_ttc = histograms[GEN+"ttc"]["exp"]
  n_ttlf = histograms[GEN+"ttlf"]["exp"]
  n_ttcclf = histograms[GEN+"ttcclf"]["exp"]
  n_ttot = histograms[GEN+"ttot"]["exp"]
  n_bkg = histograms["bkg"]["exp"]
  n_ddbkg = histograms["ddbkg"]["exp"]
  n_data = histograms["DATA"]["exp"]
 

  n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  n_ttbar = n_ttjj+n_ttot
  llratio_ = n_ttjj/n_ttbar

  print "n_ttbb:"+str(n_ttbb)
  print "n_ttb:"+str(n_ttb)
  print "n_tt2b:"+str(n_tt2b)
  #print "n_tt2b:"+str(n_tt2b)
  #print "n_ttc:"+str(n_ttc)
  print "n_ttcc:"+str(n_ttcc)
  print "n_ttlf:"+str(n_ttlf)
  print "n_ttot:"+str(n_ttot)
  print "n_bkg:"+str(n_bkg)
  print "n_ddbkg:"+str(n_ddbkg)
  print "n_data:"+str(n_data)
  print "FINAL2 :"+str(llratio_)

  if n_ttjj==0:  return False,False,False
  
  rttbb = n_ttbb/n_ttjj
  rttb  = n_ttb/n_ttjj
  rtt2b  = n_tt2b/n_ttjj
  #rtt2b = n_tt2b/n_ttjj
  rttcc = (n_ttcc)/n_ttjj
  
  x=RooRealVar("x","x",histograms["bkg"]["h1"].GetXaxis().GetXmin(),histograms["bkg"]["h1"].GetXaxis().GetXmax()) 
  y=RooRealVar("y","y",histograms["bkg"]["h1"].GetYaxis().GetXmin(),histograms["bkg"]["h1"].GetYaxis().GetXmax()) 
  
##########
  dilepBr = 0.1049580955
  ttbarCX = 831.76

  #POWHEG
  ttbbAcc=0.022
  ttjjAcc=0.020
  ttbbEff=0.2692 
  ttjjEff=0.1165 
###########

  ttjjCXFS=n_ttjj/(lumi*ttjjEff*ttjjAcc)#*ttjjAcp#*lumi/1000.#*n_ttjj
  ttbbCXFS=n_ttbb/(lumi*ttbbEff*ttbbAcc)#*ttbbAcp#*lumi/1000.#*n_ttbb
  ttjjCXVS=n_ttjj/(lumi*ttjjEff)#*ttjjAcp#*lumi/1000.#*n_ttjj
  ttbbCXVS=n_ttbb/(lumi*ttbbEff)#*ttbbAcp#*lumi/1000.#*n_ttbb
 
  print "aaaaaaaaaaaaaaaaaaaaaaaaaa"
#  print ttjjCX
#  print ttbbCX
  print "FINAL2 ttjjCXFS : "+str(ttjjCXFS)
  print "aaaaaaaaaaaaaaaaaaaaaaaaaa"

  precxttjjVS=5.1 #VS
  precxttjjVS=ttjjCXVS*1000. #VS
  precxttbbVS=0.070 #VS
  precxttbbVS=ttbbCXVS*1000. #VS
  precxttjjFS=257. #FS
  precxttjjFS=ttjjCXFS*1000.
  precxttbbFS=3.2 #FS
  precxttbbFS=ttbbCXFS*1000. #FS

  accttbb   = RooRealVar(       "accttbb","normalization factor",           ttbbAcc, ttbbAcc, ttbbAcc) 
  accttjj   = RooRealVar(       "accttjj","normalization factor",           ttjjAcc, ttjjAcc, ttjjAcc)
  ttjj_ttbarratio   = RooRealVar(       "ttjjttbarratio","normalization factor", 0.307036, 0.307036, 0.307036)

  #cxttbb   =RooRealVar(    "cxttbb",                "cxttbb",           precxttbb, precxttbb*0.5, precxttbb*2.5) 
  effttbb   = RooRealVar(       "effttbb","normalization factor",           ttbbEff, ttbbEff, ttbbEff) 

  RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
  RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
  Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
  RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);

  fsrttbb_=rttbb/ttbbEff*ttjjEff/ttbbAcc*ttjjAcc
  vsrttbb_=rttbb/ttbbEff*ttjjEff#/ttbbAcc*ttjjAcc

  fsrttbb=RooRealVar("fsrttbb","fsrttbb",fsrttbb_,fsrttbb_*0.5,fsrttbb_*2.5)
  vsrttbb=RooRealVar("vsrttbb","vsrttbb",vsrttbb_,vsrttbb_*0.5,vsrttbb_*2.5)

  cxttjj     = RooRealVar(       "cxttjj","normalization factor",           precxttjjFS, precxttjjFS*0.7, precxttjjFS*1.4)
  cxttjjVS     = RooRealVar(       "cxttjjVS","normalization factor",           precxttjjVS, precxttjjVS*0.7, precxttjjVS*1.4)

  effttjj   = RooRealVar(       "effttjj","normalization factor",           ttjjEff, ttjjEff, ttjjEff) 

  ###############################
  #k      = RooFormulaVar("k","number of ttjj events after fitting","@0/@1",    RooArgList(cxttjj,ttjj_ttbarratio) )
  #fsig  =RooFormulaVar("fsig",          "fsig","@0*@1/@2*@3/@4",RooArgList(fsrttbb,effttbb,effttjj,accttbb,accttjj) )

  k      = RooFormulaVar("k","number of ttjj events after fitting","@0/@1/@2",    RooArgList(cxttjjVS,ttjj_ttbarratio,accttjj) )
  fsig  = RooFormulaVar("fsig",          "fsig","@0*@1/@2",RooArgList(vsrttbb,effttbb,effttjj) )
  ###############################

  fsig2con  =RooFormulaVar("fsig2con",          "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )  # constraint fsig2 with fsig
  fsig3con  =RooFormulaVar("fsig3con",          "fsig3","@0/@1*@2",RooArgList(fsig,RttbbReco,Rtt2bReco) )  # constraint fsig3 with fsig


  nttjj =RooRealVar(    "nttjj","number of ttjj events",                            n_ttjj , n_ttjj, n_ttjj)
  #cxnttjj=RooFormulaVar("cxnttjj","number of ttjj events after fitting","cx*nttjj",    RooArgList(ttjjcx,nttjj) )
  knttjj=RooFormulaVar("knttjj","number of ttjj events after fitting","k*nttjj",    RooArgList(k,nttjj) )
  nttot =RooRealVar(    "nttot","number of ttot events",                            n_ttot , n_ttot, n_ttot)
  knttot=RooFormulaVar("knttot","number of ttot events after fitting","k*nttot",    RooArgList(k,nttot) )
  nbkg  =RooRealVar(     "nbkg","number of background events",                      n_bkg , n_bkg, n_bkg)
  nddbkg  =RooRealVar(   "nddbkg","number of background events",                    n_ddbkg , n_ddbkg, n_ddbkg)
  knbkg=RooFormulaVar("knbkg","number of background events after fitting","k*nbkg", RooArgList(k,nbkg) )
  
  ######
  nttcc =RooRealVar(   "nttcc","number of ttcc events",                         n_ttcc , n_ttcc, n_ttcc)
  knttcc=RooFormulaVar("knttcc","number of ttcc events after fitting","k*nttcc",RooArgList(k,nttcc) )
  #####
 
  #histogram
  xyArg = RooArgList(x, y)
  data    = RooDataHist("data",    "data set with (x)",   xyArg, histograms["DATA"]["h1"])
  #ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   xyArg, test_ttbb)
  ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   xyArg, histograms[GEN+"ttbb"]["h1"])
  ttb     = RooDataHist("ttb",     "ttb  set with (x)",   xyArg, histograms[GEN+"ttb"]["h1"])
  tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",  xyArg, histograms[GEN+"tt2b"]["h1"])
  ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   xyArg, histograms[GEN+"ttcc"]["h1"] )
  ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   xyArg, histograms[GEN+"ttlf"]["h1"])
  ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", xyArg, histograms[GEN+"ttcclf"]["h1"])

  ttot    = RooDataHist("ttot",    "ttot set with (x)",   xyArg, histograms[GEN+"ttot"]["h1"])
  bkg     = RooDataHist("bkg",     "bkg  set with (x)",   xyArg, histograms["bkg"]["h1"])
  ddbkg   = RooDataHist("ddbkg",   "ddbkg  set with (x)", xyArg, histograms["ddbkg"]["h1"])

  #print "ttbar type: "+str(type(ttbar))
  #print "rooArglist(x):"+str(type(RooArgList(x)))
  
  #pdf
  ttbbpdf      = RooHistPdf("ttbbpdf",     "ttbbpdf",      RooArgSet(RooArgList(x,y)), ttbb)
  ttbpdf       = RooHistPdf("ttbpdf",      "ttbpdf",       RooArgSet(RooArgList(x,y)), ttb)
  tt2bpdf      = RooHistPdf("tt2bpdf",     "tt2bpdf",      RooArgSet(RooArgList(x,y)), tt2b)
  ttccpdf      = RooHistPdf("ttccpdf",     "ttccpdf",      RooArgSet(RooArgList(x,y)), ttcc)
  ttlfpdf      = RooHistPdf("ttlfpdf",     "ttlfpdf",      RooArgSet(RooArgList(x,y)), ttlf)
  ttcclfpdf    = RooHistPdf("ttcclfpdf",   "ttcclfpdf",    RooArgSet(RooArgList(x,y)), ttcclf)
  ttotpdf      = RooHistPdf("ttotpdf",     "ttotpdf",      RooArgSet(RooArgList(x,y)), ttot)
  bkgpdf       = RooHistPdf("bkgpdf",      "bkgpdf",       RooArgSet(RooArgList(x,y)), bkg)
  ddbkgpdf     = RooHistPdf("ddbkgpdf",    "ddbkgpdf",     RooArgSet(RooArgList(x,y)), ddbkg)
  
  model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttcclfpdf), RooArgList(fsig,fsig2con,fsig3con))
  
  model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf,ddbkgpdf),              RooArgList(knttjj,knttot,nbkg,nddbkg)) # k*bkg
  model2.fitTo(data)

  ################
  ################
  pt = addLegendCMS()
  pt2 = addDecayMode("LL")
  pt3 = addLegend("Madgraph")
  if GEN == "POW": pt3=addLegend("Powheg")
  if GEN == "AMC": pt3=addLegend("aMC@NLO")

  #########################################################
  #########################################################
  #########################################################
  #########################################################
  #########################################################
  
  
  
  #########################################################
  #########################################################
  #########################################################
  #########################################################
  lineKKK = TLine(0,0,0,0)
  lineKKK.SetLineColor(kBlue)
  lineKKK.SetLineWidth(3)
  ################
  ################
  #cR10 = TCanvas("R10", "R", 1)#500, 500)
  cR10 = TCanvas("R10", "R", 800,400)#500, 500)
  cR10.Divide(2,1)
  cR10.cd(2)

  nll = model2.createNLL(data)
  #nll = model2.createNLL(ttlf)
  #RooMinuit(nk1).migrad() 
  RFrame = vsrttbb.frame()
  nll.plotOn(RFrame,RooFit.ShiftToZero()) 
  RFrame.SetMaximum(4.);RFrame.SetMinimum(0)
  RFrame.GetXaxis().SetTitle("R_{VS} ")
  RFrame.SetTitle("")
  RFrame.Draw()

  boxR = TBox(vsrttbb_-0.001/2.,0,vsrttbb_+0.001/2.,4.)
  ci = TColor.GetColor("#d0efd0")
  boxR.SetFillColor(ci)
  boxR.Draw()

  line = TLine(RFrame.GetXaxis().GetXmin() ,0.5,RFrame.GetXaxis().GetXmax(),0.5)
  line.SetLineColor(kRed)
  line.Draw()
  
  lineTbb = TLine(vsrttbb_,RFrame.GetMaximum(),vsrttbb_,0)
  lineTbb.SetLineStyle(2)
  lineTbb.Draw()

  l1 = make_legend(0.39,0.76,0.93,0.88)
  l1.AddEntry(lineTbb,"prefit: R_{VS}="+str(roudV(vsrttbb_)),"l")
  l1.AddEntry(lineKKK,"fit: R_{VS}="+str(roudV(vsrttbb.getVal()))+" #pm "+str(roudV(vsrttbb.getError() ))+"","l")

  l1.SetTextSize(0.04)
  l1.SetFillColor(0)
  l1.SetLineColor(0)
  l1.Draw()

  cenTtbbCX= vsrttbb.getVal()*cxttjjVS.getVal()
  errTtbbCX=sqrt( vsrttbb.getError()/vsrttbb.getVal()*vsrttbb.getError()/vsrttbb.getVal() + cxttjjVS.getError()/cxttjjVS.getVal()*cxttjjVS.getError()/cxttjjVS.getVal() )*cenTtbbCX

  cR10.cd(1).Update()

  ##################
  ##################
  ##################
  ##################
  ##################
  cR10.cd(1)
  nllK = model2.createNLL(data)
  RFrameK = cxttjjVS.frame()
  nllK.plotOn(RFrameK,RooFit.ShiftToZero())

  RFrameK.SetMaximum(4.);RFrameK.SetMinimum(0)
  RFrameK.GetXaxis().SetTitle("#sigma_{VS}^{t#bar{t}jj}")
  RFrameK.SetTitle("")
  RFrameK.Draw()
  print "RFameK: "+str(type(RFrameK))
  box = TBox(precxttjjVS-0.5/2.,0,precxttjjVS+0.5/2.,4.)
  #ci = TColor.GetColor("#d0efd0")
  box.SetFillColor(ci)
  box.Draw() 

  lineTbbK = TLine(precxttjjVS,RFrameK.GetMaximum(),precxttjjVS,0)
  lineTbbK.SetLineStyle(2)
  lineTbbK.Draw()
  
  
  l1K = make_legend(0.49,0.76,0.93,0.88)
  l1K.AddEntry(lineTbbK,"prefit: #sigma_{VS}^{t#bar{t}jj} = "+str(roudV(precxttjjVS)),"l")
  l1K.AddEntry(lineKKK,"fit: #sigma_{VS}^{t#bar{t}jj}="+str(roudV(cxttjjVS.getVal()))+" #pm "+str(roudV(cxttjjVS.getError() ))+"","l")

  l1K.SetTextSize(0.04)
  l1K.SetFillColor(0)
  l1K.SetLineColor(0)
  l1K.Draw()
 
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  ptBB  = addLegend2("prefit: #sigma_{FS}^{t#bar{t}bb} = "+str(roudV(precxttbbVS)),0.52,0.68)
  ptBB2 = addLegend2("fit: #sigma_{FS}^{t#bar{t}bb} = "+str(roudV(cenTtbbCX))+" #pm "+str(roudV( errTtbbCX ) ),0.52,0.62)
  ptBB2.Draw()
  ptBB.Draw()

  lineK = TLine(RFrameK.GetXaxis().GetXmin() ,0.5,RFrameK.GetXaxis().GetXmax(),0.5)
  lineK.SetLineColor(kRed)
  lineK.Draw()



  cR10.cd(2).Update()
  cR10.Print("plots2/"+GEN+"_VS.eps")
  cR10.Print("plots2/"+GEN+"_VS.png")
  
 ###########################
  return cR10#, cR00#, cR11, cR12, cNLLContourb,cNLLContourc, cN, cN2


################
################
################
################
################
################
################
################
def quardsum(aaa):
  bbb=0.0
  for i in aaa:
    bbb+= i*i
  return sqrt(bbb)
################
################
################
################
################
################
################
################
################
################

def roudV(val1):
  val =abs(val1)
  if val > 100 :
    return int(round(val))
  elif val > 1 : 
    return round(val*100)/100
  else :
    nom=10000.
    if val>0.1    : nom=10000.
    elif val>0.01 : nom=100000.
    elif val>0.001: nom=1000000.
    elif val>0.0001: nom=10000000.
    else          : nom=1000000000.

    return round(val*nom)/nom

def sumV(data,step,candi):
  sumV =0.
  if step == "": 
    for i in candi:  sumV +=data[i] 
  else         : 
    for i in candi:  sumV +=data[step][i]
  return sumV


##############################################################################
##############################################################################
##############################################################################
import sys
if len(sys.argv) < 3:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)
arg2 = sys.argv[2] # MG5, POW

arg3="0"
if len(sys.argv) > 3:
  arg3 = sys.argv[3]



Step="S6"


histograms,freeTTB,freeTTCC,GEN=loadHistogram(arg1, arg2,Step,"csvweight")
orig_r,orig_err = 0.,0. 

from math import *
cR10 = fitting(histograms, freeTTB, freeTTCC, GEN,False,False)
###################

