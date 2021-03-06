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

  leg.SetBorderSize(1)
  leg.SetLineStyle(1)
  leg.SetLineWidth(1)
  leg.SetLineColor(0)

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
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)

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

def th1_2to1(a,b):
  nbins = a.GetNbinsX()
  aa = TH1D(a.GetName()+"_M2","",nbins*2,0,2)
  for i in range(1,nbins+1):
    aa.SetBinContent(i,a.GetBinContent(i))
    aa.SetBinError(i,a.GetBinError(i))
    aa.SetBinContent(i+nbins,a.GetBinContent(i))
    aa.SetBinError(i+nbins,a.GetBinError(i))
  return aa

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

  sumweightQ2={'dwPOW_csvweight': 9932876.0, 'POW_csvweight': 97994442.0, 'upPOW_Q2_Up1': 9721877.978248205, 'upPOW_Q2_Up3': 8656597.607850373, 'dwPOW_Q2_Dw3': 11328951.66248878, 'dwPOW_Q2_Dw2': 11099336.392136984, 'dwPOW_Q2_Dw1': 10193564.465720307, 'upPOW_csvweight': 9919776.0, 'upPOW_Q2_Up2': 8878141.199428499, 'POW_Q2_Dw1': 100562130.05494703, 'POW_Q2_Dw2': 109501436.23855484, 'POW_Q2_Dw3': 111759839.10910639, 'POW_Q2_Up1': 96043292.78107499, 'POW_Q2_Up2': 87702904.5710082, 'POW_Q2_Up3': 85517519.10829923}
  sumweightPdf={'POW_pdf_N29': 98551830.6053606, 'POW_pdf_N28': 99598280.46658012, 'POW_pdf_N27': 98666952.35351756, 'POW_pdf_N26': 101748323.31598747, 'POW_pdf_N25': 96844004.09411715, 'POW_pdf_N24': 97782367.35702756, 'POW_pdf_N23': 95894214.21326047, 'POW_pdf_N22': 100464072.08043212, 'POW_pdf_N21': 95199979.48248267, 'POW_pdf_N20': 97438290.94294289, 'POW_csvweight': 97994442.0, 'POW_pdf_N38': 96112640.84684622, 'POW_pdf_N39': 96878566.76326233, 'POW_pdf_N34': 101802924.92296988, 'POW_pdf_N35': 98194634.1194146, 'POW_pdf_N36': 99978208.32182862, 'POW_pdf_N37': 97615407.85049275, 'POW_pdf_N30': 96354078.79097807, 'POW_pdf_N31': 96159101.61553779, 'POW_pdf_N32': 96855208.96789327, 'POW_pdf_N33': 95384641.85393983, 'POW_pdf_N89': 97077536.79626238, 'POW_pdf_N88': 100415986.17329398, 'POW_pdf_N81': 96598068.55737919, 'POW_pdf_N80': 97177967.20678662, 'POW_pdf_N83': 97868829.23414183, 'POW_pdf_N82': 100155203.41608378, 'POW_pdf_N85': 98297635.95897709, 'POW_pdf_N84': 98089342.36574581, 'POW_pdf_N87': 99099231.0502919, 'POW_pdf_N86': 99243157.29338214, 'POW_pdf_N16': 101465563.28766279, 'POW_pdf_N17': 99614508.97088099, 'POW_pdf_N14': 99784791.65061507, 'POW_pdf_N15': 98941630.87511921, 'POW_pdf_N12': 99399129.99975419, 'POW_pdf_N13': 99104851.3048476, 'POW_pdf_N10': 95246373.36174244, 'POW_pdf_N11': 98640001.53970493, 'POW_pdf_N18': 97870853.7345613, 'POW_pdf_N19': 99854268.63383387, 'POW_pdf_N98': 100124011.14032471, 'POW_pdf_N99': 100621514.92164667, 'POW_pdf_N96': 98344821.98690891, 'POW_pdf_N97': 97453028.60258128, 'POW_pdf_N94': 99867306.54921076, 'POW_pdf_N95': 98621622.84010206, 'POW_pdf_N92': 99161761.5299398, 'POW_pdf_N93': 98731070.7084023, 'POW_pdf_N90': 97504746.90689792, 'POW_pdf_N91': 97228630.26348674, 'POW_pdf_N4': 93180882.882662, 'POW_pdf_N5': 98926406.95481464, 'POW_pdf_N6': 97704373.55684854, 'POW_pdf_N7': 99036146.27863346, 'POW_pdf_N0': 95315260.08691841, 'POW_pdf_N1': 99000132.78099975, 'POW_pdf_N2': 99140427.20519423, 'POW_pdf_N3': 96196165.1015825, 'POW_pdf_N8': 98902352.81427607, 'POW_pdf_N9': 96520766.76980096, 'POW_pdf_N63': 99048180.3272661, 'POW_pdf_N62': 97874085.06152086, 'POW_pdf_N61': 97891405.4983091, 'POW_pdf_N60': 97827312.737427, 'POW_pdf_N67': 97837528.95441943, 'POW_pdf_N66': 101999082.6173971, 'POW_pdf_N65': 97066299.68566135, 'POW_pdf_N64': 98980833.69343676, 'POW_pdf_N69': 97689246.46488144, 'POW_pdf_N68': 97230505.25365736, 'POW_pdf_N70': 96151187.50086647, 'POW_pdf_N71': 97559564.75098796, 'POW_pdf_N72': 96383445.99381408, 'POW_pdf_N73': 98969681.46032143, 'POW_pdf_N74': 98005487.92826845, 'POW_pdf_N75': 94103628.09761263, 'POW_pdf_N76': 96000614.47217196, 'POW_pdf_N77': 99691472.68413058, 'POW_pdf_N78': 97437937.84729382, 'POW_pdf_N79': 97362872.35524903, 'POW_pdf_N45': 96649552.93303049, 'POW_pdf_N44': 96937117.18954912, 'POW_pdf_N47': 98379938.12413085, 'POW_pdf_N46': 98323349.32754843, 'POW_pdf_N41': 97339266.53237465, 'POW_pdf_N40': 97119962.57813382, 'POW_pdf_N43': 96981969.68850677, 'POW_pdf_N42': 95876936.95071954, 'POW_pdf_N49': 97561568.04547541, 'POW_pdf_N48': 98876572.8305867, 'POW_pdf_N58': 99367488.69632721, 'POW_pdf_N59': 97274244.5207445, 'POW_pdf_N52': 97110977.65266345, 'POW_pdf_N53': 98650389.20430166, 'POW_pdf_N50': 97065116.68381652, 'POW_pdf_N51': 97063435.94435525, 'POW_pdf_N56': 98931668.47177102, 'POW_pdf_N57': 97121701.34585664, 'POW_pdf_N54': 97211679.66039707, 'POW_pdf_N55': 98832916.00498164, 'POW_pdf_N101': 99037545.47031403, 'POW_pdf_N100': 96568415.54683125}

  #for mc in ttbarsamples:
  for name in ttbarNames:
    #name = mc['name']
    if f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar) == None : continue
    #print "FINAL2:"+name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar
    h1 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+WeightTTbar).Clone("h2_"+name+"_"+Step+"LL"+"_"+WeightTTbar)
    h2 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_ee_"+Step+"_"+WeightTTbar)
    h3 = f.Get(name+"/"+WeightTTbar+"/h2_"+name+"_"+HN+"_em_"+Step+"_"+WeightTTbar)
  
    if h1.Integral()>0 :  h1.Scale(ttbarsamples2[name]['cx']*lumi)
    if h2.Integral()>0 :  h2.Scale(ttbarsamples2[name]['cx']*lumi)
    if h3.Integral()>0 :  h3.Scale(ttbarsamples2[name]['cx']*lumi)
    h1.Add(h2)
    h1.Add(h3)
    if WeightTTbar.find("Q2")>-1 or WeightTTbar.find("pdf")>-1:
      if Weight.find("pdf")>-1: h1.Scale(1./sumweightPdf['POW_'+WeightTTbar]*sumweightQ2['POW_csvweight'])
      elif name.find("dw")>-1 : h1.Scale(1./sumweightQ2['dwPOW_'+WeightTTbar]*sumweightQ2['dwPOW_csvweight'])
      elif name.find("up")>-1 : h1.Scale(1./sumweightQ2['upPOW_'+WeightTTbar]*sumweightQ2['upPOW_csvweight'])
      else                    : h1.Scale(1./sumweightQ2['POW_'+WeightTTbar]*sumweightQ2['POW_csvweight'])

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

    if h11.Integral()>0 :  h11.Scale(ttbarsamples2[name]['cx']*lumi)
    if h21.Integral()>0 :  h21.Scale(ttbarsamples2[name]['cx']*lumi)
    if h31.Integral()>0 :  h31.Scale(ttbarsamples2[name]['cx']*lumi)
    if h12.Integral()>0 :  h12.Scale(ttbarsamples2[name]['cx']*lumi)
    if h22.Integral()>0 :  h22.Scale(ttbarsamples2[name]['cx']*lumi)
    if h32.Integral()>0 :  h32.Scale(ttbarsamples2[name]['cx']*lumi)
 

    if name in Variation["Up"]:
      h1.Scale(1.5)
      h11.Scale(1.5)
      h12.Scale(1.5)

    if name in Variation["Down"]:
      h1.Scale(0.5)
      h11.Scale(0.5)
      h12.Scale(0.5)

    h333 = th1_2to1(h11,h12)
    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12),"h333":copy.deepcopy(h333)}
    #histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}

  f.Close()

  signals1= [GEN+'ttbb', GEN+'ttb',GEN+'tt2b']
  signals2= [GEN+'ttcc', GEN+'ttlf']#, GEN+'ttot']
  backgrounds1= [GEN+"ttot"]
 
  ttcclfhist = histograms[GEN+'ttot']["h1"].Clone("ttcclfhist")
  ttcclfhist3rd = histograms[GEN+'ttot']["h11"].Clone("ttcclfhist3rd")
  ttcclfhist4th = histograms[GEN+'ttot']["h12"].Clone("ttcclfhist4th")
  ttcclfhist333 = histograms[GEN+'ttot']["h333"].Clone("ttcclfhist333")
  ttcclfhist.Reset()
  ttcclfhist3rd.Reset()
  ttcclfhist4th.Reset()
  ttcclfhist333.Reset()

  for hh in signals1:
    h = histograms[hh]
    #h = histograms[hh]
    #h333 = th1_2to1(h["h12"],h["h12"])
    #h["h333"]=copy.deepcopy(h333)
    histograms2[hh]=h 
 
  for hh in signals2:
    h = histograms[hh]["h1"]
    h3rd = histograms[hh]["h11"]
    h4th = histograms[hh]["h12"]
    h333 = histograms[hh]["h333"]
    h2 = histograms[hh]
    ttcclfhist.Add(h)
    ttcclfhist3rd.Add(h3rd)
    ttcclfhist4th.Add(h4th)
    ttcclfhist333.Add(h333)

    histograms2[hh]=h2

  #hcclfhist333 = th1_2to1(ttcclfhist3rd,ttcclfhist4th)
  histograms2[GEN+"ttcclf"]={"h1":copy.deepcopy(ttcclfhist),"exp":ttcclfhist.Integral(),"h11":copy.deepcopy(ttcclfhist3rd),"h12":copy.deepcopy(ttcclfhist4th),"h333":copy.deepcopy(ttcclfhist333)}

  for hh in backgrounds1:
    h = histograms[hh]
    #h = histograms[hh]
    #h333 = th1_2to1(h["h12"],h["h12"])
    #h["h333"]=copy.deepcopy(h333)
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

    h1111 = "h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1
    #print "FINAL2:"+h1111
    h11 = TH1F(h1111,"",10,0,1)
    if None != f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1):
      h11 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1).Clone("h11_"+name+"_"+Step+"LL"+"_"+Weight1)
      h21 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_ee_"+Step+"_"+Weight1)
      h31 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_em_"+Step+"_"+Weight1)
    if h11.Integral()>0 :  h11.Scale(mc['cx']*lumi)
    if h21.Integral()>0 :  h21.Scale(mc['cx']*lumi)
    if h31.Integral()>0 :  h31.Scale(mc['cx']*lumi)
    if name.find("DYJets")>-1:
      h11.Scale(dy_mm_sf)
      h21.Scale(dy_ee_sf)

      h11.Add(h21)
      h11.Add(h31)
  
    h1222 = "h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1
    #print "FINAL2:"+h1222
    h12 = TH1F(h1222,"",10,0,1)
    if None != f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1):
      h12 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1).Clone("h12_"+name+"_"+Step+"LL"+"_"+Weight1)
      h22 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_ee_"+Step+"_"+Weight1)
      h32 = f2.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_em_"+Step+"_"+Weight1)
    if h12.Integral()>0 :  h12.Scale(mc['cx']*lumi)
    if h22.Integral()>0 :  h22.Scale(mc['cx']*lumi)
    if h32.Integral()>0 :  h32.Scale(mc['cx']*lumi)
    if name.find("DYJets")>-1:
      h12.Scale(dy_mm_sf)
      h22.Scale(dy_ee_sf)

      h12.Add(h22)
      h12.Add(h32)


    if name in Variation["Up"]:
      h1.Scale(2.)
      h11.Scale(2.)
      h12.Scale(2.)
    if name in Variation["Down"]:
      h1.Scale(0.5)
      h11.Scale(0.5)
      h12.Scale(0.5)
 
    h333 = th1_2to1(h11,h12)
    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12),"h333":copy.deepcopy(h333)}

  f2.Close()

  backgrounds2= ['TTWqq', 'TTZqq','TTWlNu','TTZll', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ']
  backgrounds3= [ 'DYJets','DYJets10']
  higgs= ['ttH2non', 'ttH2bb']
 
  bkghist = histograms2[GEN+'ttot']["h1"].Clone("bkghist")
  bkghist3rd = histograms2[GEN+'ttot']["h11"].Clone("bkghist")
  bkghist4th = histograms2[GEN+'ttot']["h12"].Clone("bkghist2")
  bkghist333 = histograms2[GEN+'ttot']["h333"].Clone("bkghist333")
  bkghist.Reset()
  bkghist3rd.Reset()
  bkghist4th.Reset()
  bkghist333.Reset()
  ddbkghist = histograms2[GEN+'ttot']["h1"].Clone("ddbkghist")
  ddbkghist3rd = histograms2[GEN+'ttot']["h11"].Clone("ddbkghist")
  ddbkghist4th = histograms2[GEN+'ttot']["h12"].Clone("ddbkghist")
  ddbkghist333 = histograms2[GEN+'ttot']["h333"].Clone("ddbkghist333")
  ddbkghist.Reset()
  ddbkghist3rd.Reset()
  ddbkghist4th.Reset()
  ddbkghist333.Reset()
  
  for hh in backgrounds2:
    h = histograms[hh]["h1"]
    h11 = histograms[hh]["h11"]
    h12 = histograms[hh]["h12"]
    h333 = histograms[hh]["h333"]
    bkghist.Add(h)
    bkghist3rd.Add(h11)
    bkghist4th.Add(h12)
    bkghist333.Add(h333)

    #print "FINAL "+hh

  #hbkghist333 = th1_2to1(bkghist3rd,bkghist4th)
  histograms2["bkg"]={"h1":copy.deepcopy(bkghist),"exp":bkghist.Integral(),"h11":copy.deepcopy(bkghist3rd),"h12":copy.deepcopy(bkghist4th),"h333":copy.deepcopy(bkghist333) }

  for hh in backgrounds3:
    h = histograms[hh]["h1"]
    h11 = histograms[hh]["h11"]
    h12 = histograms[hh]["h12"]
    h333 = histograms[hh]["h333"]
    ddbkghist.Add(h)
    ddbkghist3rd.Add(h11)
    ddbkghist4th.Add(h12)
    ddbkghist333.Add(h333)
    #print "FINAL "+hh
  #hddbkghist333 = th1_2to1(ddbkghist3rd,ddbkghist4th)
  histograms2["ddbkg"]={"h1":copy.deepcopy(ddbkghist),"exp":ddbkghist.Integral(),"h11":copy.deepcopy(ddbkghist3rd),"h12":copy.deepcopy(ddbkghist4th),"h333":copy.deepcopy(ddbkghist333)}

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
    h3rd = f2.Get("MuMu1/"+WeightData+"/h1_MuMu1_"+HN1+"_mm_"+Step+"_"+WeightData+"").Clone("h11_"+name_+"_"+Step+"LL"+"_"+WeightData+"")
    h4th = f2.Get("MuMu1/"+WeightData+"/h1_MuMu1_"+HN2+"_mm_"+Step+"_"+WeightData+"").Clone("h12_"+name_+"_"+Step+"LL"+"_"+WeightData+"")

    h1.Reset()
    h3rd.Reset()
    h4th.Reset()
    for j in range(1,3):
      h11 = f2.Get("MuMu"+str(j)+"/"+WeightData+"/h2_MuMu"+str(j)+"_"+HN+"_mm_"+Step+"_"+WeightData+"")
      h2  = f2.Get("ElEl"+str(j)+"/"+WeightData+"/h2_ElEl"+str(j)+"_"+HN+"_ee_"+Step+"_"+WeightData+"")
      h3  = f2.Get("MuEl"+str(j)+"/"+WeightData+"/h2_MuEl"+str(j)+"_"+HN+"_em_"+Step+"_"+WeightData+"")
      h1.Add(h11)
      h1.Add(h2)
      h1.Add(h3)
      h111 = f2.Get("MuMu"+str(j)+"/"+WeightData+"/h1_MuMu"+str(j)+"_"+HN1+"_mm_"+Step+"_"+WeightData+"")
      h21  = f2.Get("ElEl"+str(j)+"/"+WeightData+"/h1_ElEl"+str(j)+"_"+HN1+"_ee_"+Step+"_"+WeightData+"")
      h31  = f2.Get("MuEl"+str(j)+"/"+WeightData+"/h1_MuEl"+str(j)+"_"+HN1+"_em_"+Step+"_"+WeightData+"")
      h3rd.Add(h111)
      h3rd.Add(h21)
      h3rd.Add(h31)
      h112 = f2.Get("MuMu"+str(j)+"/"+WeightData+"/h1_MuMu"+str(j)+"_"+HN2+"_mm_"+Step+"_"+WeightData+"")
      h22  = f2.Get("ElEl"+str(j)+"/"+WeightData+"/h1_ElEl"+str(j)+"_"+HN2+"_ee_"+Step+"_"+WeightData+"")
      h32  = f2.Get("MuEl"+str(j)+"/"+WeightData+"/h1_MuEl"+str(j)+"_"+HN2+"_em_"+Step+"_"+WeightData+"")
      h4th.Add(h112)
      h4th.Add(h22)
      h4th.Add(h32)
      
    h333 = th1_2to1(h3rd,h4th)
    histograms2[name_]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h3rd),"h12":copy.deepcopy(h4th),"h333":copy.deepcopy(h333)}
  f2.Close()
  
  return histograms2, freeTTB, freeTTCC,GEN

##############################################
##############################################
##############################################
##############################################
def resultPrint(result, freeTTB, freeTTCC, GEN):
  return resultPrintNew2(result, freeTTB, freeTTCC, GEN, True)

def resultPrintNew2(result, freeTTB, freeTTCC, GEN, isPrint):
  if isPrint : print "FINAL3: ----------------------   "
  if isPrint : print "FINAL3: MC:"+ str(GEN)
  fsig = result["fsig"]
  rttbb = result["rttbb"]
  recoR      = fsig.getVal()
  recoRerror = fsig.getError()
  if isPrint : print "FINAL3: prefit: R="+str(roudV(rttbb))
  if isPrint : print "FINAL3: R = "+ str(roudV(recoR))+" $\pm$ "+str(roudV(recoRerror))+" "
  #return false

  #"""
  recoR2=1.
  recoR3=1.
  recoR2error=0.0
  recoR3error=0.0
  if freeTTB:
    if isPrint : print "FINAL3: freeTTB : "+str(freeTTB)
    fsig2 = result["fsig2"]
    fsig3 = result["fsig3"]
    rttb = result["rttb"]
    rtt2b = result["rtt2b"]
    recoR2      = fsig2.getVal()
    recoR3      = fsig3.getVal()
    recoR2error = fsig2.getError()
    recoR3error = fsig3.getError()
    if isPrint : print "FINAL3: prefit: R2="+str(roudV(rttb))
    if isPrint : print "FINAL3: $R2 = "+ str(roudV(recoR2))+" \pm "+str(roudV(recoR2error))+"$"
    if isPrint : print "FINAL3: prefit: R3="+str(roudV(rtt2b))
    if isPrint : print "FINAL3: $R3 = "+ str(roudV(recoR3))+" \pm "+str(roudV(recoR3error))+"$"
  else:
    if isPrint : print "FINAL3: freeTTB : "+str(freeTTB)
    fsig2con = result["fsig2con"]
    fsig3con = result["fsig3con"]
    recoR2      = fsig2con.getVal()
    recoR3      = fsig3con.getVal()
    rttb = result["rttb"]
    rtt2b = result["rtt2b"]
    #recoR2error = fsig2con.getError()
    if isPrint : print "FINAL3: prefit: R2="+str(roudV(rttb))
    if isPrint : print "FINAL3: $R2 = "+ str(roudV(recoR2))#+" \pm "+str(roudV(recoR2error))+"$"
    if isPrint : print "FINAL3: prefit: R3="+str(roudV(rtt2b))
    if isPrint : print "FINAL3: $R3 = "+ str(roudV(recoR3))#+" \pm "+str(roudV(recoR3error))+"$"
  
  recoRcc=1.
  recoRccerror=0.0
  if freeTTCC:
    if isPrint : print "FINAL3: freeTTCC : "+str(freeTTCC)
    fsigcc = result["fsigcc"]
    rttcc = result["rttcc"]
    recoRcc      = fsigcc.getVal()
    recoRccerror = fsigcc.getError()
    if isPrint : print "FINAL3: prefit: Rcc="+str(roudV(rttcc))
    if isPrint : print "FINAL3: $Rcc = "+ str(roudV(recoRcc))+" \pm "+str(roudV(recoRccerror))+"$"
  else:
    if isPrint : print "FINAL3: freeTTCC : "+str(freeTTCC)
    #recoRcc      = fsigcc.getVal()
    #recoRccerror = fsigcc.getError()
    rttcc = result["rttcc"]
    if isPrint : print "FINAL3: prefit: Rcc="+str(roudV(rttcc))
    #if isPrint : print "FINAL3: $Rcc = "+ str(roudV(recoRcc))+" \pm "+str(roudV(recoRccerror))+"$"
  
  
  k = result["k"]
  kVal      = k.getVal()
  kValerror = k.getError()
  if isPrint : print "FINAL3: $k = "+str(roudV(kVal))+" \pm "+str(roudV(kValerror))+"$"
  result2 = {
      "recoR":copy.deepcopy(recoR), "recoRerror":copy.deepcopy(recoRerror),
      "recoR2":copy.deepcopy(recoR2), "recoR2error":copy.deepcopy(recoR2error),
      "recoR3":copy.deepcopy(recoR3), "recoR3error":copy.deepcopy(recoR3error),
      "recoRcc":copy.deepcopy(recoRcc), "recoRccerror":copy.deepcopy(recoRccerror),
      "kVal":copy.deepcopy(kVal), "kValerror":copy.deepcopy(kValerror)
      }

  return result2
  #"""
################
################
################
################
################
def newTemplate(h1):
  #test_ttbb = histograms[GEN+"ttbb"]["h1"].Clone()
  test_h1 = h1.Clone(h1.GetName()+"_test")
  test_h1.Reset()
  for i in range(int(h1.GetEntries())):
    xxx, yyy = Double(0), Double(0)
    h1.GetRandom2(xxx, yyy)
    test_h1.Fill(xxx,yyy)
  return copy.deepcopy(test_h1)

################
################
def fitting(histograms, freeTTB, freeTTCC, GEN, onlyPrint, isPullTest):
  res = {}
  h1_data  = histograms["DATA"]["h333"]
  h1_ttbb  = histograms[GEN+"ttbb"]["h333"]
  h1_ttb   = histograms[GEN+"ttb"]["h333"]
  h1_tt2b  = histograms[GEN+"tt2b"]["h333"]
  h1_ttcc  = histograms[GEN+"ttcc"]["h333"]
  h1_ttcclf= histograms[GEN+"ttcclf"]["h333"]
  h1_ttlf  = histograms[GEN+"ttlf"]["h333"]
  h1_ttot  = histograms[GEN+"ttot"]["h333"]
  h1_bkg   = histograms["bkg"]["h333"]
  h1_ddbkg = histograms["ddbkg"]["h333"]
  xmin = histograms["bkg"]["h333"].GetXaxis().GetXmin()
  xmax = histograms["bkg"]["h333"].GetXaxis().GetXmax()
  
  """
  h1_data.Rebin(2) 
  h1_ttbb.Rebin(2)  
  h1_ttb.Rebin(2)   
  h1_tt2b.Rebin(2)  
  h1_ttcc.Rebin(2)  
  h1_ttcclf.Rebin(2)
  h1_ttlf.Rebin(2)  
  h1_ttot.Rebin(2)  
  h1_bkg.Rebin(2)   
  h1_ddbkg.Rebin(2) 
  """

  h1_data.Scale(0.5) 
  h1_ttbb.Scale(0.5)  
  h1_ttb.Scale(0.5)   
  h1_tt2b.Scale(0.5)  
  h1_ttcc.Scale(0.5)  
  h1_ttcclf.Scale(0.5)
  h1_ttlf.Scale(0.5)  
  h1_ttot.Scale(0.5)  
  h1_bkg.Scale(0.5)   
  h1_ddbkg.Scale(0.5) 
 
  
  n_ttbb   = h1_ttbb.Integral() 
  n_ttb    = h1_ttb.Integral()
  n_tt2b   = h1_tt2b.Integral()
  #n_tt2b  = h1_tt2b.Integral()
  n_ttcc   = h1_ttcc.Integral()
  #n_ttc   = h1_ttc.Integral()
  n_ttlf   = h1_ttlf.Integral()
  n_ttcclf = h1_ttcclf.Integral()
  n_ttot   = h1_ttot.Integral()
  n_bkg    = h1_bkg.Integral()
  n_ddbkg  = h1_ddbkg.Integral()
  n_data   = h1_data.Integral()
   

  """
  n_ttbb = histograms[GEN+"ttbb"]["exp"]*2.
  n_ttb  = histograms[GEN+"ttb"]["exp"]*2.
  n_tt2b  = histograms[GEN+"tt2b"]["exp"]*2.
  #n_tt2b = histograms[GEN+"tt2b"]["exp"]
  n_ttcc = histograms[GEN+"ttcc"]["exp"]*2. #+histograms[GEN+"ttc"]["exp"]
  #n_ttc = histograms[GEN+"ttc"]["exp"]
  n_ttlf = histograms[GEN+"ttlf"]["exp"]*2.
  n_ttcclf = histograms[GEN+"ttcclf"]["exp"]*2.
  n_ttot = histograms[GEN+"ttot"]["exp"]*2.
  n_bkg = histograms["bkg"]["exp"]*2.
  n_ddbkg = histograms["ddbkg"]["exp"]*2.
  n_data = histograms["DATA"]["exp"]*2.
  """

  n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  n_ttbar = n_ttjj+n_ttot
  
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
  #print "FINAL2 :"+str(n_ttjj)

  if n_ttjj==0:  return False,False,False
  
  rttbb = n_ttbb/n_ttjj
  rttb  = n_ttb/n_ttjj
  rtt2b  = n_tt2b/n_ttjj
  #rtt2b = n_tt2b/n_ttjj
  rttcc = (n_ttcc)/n_ttjj
  
  #xmin = histograms["bkg"]["h1"].GetXaxis().GetXmin()
  #xmax = histograms["bkg"]["h1"].GetXaxis().GetXmax()
  x=RooRealVar("x","x",xmin,xmax) 
  #x=RooRealVar("x","x",xmin,xmax) 
  #y=RooRealVar("y","y",histograms["bkg"]["h1"].GetYaxis().GetXmin(),histograms["bkg"]["h1"].GetYaxis().GetXmax()) 
  
  RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
  RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
  Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
  RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);
  
  fsig   =RooRealVar(    "fsig",                "fsig",           rttbb, 0.0, 0.18) 
  fsig2con  =RooFormulaVar("fsig2con",          "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )  # constraint fsig2 with fsig
  fsig3con  =RooFormulaVar("fsig3con",          "fsig3","@0/@1*@2",RooArgList(fsig,RttbbReco,Rtt2bReco) )  # constraint fsig3 with fsig
  fsig2  =RooRealVar(   "fsig2",                "fsig2",          rttb, 0.0, 0.3)  # free fsig2
  fsig3  =RooRealVar(   "fsig3",                "fsig3",          rtt2b, 0.0, 0.3)  # free fsig3
  fsig32con  =RooFormulaVar(   "fsig32con",    "fsig32con", "@0/@1*@2",RooArgList(fsig2,RttbReco,Rtt2bReco))  # free fsig32 with fsig2
  fsigcc =RooRealVar(  "fsigcc",              "fsigcc",           rttcc, 0.0, 0.4)  # free fsigcc
  k      =RooRealVar(       "k","normalization factor",           1, 0.5, 2) 
  
  nttjj =RooRealVar(    "nttjj","number of ttjj events",                            n_ttjj , n_ttjj, n_ttjj)
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
  xyArg = RooArgList(x)
  #xyArg = RooArgList(x, y)
  data    = RooDataHist("data",    "data set with (x)",   xyArg, h1_data)
  #ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   xyArg, test_ttbb)
  ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   xyArg, h1_ttbb)
  ttb     = RooDataHist("ttb",     "ttb  set with (x)",   xyArg, h1_ttb)
  tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",   xyArg, h1_tt2b)
  ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   xyArg, h1_ttcc)
  ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   xyArg, h1_ttlf)
  ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", xyArg, h1_ttcclf)

  ttot    = RooDataHist("ttot",    "ttot set with (x)",   xyArg, h1_ttot)
  bkg     = RooDataHist("bkg",     "bkg  set with (x)",   xyArg, h1_bkg)
  ddbkg   = RooDataHist("ddbkg",   "ddbkg  set with (x)", xyArg, h1_ddbkg)

  """
  data    = RooDataHist("data",    "data set with (x)",   xyArg, histograms["DATA"]["h333"]        )
  ttbb    = RooDataHist("ttbb",    "ttbb set with (x)",   xyArg, histograms[GEN+"ttbb"]["h333"]    )
  ttb     = RooDataHist("ttb",     "ttb  set with (x)",   xyArg, histograms[GEN+"ttb"]["h333"]     )
  tt2b    = RooDataHist("tt2b",    "tt2b set with (x)",   xyArg, histograms[GEN+"tt2b"]["h333"]    )
  ttcc    = RooDataHist("ttcc",    "ttcc set with (x)",   xyArg, histograms[GEN+"ttcc"]["h333"]    )
  ttlf    = RooDataHist("ttlf",    "ttlf set with (x)",   xyArg, histograms[GEN+"ttlf"]["h333"]    )
  ttcclf  = RooDataHist("ttcclf",  "ttcclf set with (x)", xyArg, histograms[GEN+"ttcclf"]["h333"]  )
                                                                                                
  ttot    = RooDataHist("ttot",    "ttot set with (x)",   xyArg, histograms[GEN+"ttot"]["h333"]    )
  bkg     = RooDataHist("bkg",     "bkg  set with (x)",   xyArg, histograms["bkg"]["h333"]         )
  ddbkg   = RooDataHist("ddbkg",   "ddbkg  set with (x)", xyArg, histograms["ddbkg"]["h333"]       )
  """

  #print "ttbar type: "+str(type(ttbar))
  #print "rooArglist(x):"+str(type(RooArgList(x)))
  
  #pdf
  """ 
  ttbbpdf      = RooHistPdf("ttbbpdf",     "ttbbpdf",      RooArgSet(RooArgList(x,y)), ttbb)
  ttbpdf       = RooHistPdf("ttbpdf",      "ttbpdf",       RooArgSet(RooArgList(x,y)), ttb)
  tt2bpdf      = RooHistPdf("tt2bpdf",     "tt2bpdf",      RooArgSet(RooArgList(x,y)), tt2b)
  ttccpdf      = RooHistPdf("ttccpdf",     "ttccpdf",      RooArgSet(RooArgList(x,y)), ttcc)
  ttlfpdf      = RooHistPdf("ttlfpdf",     "ttlfpdf",      RooArgSet(RooArgList(x,y)), ttlf)
  ttcclfpdf    = RooHistPdf("ttcclfpdf",   "ttcclfpdf",    RooArgSet(RooArgList(x,y)), ttcclf)
  ttotpdf      = RooHistPdf("ttotpdf",     "ttotpdf",      RooArgSet(RooArgList(x,y)), ttot)
  bkgpdf       = RooHistPdf("bkgpdf",      "bkgpdf",       RooArgSet(RooArgList(x,y)), bkg)
  ddbkgpdf     = RooHistPdf("ddbkgpdf",    "ddbkgpdf",     RooArgSet(RooArgList(x,y)), ddbkg)
  """
  ttbbpdf      = RooHistPdf("ttbbpdf",     "ttbbpdf",      RooArgSet(RooArgList(x)), ttbb)
  ttbpdf       = RooHistPdf("ttbpdf",      "ttbpdf",       RooArgSet(RooArgList(x)), ttb)
  tt2bpdf      = RooHistPdf("tt2bpdf",     "tt2bpdf",      RooArgSet(RooArgList(x)), tt2b)
  ttccpdf      = RooHistPdf("ttccpdf",     "ttccpdf",      RooArgSet(RooArgList(x)), ttcc)
  ttlfpdf      = RooHistPdf("ttlfpdf",     "ttlfpdf",      RooArgSet(RooArgList(x)), ttlf)
  ttcclfpdf    = RooHistPdf("ttcclfpdf",   "ttcclfpdf",    RooArgSet(RooArgList(x)), ttcclf)
  ttotpdf      = RooHistPdf("ttotpdf",     "ttotpdf",      RooArgSet(RooArgList(x)), ttot)
  bkgpdf       = RooHistPdf("bkgpdf",      "bkgpdf",       RooArgSet(RooArgList(x)), bkg)
  ddbkgpdf     = RooHistPdf("ddbkgpdf",    "ddbkgpdf",     RooArgSet(RooArgList(x)), ddbkg)


  #for separate ttcc
  ##if freeTTB and not freeTTCC  : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttcclfpdf), RooArgList(fsig,fsig2,fsig3))
  if freeTTB and not freeTTCC  : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttcclfpdf), RooArgList(fsig,fsig2,fsig32con))
  elif not freeTTB and freeTTCC: model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttccpdf, ttlfpdf), RooArgList(fsig,fsig2con,fsig3con, fsigcc))
  elif freeTTB and freeTTCC    : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttccpdf, ttlfpdf), RooArgList(fsig,fsig2,fsig3, fsigcc))
  else                         : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttcclfpdf), RooArgList(fsig,fsig2con,fsig3con))
  
  model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf,ddbkgpdf),              RooArgList(knttjj,knttot,nbkg,nddbkg)) # k*bkg
  #model2 = RooAddPdf("model2", "model2",RooArgList( model, ttotpdf, bkgpdf),              RooArgList(knttjj,knttot,nbkg)) # fixing bkg
  model2.fitTo(data)
  #model2.fitTo(ttlf)
  #nll0 = model2.createNLL(data)

  result = {
      "fsig":copy.deepcopy(fsig), 
      "fsig2":copy.deepcopy(fsig2), 
      "fsig3":copy.deepcopy(fsig3), 
      "fsig32con":copy.deepcopy(fsig32con), 
      "fsig2con":copy.deepcopy(fsig2con), 
      "fsig3con":copy.deepcopy(fsig3con), 
      "fsigcc":copy.deepcopy(fsigcc), 
      "k":copy.deepcopy(k), 
      "rttbb":copy.deepcopy(rttbb), 
      "rttb":copy.deepcopy(rttb), 
      "rtt2b":copy.deepcopy(rtt2b), 
      "rttcc":copy.deepcopy(rttcc),
      #"nll":copy.deepcopy(nll0),
      #"x":copy.deepcopy(x),
      #"y":copy.deepcopy(y),
      #"model2":copy.deepcopy(model2)
  }
  #return result
  #result2=resultPrint(result, freeTTB, freeTTCC, GEN)
  result2=resultPrintNew2(result, freeTTB, freeTTCC, GEN, True)

  recoR=result2["recoR"]
  recoRerror=result2["recoRerror"]
  recoR2=result2["recoR2"]
  recoR3=result2["recoR3"]
  recoR2error=result2["recoR2error"]
  recoR3error=result2["recoR3error"]
  recoRcc=result2["recoRcc"]
  recoRccerror=result2["recoRccerror"]
  kVal=result2["kVal"]
  kValerror=result2["kValerror"]

  result2["n_ttbb"]  = copy.deepcopy(n_ttbb)
  result2["n_ttb"]   = copy.deepcopy(n_ttb)
  result2["n_tt2b"]   = copy.deepcopy(n_tt2b)
  result2["n_ttcc"]  = copy.deepcopy(n_ttcc)
  result2["n_ttlf"]  = copy.deepcopy(n_ttlf)
  result2["n_ttjj"]  = copy.deepcopy(n_ttjj)
  result2["n_ttot"]  = copy.deepcopy(n_ttot)
  result2["n_bkg"]   = copy.deepcopy(n_bkg)
  result2["n_ddbkg"] = copy.deepcopy(n_ddbkg)
  result2["n_data"]  = copy.deepcopy(n_data)
  result2["rttbb"]   = copy.deepcopy(rttbb), 
  result2["rttb"]    = copy.deepcopy(rttb), 
  result2["rttcc"]   = copy.deepcopy(rttcc),

  if onlyPrint : return recoR, recoRerror,result2

  ################
  ################
  pt = addLegendCMS()
  pt2 = addDecayMode("LL")
  pt3 = addLegend("Madgraph")
  if GEN == "POW": pt3=addLegend("Powheg")
  if GEN == "AMC": pt3=addLegend("aMC@NLO")

  ################
  lineKKK = TLine(0,0,0,0)
  lineKKK.SetLineColor(kBlue)
  lineKKK.SetLineWidth(3)
  ################
  ################
  cR10 = TCanvas("R10", "R", 1)#500, 500)
  nll = model2.createNLL(data)
  #nll = model2.createNLL(ttlf)
  #RooMinuit(nk1).migrad() 
  RFrame = fsig.frame()
  nll.plotOn(RFrame,RooFit.ShiftToZero()) 
  RFrame.SetMaximum(4.);RFrame.SetMinimum(0)
  RFrame.GetXaxis().SetTitle("Rreco as ttbb/ttjj")
  RFrame.SetTitle("")
  RFrame.Draw()
  
  line = TLine(RFrame.GetXaxis().GetXmin() ,0.5,RFrame.GetXaxis().GetXmax(),0.5)
  line.SetLineColor(kRed)
  line.Draw()
  
  lineTbb = TLine(rttbb,RFrame.GetMaximum(),rttbb,0)
  lineTbb.SetLineStyle(2)
  lineTbb.Draw()
  
  l1 = make_legend(0.49,0.76,0.93,0.88)
  l1.AddEntry(lineTbb,"prefit: R="+str(roudV(rttbb)),"l")
  l1.AddEntry(lineKKK,"fit: R="+str(roudV(recoR))+" #pm "+str(roudV(recoRerror))+"","l")
  l1.SetTextSize(0.04)
  l1.SetFillColor(0)
  l1.SetLineColor(0)
  l1.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
########################
  #cPull0 = TCanvas("CPull0", "Pull", 1)
  #hpull = RFrame.pullHist() 
  #RFramePull = xyArg.frame(Title("Pull Distribution"))
  #RFramePull.addPlotable(hpull,"P")
  #RFramePull.Draw()
  #cPull0.Print("plot/"+GEN+"_pull_test.eps")

######################## 
  if freeTTB and freeTTCC:
    cR10.Print("plots/"+GEN+"_R_freeTTBTTCC.eps")
    cR10.Print("plots/"+GEN+"_R_freeTTBTTCC.png") 
  elif freeTTB:
    cR10.Print("plots/"+GEN+"_R_freeTTB.eps")
    cR10.Print("plots/"+GEN+"_R_freeTTB.png")
  elif freeTTCC:              
    cR10.Print("plots/"+GEN+"_R_freeTTCC.eps")
    cR10.Print("plots/"+GEN+"_R_freeTTCC.png")
  else :                      
    cR10.Print("plots/"+GEN+"_R_constraintTTB.eps")
    cR10.Print("plots/"+GEN+"_R_constraintTTB.png")
  #return cR10
  
  ################
  ################
  ################
  ################
  cR00 = TCanvas("R00", "R", 1)#500, 500)
  nllK = model2.createNLL(data)
  #nllK = result["nll"]#model2.createNLL(data)
  #nll = model2.createNLL(ttlf)
  #RooMinuit(nk1).migrad() 
  RFrameK = k.frame()
  nllK.plotOn(RFrameK,RooFit.ShiftToZero()) 
  RFrameK.SetMaximum(4.);RFrameK.SetMinimum(0)
  RFrameK.GetXaxis().SetTitle("k")
  RFrameK.SetTitle("")
  #RFrameK.SetLineColor(kBlue)
  RFrameK.Draw()
  print "RFameK: "+str(type(RFrameK))
  lineK = TLine(RFrameK.GetXaxis().GetXmin() ,0.5,RFrameK.GetXaxis().GetXmax(),0.5)
  lineK.SetLineColor(kRed)
  lineK.Draw()
  
  lineTbbK = TLine(1,RFrameK.GetMaximum(),1,0)
  lineTbbK.SetLineStyle(2)
  lineTbbK.Draw()
  
  #lineTbb2 = TLine(0.0652239,RFrame.GetMaximum(),0.0652239,0)
  #lineTbb2.SetLineStyle(3)
  #lineTbb2.Draw()
  
  l1K = make_legend(0.49,0.76,0.93,0.88)
  l1K.AddEntry(lineTbbK,"prefit: k=1.0","l")
  l1K.AddEntry(lineKKK,"fit: k="+str(roudV(kVal))+" #pm "+str(roudV(kValerror))+"","l")
  l1K.SetTextSize(0.04)
  l1K.SetFillColor(0)
  l1K.SetLineColor(0)
  l1K.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB and freeTTCC:
    cR00.Print("plots/"+GEN+"_K_freeTTBTTCC.eps")
    cR00.Print("plots/"+GEN+"_K_freeTTBTTCC.png") 
  elif freeTTB:
    cR00.Print("plots/"+GEN+"_K_freeTTB.eps")
    cR00.Print("plots/"+GEN+"_K_freeTTB.png")
  elif freeTTCC:              
    cR00.Print("plots/"+GEN+"_K_freeTTCC.eps")
    cR00.Print("plots/"+GEN+"_K_freeTTCC.png")
  else :                      
    cR00.Print("plots/"+GEN+"_K_constraintTTB.eps")
    cR00.Print("plots/"+GEN+"_K_constraintTTB.png")
  
  
  ################
  ################
  ################
  ################
  cR11 = TCanvas("R11", "R", 1)# 500, 500)
  xframe = x.frame()
  data.plotOn(xframe, RooFit.DataError(RooAbsData.SumW2) ) 
  model2.paramOn(xframe, RooFit.Layout(0.65,0.9,0.9) )
  model2.plotOn(xframe)
  chi2 = xframe.chiSquare(1)
  ndof = xframe.GetNbinsX()
  print "chi2 = "+ str(chi2)
  print "ndof = "+ str(ndof)
  xframe.SetMaximum(xframe.GetMaximum()*1.5)
  xframe.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB and freeTTCC:
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTBTTCC.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTBTTCC.png") 
  elif freeTTB:
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTB.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTB.png")
  elif freeTTCC:              
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTCC.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_freeTTCC.png")
  else :                      
    cR11.Print("plots/"+GEN+"_jet3CSV_constraintTTB.eps")
    cR11.Print("plots/"+GEN+"_jet3CSV_constraintTTB.png")
  
  ################
  ################
  ################
  ################
  ################
  """
  cR12 = TCanvas("R12", "R", 1)#500, 500)
  yframe = y.frame()
  data.plotOn(yframe, RooFit.DataError(RooAbsData.SumW2) ) 
  model2.paramOn(yframe, RooFit.Layout(0.65,0.9,0.9) )
  model2.plotOn(yframe)
  chi22 = yframe.chiSquare(2)
  ndof2 = yframe.GetNbinsX()
  print "chi2 = "+ str(chi22)
  print "ndof = "+ str(ndof2)
  yframe.SetMaximum(yframe.GetMaximum()*1.5)
  yframe.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  if freeTTB and freeTTCC:
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTBTTCC.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTBTTCC.png") 
  elif freeTTB:
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTB.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTB.png")
  elif freeTTCC:
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTCC.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_freeTTCC.png")
  else :
    cR12.Print("plots/"+GEN+"_jet4CSV_constraintTTB.eps")
    cR12.Print("plots/"+GEN+"_jet4CSV_constraintTTB.png")
  """  
  ###########################
  ###########################
  ###########################
  ###########################
  ###########################
  ###########################
  cNLLContourb = TCanvas("cNLLContourb", "cNLLContourb", 1)
  if freeTTB:  
    nll22 = model2.createNLL(data)
    m=RooMinuit(nll22)
    frameNLLContour = m.contour(fsig, fsig2,1,2,3)
    #cNLLContour = TCanvas("cNLLContour", "cNLLContour", 1)
  
    frameNLLContour.GetXaxis().SetTitle("R as ttbb/ttjj")
    frameNLLContour.GetYaxis().SetTitle("R2 as ttb/ttjj")
    frameNLLContour.SetMarkerStyle(21)
    frameNLLContour.Draw()
  
    preM = TMarker(rttbb,rttb,20)
    preM.SetMarkerColor(kRed)
    preM.Draw()
    preM2 = TMarker(rttbb,rttb,20)
    preM2.SetMarkerColor(kBlack)

    
    preM23 = TMarker(0.05554,0.09849,20)
    preM23.SetMarkerColor(kBlue)
    preM23.Draw()

    pt.Draw()
    #pt2.Draw()
    pt3.Draw()
  
    l2 = make_legend(0.38,0.63,0.94,0.90)
    l2.AddEntry(preM,"prefit: R="+str(roudV(rttbb*100)/100),"p")
    l2.AddEntry(preM,"prefit: R2="+str(roudV(rttb*100)/100),"p")
    l2.AddEntry(preM23,"fit(cen.): R="+str(roudV(0.0555))+str(" #pm 0.0077") ,"p")
    l2.AddEntry(preM23,"fit(cen.): R2="+str(roudV(0.0985)),"p")
  
    l2.AddEntry(preM2,"fit: R="+str(roudV(recoR*100)/100)+" #pm "+str(roudV(recoRerror*100)/100)+"","p")
    l2.AddEntry(preM2,"fit: R2="+str(roudV(recoR2*100)/100)+" #pm "+str(roudV(recoR2error*100)/100)+"","p")
    l2.SetTextSize(0.04)
    l2.SetFillColor(0)
    l2.SetLineColor(0)
    l2.Draw()
  
    if freeTTCC:
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTBTTCC.eps")
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTBTTCC.png") 
    else :
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTB.eps")
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig2_freeTTB.png")

    nll23 = model2.createNLL(data)
    m=RooMinuit(nll23)
    frameNLLContour2 = m.contour(fsig, fsig3,1,2,3)
    #cNLLContour = TCanvas("cNLLContour", "cNLLContour", 1)
  
    frameNLLContour2.GetXaxis().SetTitle("R as ttbb/ttjj")
    frameNLLContour2.GetYaxis().SetTitle("R3 as tt2b/ttjj")
    frameNLLContour2.SetMarkerStyle(21)
    frameNLLContour2.Draw()
  
    preM21 = TMarker(rttbb,rtt2b,20)
    preM21.SetMarkerColor(kRed)
    preM21.Draw()
    preM22 = TMarker(rttbb,rtt2b,20)
    preM22.SetMarkerColor(kBlack)
  
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
  
    l21 = make_legend(0.49,0.7,0.93,0.88)
    l21.AddEntry(preM21,"prefit: R="+str(roudV(rttbb)),"p")
    l21.AddEntry(preM21,"prefit: R3="+str(roudV(rtt2b)),"p")
  
    l21.AddEntry(preM22,"fit: R="+str(roudV(recoR))+" #pm "+str(roudV(recoRerror))+"","p")
    l21.AddEntry(preM22,"fit: R3="+str(roudV(recoR3))+" #pm "+str(roudV(recoR3error))+"","p")
    l21.SetTextSize(0.04)
    l21.SetFillColor(0)
    l21.SetLineColor(0)
    l21.Draw()
  
    if freeTTCC:
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig3_freeTTBTTCC.eps")
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig3_freeTTBTTCC.png") 
    else :
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig3_freeTTB.eps")
      cNLLContourb.Print("plots/"+GEN+"_NLL_fsigVSfsig3_freeTTB.png")
  
  ###########################
  ###########################
  ###########################
  ###########################
  cNLLContourc = TCanvas("cNLLContourc", "cNLLContourc", 1)
  if freeTTCC:  
    nll22 = model2.createNLL(data)
    m=RooMinuit(nll22)
    frameNLLContour = m.contour(fsig, fsigcc,1,2,3)
    #cNLLContourc = TCanvas("cNLLContourc", "cNLLContourc", 1)
  
    frameNLLContour.GetXaxis().SetTitle("R as ttbb/ttjj")
    frameNLLContour.GetYaxis().SetTitle("R3 as ttcc/ttjj")
    frameNLLContour.SetMarkerStyle(21)
    frameNLLContour.Draw()
  
    preM = TMarker(rttbb,rttcc,20)
    preM.SetMarkerColor(kRed)
    preM.Draw()
    preM2 = TMarker(rttbb,rttcc,20)
    preM2.SetMarkerColor(kBlack)
   
  
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
  
    l2 = make_legend(0.49,0.7,0.93,0.88)
    l2.AddEntry(preM,"prefit: R="+str(roudV(rttbb)),"p")
    l2.AddEntry(preM,"prefit: Rcc="+str(roudV(rttcc)),"p")
    l2.AddEntry(preM2,"fit: R="+str(roudV(recoR))+" #pm "+str(roudV(recoRerror))+"","p")
    l2.AddEntry(preM2,"fit: Rcc="+str(roudV(recoRcc))+" #pm "+str(roudV(recoRccerror))+"","p")
    l2.SetTextSize(0.04)
    l2.SetFillColor(0)
    l2.SetLineColor(0)
    l2.Draw()
  
    if freeTTB:
      cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTBTTCC.eps")
      cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTBTTCC.png")
    else :
      cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTCC.eps")
      cNLLContourc.Print("plots/"+GEN+"_NLL_fsigVSfsigcc_freeTTCC.png")
  
  ###########################
  ###########################
  ###########################
  cN = TCanvas("cN", "cN", 1)
  #histograms[GEN+"ttcc"]["h11"].Add(histograms[GEN+"ttc"]["h11"])
  histograms[GEN+"ttbb"]["h333"].SetLineColor(kRed)
  histograms[GEN+"ttb"]["h333"].SetLineColor(kOrange)
  histograms[GEN+"tt2b"]["h333"].SetLineColor(kGreen)
  histograms[GEN+"ttcc"]["h333"].SetLineColor(kBlue)
  histograms[GEN+"ttlf"]["h333"].SetLineColor(kViolet)

  histograms[GEN+"ttbb"]["h333"].SetMarkerStyle(1)
  histograms[GEN+"ttb"]["h333"].SetMarkerStyle(1)
  histograms[GEN+"tt2b"]["h333"].SetMarkerStyle(1)
  histograms[GEN+"ttcc"]["h333"].SetMarkerStyle(1)
  histograms[GEN+"ttlf"]["h333"].SetMarkerStyle(1)
 

  normH1=histograms[GEN+"ttbb"]["h333"].DrawNormalized()
  normH1.SetMaximum(normH1.GetMaximum()*2.0)


  normH1.Draw("same")
  histograms[GEN+"ttb"]["h333"].DrawNormalized("same")
  histograms[GEN+"tt2b"]["h333"].DrawNormalized("same")
  histograms[GEN+"ttcc"]["h333"].DrawNormalized("same")
  histograms[GEN+"ttlf"]["h333"].DrawNormalized("same")
 
  normH1.Draw("sameHIST")
  histograms[GEN+"ttb"]["h333"].DrawNormalized("sameHIST")
  histograms[GEN+"tt2b"]["h333"].DrawNormalized("sameHIST")
  histograms[GEN+"ttcc"]["h333"].DrawNormalized("sameHIST")
  histograms[GEN+"ttlf"]["h333"].DrawNormalized("sameHIST")

  l21 = make_legend(0.69,0.6,0.85,0.88)
  l21.AddEntry(histograms[GEN+"ttbb"]["h333"],"ttbb","l")
  l21.AddEntry(histograms[GEN+"ttb"]["h333"],"ttb","l")
  l21.AddEntry(histograms[GEN+"tt2b"]["h333"],"tt2b","l")
  l21.AddEntry(histograms[GEN+"ttcc"]["h333"],"ttcc","l")
  l21.AddEntry(histograms[GEN+"ttlf"]["h333"],"ttlf","l")
  l21.SetTextSize(0.04)
  l21.SetFillColor(0)
  l21.SetLineColor(0)
  l21.Draw()
  
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  
  
  cN.Print("plots/"+GEN+"_Norm1.eps")
  cN.Print("plots/"+GEN+"_Norm1.png")
  ###########################
  cN2 = TCanvas("cN2", "cN2", 1)
  #histograms[GEN+"ttcc"]["h12"].Add(histograms[GEN+"ttc"]["h12"])
  histograms[GEN+"ttbb"]["h12"].SetLineColor(kRed)
  histograms[GEN+"ttb"]["h12"].SetLineColor(kOrange)
  histograms[GEN+"tt2b"]["h12"].SetLineColor(kGreen)
  histograms[GEN+"ttcc"]["h12"].SetLineColor(kBlue)
  histograms[GEN+"ttlf"]["h12"].SetLineColor(kViolet)


  normH2=histograms[GEN+"ttbb"]["h12"].DrawNormalized()
  normH2.SetMaximum(normH2.GetMaximum()*3.8)
  normH2.Draw("HIST")
  histograms[GEN+"ttb"]["h12"].DrawNormalized("sameHIST")
  histograms[GEN+"tt2b"]["h12"].DrawNormalized("sameHIST")
  histograms[GEN+"ttcc"]["h12"].DrawNormalized("sameHIST")
  histograms[GEN+"ttlf"]["h12"].DrawNormalized("sameHIST")
  l22 = make_legend(0.69,0.6,0.85,0.88)
  l22.AddEntry(histograms[GEN+"ttbb"]["h12"],"ttbb","l")
  l22.AddEntry(histograms[GEN+"ttb"]["h12"],"ttb","l")
  l22.AddEntry(histograms[GEN+"tt2b"]["h12"],"tt2b","l")
  l22.AddEntry(histograms[GEN+"ttcc"]["h12"],"ttcc","l")
  l22.AddEntry(histograms[GEN+"ttlf"]["h12"],"ttlf","l")
  l22.SetTextSize(0.04)
  l22.SetFillColor(0)
  l22.SetLineColor(0)
  l22.Draw()
  pt.Draw()
  pt2.Draw()
  pt3.Draw()
  
  
  cN2.Print("plots/"+GEN+"_Norm2.eps")
  cN2.Print("plots/"+GEN+"_Norm2.png")

 ###########################
  return cR10, cR00, cR11, cR12, cNLLContourb,cNLLContourc, cN, cN2


################
################
################
################
################
################
################
def Chi2Test1D(GEN,histograms):#data2D,mc2D):
  ttbb = histograms[GEN+"ttbb"]["h333"]
  ttb  = histograms[GEN+"ttb"]["h333"]
  tt2b  = histograms[GEN+"tt2b"]["h333"]
  ttcc = histograms[GEN+"ttcc"]["h333"]
  #ttc = histograms[GEN+"ttc"]["h333"]
  ttlf = histograms[GEN+"ttlf"]["h333"]
  ttcclf = histograms[GEN+"ttcclf"]["h333"]
  ttot = histograms[GEN+"ttot"]["h333"]
  bkg = histograms["bkg"]["h333"]
  ddbkg = histograms["ddbkg"]["h333"]
  data2D = histograms["DATA"]["h333"]

  mc2D = histograms[GEN+"ttbb"]["h333"].Clone("mc2D")
  mc2D.Reset()
  #FINAL2:newSF by fitting :{'ttbbSF':1.65202242693,'ttcclfSF':0.913516936027,'k':0.896536953009}

  ttbbSF=1.65202242693
  ttcclfSF=0.913516936027
  k=0.896536953009
  ttbb.Scale(ttbbSF*k)
  ttb.Scale(ttbbSF*k)
  tt2b.Scale(ttbbSF*k)
  ttcclf.Scale(ttcclfSF*k)
  ttot.Scale(k)
  print  "FINAL2:chi2test: ttbb: "+str(ttbb.Integral())
  print  "FINAL2:chi2test: ttb: "+str(ttb.Integral())
  print  "FINAL2:chi2test: tt2b: "+str(tt2b.Integral())
  print  "FINAL2:chi2test: ttcc: "+str(ttcc.Integral())
  print  "FINAL2:chi2test: ttlf: "+str(ttlf.Integral())
  print  "FINAL2:chi2test: ttot: "+str(ttot.Integral())

  print  "FINAL2:chi2test: bkg: "+str(bkg.Integral())
  print  "FINAL2:chi2test: ddbkg: "+str(ddbkg.Integral())
  print  "FINAL2:chi2test: data2D: "+str(data2D.Integral())

  mc2D.Add(ttbb), mc2D.Add(ttb),mc2D.Add(tt2b)
  #mc2D.Add(ttcc)
  mc2D.Add(ttcclf),  mc2D.Add(ttot),  mc2D.Add(bkg),  mc2D.Add(ddbkg)

    ##https://root.cern.ch/doc/master/classTH1.html#a11153bd9c45ceac48bbfac56cb62ea74
  # options
  chi2nof_1d =  data2D.Chi2Test(mc2D,"UW P CHI2/NDF")
  chi2_1d = data2D.Chi2Test(mc2D,"UW P CHI2")

  print "FINAL: chi/ndof = "+str(chi2nof_1d)
  print "FINAL: chi      = "+str(chi2_1d)

################
################
#
################
def Chi2Test2D(GEN,histograms):#data2D,mc2D):
  ttbb = histograms[GEN+"ttbb"]["h1"]
  ttb  = histograms[GEN+"ttb"]["h1"]
  tt2b  = histograms[GEN+"tt2b"]["h1"]
  ttcc = histograms[GEN+"ttcc"]["h1"]
  #ttc = histograms[GEN+"ttc"]["h1"]
  ttlf = histograms[GEN+"ttlf"]["h1"]
  ttcclf = histograms[GEN+"ttcclf"]["h1"]
  ttot = histograms[GEN+"ttot"]["h1"]
  bkg = histograms["bkg"]["h1"]
  ddbkg = histograms["ddbkg"]["h1"]
  data2D = histograms["DATA"]["h1"]

  mc2D = histograms[GEN+"ttbb"]["h1"].Clone("mc2D")
  mc2D.Reset()
  mc2D.Add(ttbb), mc2D.Add(ttb),mc2D.Add(tt2b)
  #mc2D.Add(ttcc)
  mc2D.Add(ttcclf),  mc2D.Add(ttot),  mc2D.Add(bkg),  mc2D.Add(ddbkg)

  binN    = mc2D.GetNbinsX()*mc2D.GetNbinsY()
  mc_1d   =  TH1D("mc_1d","",binN,0.,10.)
  data_1d = TH1D("data_1d","",binN,0.,10.)
  for i in range(1,mc2D.GetNbinsX()+1):
    for j in range(1,mc2D.GetNbinsY()+1):
       ij = i*(mc2D.GetNbinsX()-1)+j
       mc_1d.SetBinContent  (ij,mc2D.GetBinContent  (i,j) )
       mc_1d.SetBinError    (ij,mc2D.GetBinError    (i,j) )
       data_1d.SetBinContent(ij,data2D.GetBinContent(i,j) )
       data_1d.SetBinError  (ij,data2D.GetBinError  (i,j) )
  ##https://root.cern.ch/doc/master/classTH1.html#a11153bd9c45ceac48bbfac56cb62ea74
  # options
  chi2nof_1d =  data_1d.Chi2Test(mc_1d,"UW P CHI2/NDF")
  chi2_1d = data_1d.Chi2Test(mc_1d,"UW P CHI2")

  print "FINAL: chi/ndof = "+str(chi2nof_1d)
  print "FINAL: chi      = "+str(chi2_1d)

################
################
################
################
################
################
################
################
def resultPrint3(result, genInfo):

  #eR = genInfo["eR"]
  #acP = genInfo["acP"]
  #dilepBr = 0.10705984
  dilepBr = 0.1049580955
  ttbarCX = 831.76 
  #ttjjAcp = genInfo["Acc"]["ttjj"]*dilepBr
  #ttbbAcp = genInfo["Acc"]["ttbb"]*dilepBr

  #Acc :  ttbbVPS_DiLeptonic / ttbbFPS_Alldecay , 2016. June 13
  #POW & 0.0160401846363 & 0.0176910436472
  #$MG5 & 0.0168631361516 & 0.0192072020681
  #AMC & 0.0160596740749 & 0.0177292239969
  #ttjjAcp = 0.0176910436472
  #ttbbAcp = 0.0160401846363
  #ttbbAcp=0.021
  ttbbAcp=0.022
  ttjjAcp=0.020

  ttjjEff = genInfo["Eff"]["ttjj"]
  ttbbEff = genInfo["Eff"]["ttbb"]

  rttbb= result["rttbb"][0]

  n_ttjj = result["n_ttbb"] + result["n_ttb"] + result["n_tt2b"] + result["n_ttcc"] + result["n_ttlf"]
  print "FINAL2: n_ttbb: "+str(roudV(result["n_ttbb"])) +", ttb:"+ str(roudV(result["n_ttb"]))+", tt2b:"+str(roudV(result["n_tt2b"]))
  print "FINAL2: n_ttcc: "+str(roudV(result["n_ttcc"])) +", ttlf: "+ str(roudV(result["n_ttlf"]))
  print "FINAL2: n_ttjj: "+str(roudV(n_ttjj))

  #eR=ttjjEff/ttbbEff
  recoR = result["recoR"] 
  recoRerror = result["recoRerror"] 
  genR = result["recoR"] * (ttjjEff/ttbbEff)
  genRerror = recoR*(ttjjEff/ttbbEff)*recoRerror/recoR

  #print "FINAL2: n_ttjj:"+str(type(n_ttjj))+", rttbb:"+str(rttbb)+", "+str(type(rttbb))

  NewNttbb = n_ttjj * result["kVal"]*result["recoR"]  #(result["n_ttbb"] * result["recoR"] * result["kVal"]) / rttbb
  NewNttjj = n_ttjj * result["kVal"]

  NewCXttbbvis = NewNttbb/(lumi * ttbbEff )
  NewCXttjjvis = NewNttjj/(lumi * ttjjEff )
  NewCXttbbfull = NewNttbb/(lumi * ttbbEff * ttbbAcp )
  NewCXttjjfull = NewNttjj/(lumi * ttjjEff * ttjjAcp )

  print "FINAL2: ---genInfo---------------------------------"

  ttbbScaleSysVS=0.1295530779
  ttjjScaleSysVS=0.101
  rScaleSysVS=0.1024890238

  #ttbbScaleSysFS = 0.1333604139
  #ttjjScaleSysFS = 0.1101635148
  #rScaleSysFS = 0.114629839
  ttbbScaleSysFS =  ttbbScaleSysVS
  ttjjScaleSysFS =  ttjjScaleSysVS
  rScaleSysFS =     rScaleSysVS

  NttbbVS = genInfo["ttbbVS"]/genInfo["total"]*ttbarCX
  NttjjVS = genInfo["ttjjVS"]/genInfo["total"]*ttbarCX
  NttbbFS = genInfo["ttbbFS"]/genInfo["total"]/dilepBr*ttbarCX
  NttjjFS = genInfo["ttjjFS"]/genInfo["total"]/dilepBr*ttbarCX

  rFS = genInfo["rFS"]
  rVS = genInfo["rVS"]

  print "FINAL2: R full : "+str(roudV(rFS))+" $\pm$  "+str(roudV(rFS*rScaleSysFS))
  print "FINAL2: R_vis : " +str(roudV(rVS))+" $\pm$  "+str(roudV(rVS*rScaleSysVS))

  print "FINAL2: ttbb vis : "+str(roudV(NttbbVS))+" $\pm$ "+str(roudV(NttbbVS*ttbbScaleSysVS ))
  print "FINAL2: ttjj vis : "+str(roudV(NttjjVS))+" $\pm$ "+str(roudV(NttjjVS*ttjjScaleSysVS ))

  print "FINAL2: ttbb full : "+str(roudV(NttbbFS))+" $\pm$ "+str(roudV(NttbbFS*ttbbScaleSysFS )) 
  print "FINAL2: ttjj full : "+str(roudV(NttjjFS))+" $\pm$ "+str(roudV(NttjjFS*ttjjScaleSysFS ))

  print "FINAL2: Acceptance ttjj : "+str(roudV(ttjjAcp*100))+" % "
  print "FINAL2: Acceptance ttbb : "+str(roudV(ttbbAcp*100))+" % "

  print "FINAL2: efficiency ttjj : "+str(roudV(ttjjEff*100))+" % "
  print "FINAL2: efficiency ttbb : "+str(roudV(ttbbEff*100))+" % "


  print "FINAL2: #ttjj prefit = "+str(roudV(n_ttjj))+"  "
  print "FINAL2: -----Measure----------------"
  print "FINAL2: #ttjj fitting = "+str(roudV(NewNttjj))+"  "
  print "FINAL2: #ttbb fitting = "+str(roudV(NewNttbb))+"  "

  #b=1-ttbAll(r-1)/ttlf
  n_ttbAll = result["n_ttbb"] + result["n_ttb"] + result["n_tt2b"]
  n_ttcclf = result["n_ttcc"] + result["n_ttlf"]
  ttbbSF = recoR/rttbb
  ttcclfSF = 1.0-n_ttbAll*(recoR/rttbb -1.0)/n_ttcclf

  ##################### 2016.06.04 v765
  #RSysVS=0.293901088804
  #ttjjSysVS=0.184561371906
  #ttbbSysVS=0.348243937492
  #RSysFS=0.299949829138
  #ttjjSysFS=0.210478597487
  #ttbbSysFS=0.366785114202

  ##################### 2016.06.07 v765
  #RSysVS=0.295461621873
  #ttjjSysVS=0.186268864816
  #ttbbSysVS=0.348729522696
  #RSysFS=0.299769728292
  #ttjjSysFS=0.212804793179
  #ttbbSysFS=0.367060703427
  ####################### 2016. 06.11 v765
  RSysVS=0.281609658925
  ttjjSysVS=0.186850207385
  #ttbbSysVS=0.337921588538
  ttbbSysVS=0.318233368547

  RSysFS=0.285952793307
  ttjjSysFS=0.210059515376
  #ttbbSysFS=0.35324354205
  ttbbSysFS=0.329605031601
  ######## FPS all decays 2016. 06. 13. v765
  #RSysFS=0.291293666255
  #ttjjSysFS=0.202281981402
  #ttbbSysFS=0.348651688652

  print "FINAL2:prefit Reco R = "+str(roudV(rttbb))
  print "FINAL2:newSF by fitting :"+"{'ttbbSF':"+str(ttbbSF)+",'ttcclfSF':"+str(ttcclfSF)+",'k':"+str(result['kVal'])+"}"
  print "FINAL2:Reco  R = "+ str(roudV(recoR))+" $\pm$ "+str(roudV(recoRerror))+" "
  print "FINAL2:vis   R = "+ str(roudV(genR))+" $\pm$ "+str(roudV(genRerror))+"(stat.) $\pm$ "+str(roudV(genR*RSysVS))+"(syst.) "
  fullR    = (genR*ttjjAcp/ttbbAcp)
  fullRerr = (genR*ttjjAcp/ttbbAcp)*(genRerror/genR)
  print "FINAL2:full  R = "+ str(roudV(fullR))+" $\pm$ "+str(roudV(fullRerr))+"(stat.) $\pm$ "+str(roudV(fullR*RSysFS))+"(syst.)"

  print "FINAL2:vis   ttbb :"+str(roudV(NewCXttbbvis))+" $\pm$ "+str(roudV(NewCXttbbvis*(sqrt((result["kValerror"]/result["kVal"])*(result["kValerror"]/result["kVal"])+(genRerror/genR)*(genRerror/genR)))))+"(stat.) $\pm$ "+str(roudV(NewCXttbbvis*ttbbSysVS))+"(syst.) pb"
  print "FINAL2:vis   ttjj :"+str(roudV(NewCXttjjvis))+" $\pm$ "+str(roudV(NewCXttjjvis*(result["kValerror"]/result["kVal"])))+"(syst.) $\pm$ "+str(roudV(NewCXttjjvis*ttjjSysVS))+"(syst.) pb"

  print "FINAL2:full ll   ttbb :"+str(roudV(NewCXttbbfull))+" $\pm$ "+str(roudV(NewCXttbbfull*(sqrt((result["kValerror"]/result["kVal"])*(result["kValerror"]/result["kVal"])+(genRerror/genR)*(genRerror/genR)))))+"(syst.) $\pm$ "+str(roudV(NewCXttbbfull*ttbbSysFS))+"(syst.) pb"
  print "FINAL2:full ll  ttjj :"+str(roudV(NewCXttjjfull))+" $\pm$ "+str(roudV(NewCXttjjfull*(result["kValerror"]/result["kVal"])))+"(stat.) $\pm$ "+str(roudV(NewCXttjjfull*ttjjSysFS))+"(syst.) pb"
  RdilepPOW=dilepBr #genInfo["data"]['dileptonic']/genInfo["total"]
  print "FINAL2: ----------------------------------------------"
 


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

def printV(data,isPrint):
  total = sumV(data,"",['dileptonic','semileptonic','hadroic'])
  if isPrint : print "total : "+str(total)
  if isPrint : print "dileptonic : "+str(data['dileptonic'])+", semileptonic : "+str(data['semileptonic'])+", hadroic : "+str(data['hadroic'])
  VS = ["ttbb","tt2b","ttb","ttcc","ttlf"]# "ttot"
  FS = ["ttbbF","tt2bF","ttbF","ttccF","ttlfF"]
  ttbb = data['S0']['ttbb']
  ttbbF = data['S0']['ttbbF']
  ttjj = sumV(data,'S0',VS)
  ttjjF = sumV(data,'S0',FS)
  ttbbAcc=ttbb/ttbbF
  ttjjAcc=ttjj/ttjjF
  rFS = ttbbF/ttjjF
  rVS = ttbb/ttjj
  rTtjjTotalFS=ttjjF/total
  rTtjjTotalVS=ttjj/total

  if isPrint : print "ratio ttjj/total FS: "+str(roudV(rTtjjTotalFS*100))+" %"
  if isPrint : print "ratio ttjj/total VS: "+str(roudV(rTtjjTotalVS*100))+" %"
  if isPrint : print "Acceptance(VS/FS) ttbb : "+str(roudV(ttbbAcc))+", ttjj : "+str(roudV(ttjjAcc))
  if isPrint : print "FS R(ttbb/ttjj) : "+str(roudV(rFS)*100)+" %"
  if isPrint : print "VS R(ttbb/ttjj) : "+str(roudV(rVS)*100)+" %"
  ttbbS6 = data['S6']['ttbb']
  ttjjS6 = sumV(data,"S6",["ttbb","tt2b","ttb","ttcc","ttlf"])
  ttbbEff= ttbbS6/ttbb
  ttjjEff= ttjjS6/ttjj
  rTtjjTotalS6=ttjjS6/total
  if isPrint : print "ratio ttjj/total S6: "+str(roudV(rTtjjTotalS6))+" %"
  if isPrint : print "efficiency S6/S0 in VS"
  if isPrint : print "ttbb : "+str(roudV(ttbbEff)*100)+" %"
  if isPrint : print "ttjj : "+str(roudV(ttjjEff)*100)+" %"

  if isPrint : print data["name"]+" & "+str(roudV(rFS)*100)+" \% & "+str(roudV(rVS)*100)+" \% & "+str(roudV(ttjjAcc)*100)+" \% & "+str(roudV(ttbbAcc)*100)+" \% & "+str(roudV(ttjjEff)*100)+" \% & "+str(roudV(ttbbEff)*100)+" \% \\"

  return {"name":data["name"],"rFS":rFS,"rVS":rVS,"Acc":{"ttbb":ttbbAcc,"ttjj":ttjjAcc},"Eff":{"ttbb":ttbbEff,"ttjj":ttjjEff},"rTtjjTotal":{"FS":rTtjjTotalFS,"VS":rTtjjTotalVS,"S6":rTtjjTotalS6},"data":data,"total":total,"ttjjVS":ttjj,"ttjjFS":ttjjF,"ttjjS6":ttjjS6,"ttbbVS":ttbb, "ttbbFS":ttbbF, "ttbbS6":ttbbS6}

def printV2(data,data2):
  name = data2["name"]
  rFS=data2["rFS"]
  rVS=data2["rVS"]
  ttbbAcc=data2["Acc"]["ttbb"]
  ttjjAcc=data2["Acc"]["ttjj"]
  ttbbEff=data2["Eff"]["ttbb"]
  ttjjEff=data2["Eff"]["ttjj"]

  rFSsys=getSys(data["rFS"],rFS)
  rVSsys=getSys(data["rVS"],rVS)
  ttbbAccsys=getSys(data["Acc"]["ttbb"],ttbbAcc)
  ttjjAccsys=getSys(data["Acc"]["ttjj"],ttjjAcc)
  ttbbEffsys=getSys(data["Eff"]["ttbb"],ttbbEff)
  ttjjEffsys=getSys(data["Eff"]["ttjj"],ttjjEff)

  aa= data2["name"]+" & "
  bb= str(roudV(rFS)*100)+" ("+str(roudV(rFSsys)*100)+") & "
  cc= str(roudV(rVS)*100)+" ("+str(roudV(rVSsys)*100)+") & "
  dd= str(roudV(ttjjAcc)*100)+" ("+str(roudV(ttjjAccsys)*100)+") & "
  ee= str(roudV(ttbbAcc)*100)+" ("+str(roudV(ttbbAccsys)*100)+") & "
  ff= str(roudV(ttjjEff)*100)+" ("+str(roudV(ttjjEffsys)*100)+") & "
  gg= str(roudV(ttbbEff)*100)+" ("+str(roudV(ttbbEffsys)*100)+") \\\\"
  print aa+bb+cc+dd+ee+ff+gg

def getSys(a,b):
  return (a-b)/a

################
################
################
################
################
################
##origin : genstudy/Q2scale.py 
POW={"name":"powheg-pythia8",'semileptonic': 42929174.0, 'dileptonic': 10285310.0, 'S0': {'ttbbF': 43175.0, 'ttbF': 124142.0, 'ttlfF': 3637657.0, 'ttotF': 94065561.0, 'ttccF': 87638.0, 'ttb': 24712.0, 'ttlf': 546363.0, 'ttbb': 8194.0, 'ttot': 97393418.0, 'ttcc': 15362.0, 'tt2bF': 36269.0, 'tt2b': 6393.0}, 'S7': {'ttbbF': 1940.0, 'ttbF': 2537.0, 'ttlfF': 29941.0, 'ttotF': 915.0, 'ttccF': 1303.0, 'ttb': 2527.0, 'ttlf': 29159.0, 'ttbb': 1532.0, 'ttot': 2428.0, 'ttcc': 1209.0, 'tt2bF': 1207.0, 'tt2b': 988.0}, 'S6': {'ttbbF': 2838.0, 'ttbF': 4276.0, 'ttlfF': 62138.0, 'ttotF': 1874.0, 'ttccF': 3056.0, 'ttb': 4127.0, 'ttlf': 59498.0, 'ttbb': 2206.0, 'ttot': 6077.0, 'ttcc': 2659.0, 'tt2bF': 1905.0, 'tt2b': 1520.0}, 'etc': 0.0, 'hadroic': 44779958.0}
MG5={"name":"madgraph-pythia8",'semileptonic': 4538129.0, 'etc': 0.0, 'S0': {'ttbbF': 4909.0, 'ttbb': 947.0, 'ttbF': 14552.0, 'ttlfF': 428550.0, 'ttotF': 9752453.0, 'ttccF': 10408.0, 'ttcc': 1881.0, 'tt2bF': 4259.0, 'tt2b': 787.0, 'ttb': 2969.0, 'ttlf': 66280.0, 'ttot': 10142267.0}, 'S7': {'ttbbF': 214.0, 'ttbb': 166.0, 'ttbF': 307.0, 'ttlfF': 3767.0, 'ttotF': 117.0, 'ttccF': 169.0, 'ttcc': 159.0, 'tt2bF': 161.0, 'tt2b': 132.0, 'ttb': 305.0, 'ttlf': 3669.0, 'ttot': 304.0}, 'S6': {'ttbbF': 333.0, 'ttbb': 198.0, 'ttbF': 520.0, 'ttlfF': 7859.0, 'ttotF': 233.0, 'ttccF': 303.0, 'ttcc': 264.0, 'tt2bF': 172.0, 'tt2b': 141.0, 'ttb': 407.0, 'ttlf': 5816.0, 'ttot': 570.0}, 'dileptonic': 1134687.0, 'hadroic': 4542315.0}
AMC={"name":"aMCatNLO-pythia8",'semileptonic': 5638266.0, 'etc': 0.0, 'S0': {'ttbbF': 6284.0, 'ttbb': 1150.0, 'ttbF': 17267.0, 'ttlfF': 556938.0, 'ttotF': 12100541.0, 'ttccF': 13274.0, 'ttcc': 2140.0, 'tt2bF': 4222.0, 'tt2b': 735.0, 'ttb': 3307.0, 'ttlf': 80763.0, 'ttot': 12610431.0}, 'S7': {'ttbbF': 257.0, 'ttbb': 177.0, 'ttbF': 275.0, 'ttlfF': 4158.0, 'ttotF': 125.0, 'ttccF': 173.0, 'ttcc': 157.0, 'tt2bF': 131.0, 'tt2b': 125.0, 'ttb': 298.0, 'ttlf': 4062.0, 'ttot': 300.0}, 'S6': {'ttbbF': 397.0, 'ttbb': 283.0, 'ttbF': 543.0, 'ttlfF': 8713.0, 'ttotF': 243.0, 'ttccF': 348.0, 'ttcc': 307.0, 'tt2bF': 220.0, 'tt2b': 186.0, 'ttb': 559.0, 'ttlf': 8328.0, 'ttot': 801.0}, 'dileptonic': 1409642.0, 'hadroic': 5650618.0}
POHP={"name":"powheg-herwig++",'semileptonic': 8489765.0, 'dileptonic': 2035532.0, 'S0': {'ttbbF': 6839.0, 'ttbF': 22130.0, 'ttlfF': 850216.0, 'ttotF': 18481078.0, 'ttccF': 14347.0, 'ttb': 3330.0, 'ttlf': 100634.0, 'ttbb': 982.0, 'ttot': 19275308.0, 'ttcc': 2027.0, 'tt2bF': 8853.0, 'tt2b': 1182.0}, 'S7': {'ttbbF': 272.0, 'ttbF': 336.0, 'ttlfF': 5526.0, 'ttotF': 166.0, 'ttccF': 145.0, 'ttb': 298.0, 'ttlf': 4420.0, 'ttbb': 159.0, 'ttot': 1534.0, 'ttcc': 113.0, 'tt2bF': 224.0, 'tt2b': 145.0}, 'S6': {'ttbbF': 398.0, 'ttbF': 587.0, 'ttlfF': 11883.0, 'ttotF': 346.0, 'ttccF': 421.0, 'ttb': 489.0, 'ttlf': 9379.0, 'ttbb': 227.0, 'ttot': 3386.0, 'ttcc': 286.0, 'tt2bF': 363.0, 'tt2b': 231.0}, 'etc': 0.0, 'hadroic': 8858166.0}

dwPOW={"name":"powheg-pythia8\_dw",'semileptonic': 4349284.0, 'dileptonic': 1042439.0, 'S0': {'ttbbF': 5347.0, 'ttbF': 15480.0, 'ttlfF': 369623.0, 'ttotF': 9525267.0, 'ttccF': 12558.0, 'ttb': 3092.0, 'ttlf': 54732.0, 'ttbb': 985.0, 'ttot': 9871017.0, 'ttcc': 2225.0, 'tt2bF': 4601.0, 'tt2b': 825.0}, 'S7': {'ttbbF': 204.0, 'ttbF': 279.0, 'ttlfF': 2518.0, 'ttotF': 61.0, 'ttccF': 147.0, 'ttb': 279.0, 'ttlf': 2472.0, 'ttbb': 157.0, 'ttot': 181.0, 'ttcc': 145.0, 'tt2bF': 137.0, 'tt2b': 112.0}, 'S6': {'ttbbF': 328.0, 'ttbF': 489.0, 'ttlfF': 5512.0, 'ttotF': 149.0, 'ttccF': 335.0, 'ttb': 491.0, 'ttlf': 5320.0, 'ttbb': 243.0, 'ttot': 499.0, 'ttcc': 308.0, 'tt2bF': 242.0, 'tt2b': 194.0}, 'etc': 0.0, 'hadroic': 4541153.0}

upPOW={"name":"powheg-pythia8\_up",'semileptonic': 4343618.0, 'dileptonic': 1040881.0, 'S0': {'ttbbF': 3719.0, 'ttbF': 10824.0, 'ttlfF': 360691.0, 'ttotF': 9534748.0, 'ttccF': 6762.0, 'ttb': 2136.0, 'ttlf': 53991.0, 'ttbb': 709.0, 'ttot': 9861177.0, 'ttcc': 1199.0, 'tt2bF': 3032.0, 'tt2b': 564.0}, 'S7': {'ttbbF': 200.0, 'ttbF': 215.0, 'ttlfF': 3206.0, 'ttotF': 114.0, 'ttccF': 112.0, 'ttb': 219.0, 'ttlf': 3103.0, 'ttbb': 159.0, 'ttot': 277.0, 'ttcc': 104.0, 'tt2bF': 102.0, 'tt2b': 87.0}, 'S6': {'ttbbF': 278.0, 'ttbF': 370.0, 'ttlfF': 6504.0, 'ttotF': 240.0, 'ttccF': 245.0, 'ttb': 349.0, 'ttlf': 6198.0, 'ttbb': 219.0, 'ttot': 697.0, 'ttcc': 208.0, 'tt2bF': 170.0, 'tt2b': 136.0}, 'etc': 0.0, 'hadroic': 4535277.0}

ttbarMCsamples = {  "MG5":"TTJets_MG5",         "AMC":"TTJets_aMC",            "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp"
                    ,"upPOW":"TT_powheg_scaleup", "dwPOW":"TT_powheg_scaledown"
                  }

#from .genstudy.pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
POW2=printV(POW,True)
MG52=printV(MG5,True)
POHP2=printV(POHP,True)
AMC2=printV(AMC,True)
dwPOW2=printV(dwPOW,True)
upPOW2=printV(upPOW,True)

printV2(POW2,MG52)
printV2(POW2,POHP2)
printV2(POW2,AMC2)
printV2(POW2,dwPOW2)
printV2(POW2,upPOW2)

##############################################################################
##############################################################################
##############################################################################
##############################################################################
def makeUpDown(sys,sysa):
  return {sys+"Up":{"Up":sysa,"Down":[]}, sys+"Down":{"Up":[],"Down":sysa}}

#######
import sys
if len(sys.argv) < 3:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)
arg2 = sys.argv[2] # MG5, POW

arg3="0"
if len(sys.argv) > 3:
  arg3 = sys.argv[3]


#StepSys = ["JES_Up","JES_Down","JER_NOM","JER_Up","JER_Down","LF_Up", "LF_Down", "HF_Up", "HF_Down", "HF_Stats1_Up","HF_Stats1_Down","HF_Stats2_Up","HF_Stats2_Down","LF_Stats1_Up","LF_Stats1_Down","LF_Stats2_Up","LF_Stats2_Down","CQ_Err1_Up", "CQ_Err1_Down", "CQ_Err2_Up", "CQ_Err2_Down","PW_Up","PW_Down"]
StepSys2 = {"JES":["JES","JER"],"LF":["LF","HF_Stats1","HF_Stats2"],"HF":["HF","LF_Stats1","LF_Stats2"],"CQ":["CQ_Err1","CQ_Err2"],"pileup":["PW"],"lepton":["Mu","El"],"Trigger":["Trig"]}

from sysWeight_cfi import mceventweight
sysWeights =  [i["name"] for i in mceventweight]
#sysWeights.append("Scale_Up")
#sysWeights.append("Scale_Down")
Step="S6"

from sysWeightQ2_cfi import scaleweight
sysWeightsQ2 =  [i["name"] for i in scaleweight if i["name"].find("Q2")>-1 ]
print "FINAL2: "+str(sysWeightsQ2)

histograms,freeTTB,freeTTCC,GEN=loadHistogram(arg1, arg2,Step,"csvweight")
orig_r,orig_err = 0.,0. 
Chi2Test1D(GEN,histograms)
#SystematicUnck={}
#StepSys2 = ["JES","LF","HF","HF_Stats1","HF_Stats2","LF_Stats1","LF_Stats1","Charm_Err1","Charm_Err2"]

from math import *
if int(arg3)==0:
  cR10, cR00, cR11, cR12, cNLLContourb,cNLLContourc, cN, cN2=fitting(histograms, freeTTB, freeTTCC, GEN,False,False)
###################
elif int(arg3)==4:
  sumweightQ2={'dwPOW_csvweight': 9932876.0, 'POW_csvweight': 97994442.0, 'upPOW_Q2_N1': 9721877.978248205, 'upPOW_Q2_N3': 8656597.607850373, 'dwPOW_Q2_N6': 11328951.66248878, 'dwPOW_Q2_N5': 11099336.392136984, 'dwPOW_Q2_N4': 10193564.465720307, 'upPOW_csvweight': 9919776.0, 'upPOW_Q2_N2': 8878141.199428499, 'POW_Q2_N4': 100562130.05494703, 'POW_Q2_N5': 109501436.23855484, 'POW_Q2_N6': 111759839.10910639, 'POW_Q2_N1': 96043292.78107499, 'POW_Q2_N2': 87702904.5710082, 'POW_Q2_N3': 85517519.10829923}
  SystematicUnc,SystematicUnck ={},{}
  histogramSys = {}
  histogramSysGEN = {}
  Q2sample = ["1","4","5"]
  for Q2s in Q2sample:
    histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram2(arg1, Q2s,Step,0,"csvweight",{"Up":[],"Down":[]})
    histogramSys[GEN2+"_csvweight"] = copy.deepcopy(histograms2)
    histogramSysGEN[GEN2+"_csvweight"] = copy.deepcopy(GEN2)
    for i,sys in enumerate(sysWeightsQ2):
      if i<3 and Q2s == "5": continue
      if i>2 and Q2s == "4": continue
      histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram2(arg1, Q2s,Step,i+1,sys,{"Up":[],"Down":[]})
      #histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram(arg1,Q2s,Step,sys)
      histogramSys[GEN2+"_"+sys] = copy.deepcopy(histograms2)
      histogramSysGEN[GEN2+"_"+sys] = copy.deepcopy(GEN2)

  orig_r,orig_err,result=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)

  eRPOW=POW2["Eff"]['ttjj']/POW2["Eff"]['ttbb']
  acPPOW=POW2["Acc"]['ttjj']/POW2["Acc"]['ttbb']
  genR      = orig_r*eRPOW*acPPOW
 
  eRupPOW=upPOW2["Eff"]['ttjj']/upPOW2["Eff"]['ttbb']
  acPupPOW=upPOW2["Acc"]['ttjj']/upPOW2["Acc"]['ttbb']
  eRdwPOW=dwPOW2["Eff"]['ttjj']/dwPOW2["Eff"]['ttbb']
  acPdwPOW=dwPOW2["Acc"]['ttjj']/dwPOW2["Acc"]['ttbb']
 
  kVal = result["kVal"]
  maxRsys=0.
  maxKsys=0.
  for sys in histogramSys.keys():
    orig_r2,orig_err2,result2=fitting(histogramSys[sys], freeTTB, freeTTCC, histogramSysGEN[sys],True,False)
    SFsys = eRPOW*acPPOW
    if sys.find("up")>-1: SFsys=eRupPOW*acPupPOW
    if sys.find("dw")>-1: SFsys=eRdwPOW*acPdwPOW

    sysUnc = getSys(genR,orig_r2*SFsys)
    sysUnck = getSys(kVal,result2["kVal"])
    print "FINAL2: "+(sys.rjust(30))+": R "+ str(roudV(sysUnc*100))+" %     ,     R = "+ str(roudV(orig_r2*SFsys))+" "
    print "FINAL2: "+(sys.rjust(30))+": k "+str(roudV(sysUnck*100))+" %     ,     k = "+ str(roudV(result2["kVal"]))+" "
    print "FINAL2: "+(sys.rjust(30))+": ttbb: "+str(roudV(quardsum([sysUnc,sysUnck])))+" %"
    SystematicUnc[sys]=copy.deepcopy(sysUnc)
    SystematicUnck[sys]=copy.deepcopy(sysUnck)
    maxRsys= max(maxRsys,abs(sysUnc))
    maxKsys= max(maxKsys,abs(sysUnck))

  print ""
  print "FINAL2: Q2scale : r: "+str(roudV(maxRsys*100))+" %, k:"+str(roudV(maxKsys*100))+" %"

elif int(arg3)==5:
  SystematicUnc,SystematicUnck ={},{}
  histogramSys = {}
  histogramSysGEN = {}
  for i in range(0,102):
    histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram2(arg1, "1",Step,0,"pdf_N"+str(i),{"Up":[],"Down":[]})
    histogramSys[GEN2+"_pdf"+str(i)] = copy.deepcopy(histograms2)
    histogramSysGEN[GEN2+"_pdf"+str(i)] = copy.deepcopy(GEN2)

  orig_r,orig_err,result=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)

  kVal = result["kVal"]
  maxRsys=0.
  maxKsys=0.
  for sys in histogramSys.keys():
    orig_r2,orig_err2,result2=fitting(histogramSys[sys], freeTTB, freeTTCC, histogramSysGEN[sys],True,False)
    sysUnc = getSys(orig_r,orig_r2)
    sysUnck = getSys(kVal,result2["kVal"])
    print "FINAL2: "+(sys.rjust(30))+": R "+ str(roudV(sysUnc*100))+" %     ,     R = "+ str(roudV(orig_r2))+" "
    print "FINAL2: "+(sys.rjust(30))+": k "+str(roudV(sysUnck*100))+" %     ,     k = "+ str(roudV(result2["kVal"]))+" "
    print "FINAL2: "+(sys.rjust(30))+": ttbb: "+str(roudV(quardsum([sysUnc,sysUnck])))+" %"
    SystematicUnc[sys]=copy.deepcopy(sysUnc)
    SystematicUnck[sys]=copy.deepcopy(sysUnck)
    maxRsys= max(maxRsys,abs(sysUnc))
    maxKsys= max(maxKsys,abs(sysUnck))

  print ""
  print "FINAL2: pdf : r: "+str(roudV(maxRsys*100))+" %, k:"+str(roudV(maxKsys*100))+" %"




#################
elif int(arg3)==3:
  SystematicUnc,SystematicUnck,SystematicUncTTBB ={},{},{}
  histogramSys = {}
  histogramSysGEN = {}
  #ttccUp={"Up":[GEN+'ttcc'],"Down":[]}
  #ttccDown={"Up":[],"Down":[GEN+'ttcc']}
  #sysSets = {"ttccUp":ttccUp,"ttccDown":ttccDown}
  sysSets=        makeUpDown("ttcc",[GEN+'ttcc'])
  #print "FINAL2: "+str(makeUpDown("SingleTop",['STbt', 'STt', 'STbtW', 'STtW'] ) )
  sysSets.update( makeUpDown("SingleTop",['STbt', 'STt', 'STbtW', 'STtW'])  )
  sysSets.update( makeUpDown("VV",['WW', 'WZ', 'ZZ'])  )
  sysSets.update( makeUpDown("DYJets",['DYJets','DYJets10'])  )
  sysSets.update( makeUpDown("TTV",[ 'TTWqq','TTWlNu', 'TTZqq','TTZll'])  )
  sysSets.update( makeUpDown("ttot",[GEN+"ttot"])  )
  for sys in sysSets.keys():
    histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram2(arg1, arg2,Step,0,"csvweight",sysSets[sys])
    histogramSys[sys] = copy.deepcopy(histograms2)
    histogramSysGEN[sys] = copy.deepcopy(GEN2)

  orig_r,orig_err,result=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)
  kVal = result["kVal"] 
  ttbbCenter = result["n_ttjj"]*kVal*orig_r
  for sys in sysSets.keys():
    orig_r2,orig_err2,result2=fitting(histogramSys[sys], freeTTB, freeTTCC, histogramSysGEN[sys],True,False)
    sysUnc = getSys(orig_r,orig_r2)
    sysUnck = getSys(kVal,result2["kVal"])
    ttbbNew2 = result2["n_ttjj"]*result2["kVal"]*orig_r2
    sysUncTTBB = getSys(ttbbCenter, ttbbNew2)


    print "FINAL2: "+(sys.rjust(30))+": R "+ str(roudV(sysUnc*100))+" %     ,     R = "+ str(roudV(orig_r2))+" "
    print "FINAL2: "+(sys.rjust(30))+": k "+str(roudV(sysUnck*100))+" %     ,     k = "+ str(roudV(result2["kVal"]))+" "
    print "FINAL2: "+(sys.rjust(30))+": ttbb: "+str(roudV(sysUncTTBB*100))+" % "
    SystematicUnc[sys]=copy.deepcopy(sysUnc)
    SystematicUnck[sys]=copy.deepcopy(sysUnck)
    SystematicUncTTBB[sys]=copy.deepcopy(sysUncTTBB)

  """
  signals2= [GEN+'ttcc', GEN+'ttlf']
  backgrounds1= [GEN+"ttot"]
  backgrounds2= ['TTWlNu', 'TTWqq', 'TTZll', 'TTZqq', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ']
  backgrounds3= [ 'DYJets','DYJets10']
  higgs= ['ttH2non', 'ttH2bb']
  """
###############################################################################
###############################################################################
###############################################################################
elif int(arg3)==2:
  SystematicUnc,SystematicUnck,SystematicUncTTBB ={},{},{}
  histogramsMG5,freeTTB5,freeTTCC5,GEN5=loadHistogram("0", "0",Step,"csvweight")
  histogramsPOHP,freeTTBPOHP,freeTTCCPOHP,GENPOHP=loadHistogram("0", "2",Step,"csvweight")
  histogramsupPOW,freeTTBupPOW,freeTTCCupPOW,GENupPOW=loadHistogram("0", "4",Step,"csvweight")
  histogramsdwPOW,freeTTBdwPOW,freeTTCCdwPOW,GENdwPOW=loadHistogram("0", "5",Step,"csvweight")
  histogramSys = {}
  histogramSysGEN = {}

  for sys in sysWeights:
    #print "FINAL2: loadhistogram..... "+sys 
    histograms2,freeTTB2,freeTTCC2,GEN2=loadHistogram(arg1, arg2,Step,sys)
    histogramSys[sys] = copy.deepcopy(histograms2)
    histogramSysGEN[sys] = copy.deepcopy(GEN2)

  #print "FINAL2: "+str(sysWeights)
  orig_r,orig_err,result=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)

  #print "FINAL2: csvweight: R = "+ str(roudV(orig_r))+" \pm "+str(roudV(orig_err))+"$"
  eRPOW=POW2["Eff"]['ttjj']/POW2["Eff"]['ttbb']
  acPPOW=POW2["Acc"]['ttjj']/POW2["Acc"]['ttbb']
  genR      = orig_r*eRPOW 
  resultPrint3(result,POW2)
  genRerror = orig_r*eRPOW*orig_err/orig_r
  #print "FINAL2: csvweight: gen R $= "+ str(roudV(genR))+" \pm "+str(roudV(genRerror))+"$"
  genRF      = orig_r*eRPOW*acPPOW
  genRerrorF = orig_r*eRPOW*acPPOW*orig_err/orig_r
  kVal = result["kVal"]

  ttbbCenter = result["n_ttjj"]*kVal*orig_r

  print "FINAL2: csvweight: full gen R = "+ str(roudV(genRF))+" $\pm$ "+str(roudV(genRerrorF))+" "
  print "FINAL2: csvweight: k ="+str(roudV(result["kVal"]))+" $\pm$ "+str(roudV(result["kValerror"]))+" "

  #print "FINAL2: loading.Sys.. "+str( histogramSys["LF_Down"])
  #print "FINAL2: loading.GEN.. "+str( histogramSysGEN["LF_Down"])

  for sys in sysWeights:
    #print "FINAL2: fitting..... "+sys 
    orig_r2,orig_err2,result2=fitting(histogramSys[sys], freeTTB, freeTTCC, histogramSysGEN[sys],True,False)
    if orig_r==False or result2==False : continue
    sysUnc = getSys(orig_r,orig_r2)
    sysUnck = getSys(kVal,result2["kVal"])
    ttbbNew2 = result2["n_ttjj"]*result2["kVal"]*orig_r2
    sysUncTTBB = getSys(ttbbCenter, ttbbNew2)

    print "FINAL2: "+(sys.rjust(30))+": R "+str(roudV(sysUnc*100))+" %     ,     R = "+ str(roudV(orig_r2))+" "
    print "FINAL2: "+(sys.rjust(30))+": k "+str(roudV(sysUnck*100))+" %     ,     k = "+ str(roudV(result2["kVal"]))+" "
    print "FINAL2: "+(sys.rjust(30))+": TTBB "+str(roudV(sysUncTTBB*100))+" %     ,     TTBB = "+ str(roudV( ttbbNew2  ))+" "
    SystematicUnc[sys]=copy.deepcopy(sysUnc)
    SystematicUnck[sys]=copy.deepcopy(sysUnck)
    SystematicUncTTBB[sys]=copy.deepcopy(sysUncTTBB)
    #print "FINAL2: ttbb "+str(SystematicUncTTBB)
  #print "FINAL2: ---- "+str(SystematicUnc)+"------"
  orig_r3,orig_err3,result3 = fitting(histograms, True, False, GEN,True,False)
  orig_r4,orig_err4,result4 = fitting(histograms, False, True, GEN,True,False)
  orig_r5,orig_err5,result5 = fitting(histogramsMG5, False, False, "MG5",True,False)
  orig_r6,orig_err6,result6 = fitting(histogramsPOHP, False, False, "POHP",True,False)
  orig_r7,orig_err7,result7 = fitting(histogramsupPOW, False, False, "upPOW",True,False)
  orig_r8,orig_err8,result8 = fitting(histogramsdwPOW, False, False, "dwPOW",True,False)

  print "FINAL2: ----MG5 k="+str(result5["kVal"])

  eRMG5=MG52["Eff"]['ttjj']/MG52["Eff"]['ttbb']
  #acPMG5=MG52["Acc"]['ttjj']/MG52["Acc"]['ttbb']
  eRPOHP=POHP2["Eff"]['ttjj']/POHP2["Eff"]['ttbb']
  eRupPOW=upPOW2["Eff"]['ttjj']/upPOW2["Eff"]['ttbb']
  eRdwPOW=dwPOW2["Eff"]['ttjj']/dwPOW2["Eff"]['ttbb']
 
  sysUnc3 = getSys(orig_r,orig_r3)
  sysUnc3k = getSys(kVal,result3["kVal"])
  ttbbNew3 = result3["n_ttjj"]*result3["kVal"]*orig_r3
  sysUnc3ttbb = getSys(ttbbCenter,ttbbNew3)

  sysUnc4 = getSys(orig_r,orig_r4)
  sysUnc4k = getSys(kVal,result4["kVal"])
  ttbbNew4 = result4["n_ttjj"]*result4["kVal"]*orig_r4
  sysUnc4ttbb = getSys(ttbbCenter,ttbbNew4)
  sysUnc5 = (genR-orig_r5*eRMG5)/genR
  #sysUnc5 = (orig_r-orig_r5)/orig_r
  sysUnc5k = getSys(kVal,result5["kVal"])
  ttbbNew5 = result5["n_ttjj"]*result5["kVal"]*orig_r5
  sysUnc5ttbb = getSys(ttbbCenter,ttbbNew5)

  sysUnc6 = (genR-orig_r6*eRPOHP)/genR
  sysUnc6k = getSys(kVal,result6["kVal"])
  ttbbNew6 = result6["n_ttjj"]*result6["kVal"]*orig_r6
  sysUnc6ttbb = getSys(ttbbCenter,ttbbNew6)

  sysUnc7 = (genR-orig_r7*eRupPOW)/genR
  sysUnc7k = getSys(kVal,result7["kVal"])
  ttbbNew7 = result7["n_ttjj"]*result7["kVal"]*orig_r7
  sysUnc7ttbb = getSys(ttbbCenter,ttbbNew7)

  sysUnc8 = (genR-orig_r8*eRdwPOW)/genR
  sysUnc8k = getSys(kVal,result8["kVal"])
  ttbbNew8 = result8["n_ttjj"]*result8["kVal"]*orig_r8
  sysUnc8ttbb = getSys(ttbbCenter,ttbbNew8)


  sysUnc=0.
  #print "FINAL2: ttbb "+str(SystematicUncTTBB)
  for sys2 in StepSys2.keys():
    sysUnc1=[]
    sysUnc1k=[]
    sysUnc1ttbb=[]
    for sys3 in StepSys2[sys2]:
      if sys3.find("JER")>-1:
        up=SystematicUnc[sys3+"_Up"] 
        upk=SystematicUnck[sys3+"_Up"] 
        upttbb=SystematicUncTTBB[sys3+"_Up"] 
        dw=SystematicUnc[sys3+"_Down"] 
        dwk=SystematicUnck[sys3+"_Down"] 
        dwttbb=SystematicUncTTBB[sys3+"_Down"] 
      else:
        up=SystematicUnc[sys3+"_Up"] 
        upk=SystematicUnck[sys3+"_Up"] 
        upttbb=SystematicUncTTBB[sys3+"_Up"] 
        dw=SystematicUnc[sys3+"_Down"] 
        dwk=SystematicUnck[sys3+"_Down"] 
        dwttbb=SystematicUncTTBB[sys3+"_Down"] 
      sysUnc1.append(max(abs(up),abs(dw)))
      sysUnc1k.append(max(abs(upk),abs(dwk)))
      sysUnc1ttbb.append(max(abs(upttbb),abs(dwttbb)))

    sysUnc = quardsum(sysUnc1)
    sysUnck = quardsum(sysUnc1k)
    sysUncTTBB = quardsum(sysUnc1ttbb)
    #print "FINAL2: "+sys2.rjust(10)+": R : "+str(roudV(sysUnc*100))+" % ,     k="+str(roudV(sysUnck*100))+" %, ttbb: "+str(roudV(quardsum([sysUnc,sysUnck])*100))+" %"
    print "FINAL2: "+sys2.rjust(10)+": & "+str(roudV(sysUnc*100)).rjust(10)+"  & "+str(roudV(sysUnck*100)).rjust(10)+" & "+str(roudV(sysUncTTBB*100)).rjust(10)+"  \\\\ "
    sysUnc = 0.

  print "FINAL2: "+("TTB").rjust(5)+" : "+str(roudV(sysUnc3*100)).rjust(10)+"  &  "+str(roudV(sysUnc3k*100)).rjust(10)+"   &    "+str(roudV(sysUnc3ttbb*100)).rjust(10)+"   \\\\  "
  print "FINAL2: "+("TTCC").rjust(5)+" : "+str(roudV(sysUnc4*100)).rjust(10)+"  &  "+str(roudV(sysUnc4k*100)).rjust(10)+"   &   "+str(roudV(sysUnc4ttbb*100)).rjust(10)+"   \\\\  "
  print "FINAL2: "+("GEN").rjust(5)+" : "+str(roudV(sysUnc5*100)).rjust(10)+"  &  "+str(roudV(sysUnc5k*100)).rjust(10)+"   &    "+str(roudV(sysUnc5ttbb*100)).rjust(10)+"   \\\\  "
  print "FINAL2: "+("POHP").rjust(5)+" : "+str(roudV(sysUnc6*100)).rjust(10)+"  &  "+str(roudV(sysUnc6k*100)).rjust(10)+"   &   "+str(roudV(sysUnc6ttbb*100)).rjust(10)+"   \\\\  "
  print "FINAL2: "+("upPOW").rjust(5)+" : "+str(roudV(sysUnc7*100)).rjust(10)+"  &  "+str(roudV(sysUnc7k*100)).rjust(10)+"   &  "+str(roudV(sysUnc7ttbb*100)).rjust(10)+"   \\\\  "
  print "FINAL2: "+("dwPOW").rjust(5)+" : "+str(roudV(sysUnc8*100)).rjust(10)+"  &  "+str(roudV(sysUnc8k*100)).rjust(10)+"   &  "+str(roudV(sysUnc8ttbb*100)).rjust(10)+"   \\\\  "
 
  """
  print "FINAL2: "+("TTB").rjust(5)+" : "+str(roudV(sysUnc3*100))+" % ,     k="+str(roudV(sysUnc3k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc3,sysUnc3k])*100))+" %"
  print "FINAL2: "+("TTCC").rjust(5)+" : "+str(roudV(sysUnc4*100))+" % ,     k="+str(roudV(sysUnc4k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc4,sysUnc4k])*100))+" %"
  print "FINAL2: "+("GEN").rjust(5)+" : "+str(roudV(sysUnc5*100))+" % ,     k="+str(roudV(sysUnc5k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc5,sysUnc5k])*100))+" %"
  print "FINAL2: "+("POHP").rjust(5)+" : "+str(roudV(sysUnc6*100))+" % ,     k="+str(roudV(sysUnc6k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc6,sysUnc6k])*100))+" %"
  print "FINAL2: "+("upPOW").rjust(5)+" : "+str(roudV(sysUnc7*100))+" % ,     k="+str(roudV(sysUnc7k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc7,sysUnc7k])*100))+" %"
  print "FINAL2: "+("dwPOW").rjust(5)+" : "+str(roudV(sysUnc8*100))+" % ,     k="+str(roudV(sysUnc8k*100))+" %, ttbb:  "+str(roudV(quardsum([sysUnc8,sysUnc8k])*100))+" %"
  """
  print "FINAL2: ---------------- "#+str(SystematicUnc)+"------"
  




