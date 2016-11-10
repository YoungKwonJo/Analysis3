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

  h1_data = th2DtoTH1D(histograms["DATA"]["h1"])
  h1_ttbb = th2DtoTH1D(histograms[GEN+"ttbb"]["h1"]) 
  h1_ttb = th2DtoTH1D(histograms[GEN+"ttb"]["h1"]) 
  h1_tt2b = th2DtoTH1D(histograms[GEN+"tt2b"]["h1"]) 
  h1_ttcc = th2DtoTH1D(histograms[GEN+"ttcc"]["h1"]) 
  h1_ttlf = th2DtoTH1D(histograms[GEN+"ttlf"]["h1"]) 
  h1_ttcclf = th2DtoTH1D(histograms[GEN+"ttcclf"]["h1"]) 

  h1_ttot = th2DtoTH1D(histograms[GEN+"ttot"]["h1"]) 
  h1_bkg = th2DtoTH1D(histograms["bkg"]["h1"]) 
  h1_ddbkg = th2DtoTH1D(histograms["ddbkg"]["h1"]) 


  if n_ttjj==0:  return False,False,False
  
  rttbb = n_ttbb/n_ttjj
  rttb  = n_ttb/n_ttjj
  rtt2b  = n_tt2b/n_ttjj
  rttcc = (n_ttcc)/n_ttjj
  
 
  h1_data2 = h1_data.Clone("data2")
  h1_data2.Add(h1_bkg,-1.)
  h1_data2.Add(h1_ddbkg,-1.)
  h1_data2.Add(h1_ttot,-0.8425)

  h1_ttb3 = h1_ttb.Clone("ttb3")
  h1_ttb3.Add(h1_tt2b)
  h1_ttb3.Add(h1_ttbb)
  
  h1_bkgAll3 = h1_bkg.Clone("BkgAll")
  h1_bkgAll3.Add(h1_ddbkg)

  h1_ttcclf3 = h1_ttcclf.Clone("ttcclf3")
  #h1_ttcclf1b2b3.Add(h1_ttb)
  #h1_ttcclf1b2b3.Add(h1_tt2b)

  mc = TObjArray(3)
  #mc.Add(h1_ttbb)
  mc.Add(h1_ttb3)
  mc.Add(h1_ttcclf3)
  ##mc.Add(h1_ttlf)
  #mc.Add(h1_ttot)
  ##mc.Add(h1_bkg)
  ##mc.Add(h1_ddbkg)
  fit = TFractionFitter(h1_data2, mc)
  fit.Constrain(0,0.0001,0.4)
  #fit.Constrain(1,0.0001,0.4)
  fit.Constrain(1,0.7,0.999)
  #fit.Constrain(3,0.011,0.4)
  fit.SetRangeX(1,100)
  #fit.SetMC(parameter , );

  status = int(fit.Fit())
  print "status : "+str(status)
  ###############
  print "NDF:"+str(fit.GetNDF() )
  print "Chi^2:"+str(fit.GetChisquare())
  rrr,rrr_error=ROOT.Double(0),ROOT.Double(0)
  fit.GetResult(0,rrr,rrr_error)
  print "R : "+str(rrr)+" +- "+str(rrr_error)

  cRAAA = TCanvas("RAAA", "AAA", 1)#500, 500)
  result = h1_bkg.Clone("result")
  result.Reset()
  result.Add(fit.GetPlot())
  result.SetLineColor(kRed)
  h1_data2.Draw("")
  result.Draw("same")
  leg=make_legend(0.5,0.8,0.88,0.88)
  leg.AddEntry(result, "t#bar{t}jj ", "l")
  leg.AddEntry(h1_data2, "Data - (Bkg. + t#bar{t} others)", "ep")
  leg.Draw()
  #n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  #n_ttbar = n_ttjj+n_ttot
  r_ttbb_ttb = n_ttbb/(n_ttbb+n_ttb+n_tt2b) 


  leg2=addLegend2("(ttbj+ttbb)/ttjj : "+str(round(rrr*10000)/10000)+" #pm "+str(round(rrr_error*100000)/100000),0.46,0.75)
  leg3=addLegend2("ttbb/ttjj : "+str(round(rrr*r_ttbb_ttb*10000)/10000)+" #pm "+str(round(rrr_error*100000*r_ttbb_ttb)/100000),0.46,0.7)
  leg4=addLegend2("NDF : "+str(fit.GetNDF())+", #chi^2 : "+str(round(fit.GetChisquare()*10)/10),0.46,0.65)
  leg2.Draw()
  leg3.Draw()
  leg4.Draw()

  cRAAA.Print("TFraction.pdf")

  return cRAAA,h1_data2,result,leg,leg2,leg3,leg4


################
################
################
################
################
################
################
################
def th2DtoTH1D(h2):
  binN    = 55# h2.GetNbinsX()*h2.GetNbinsY()
  h1   =  TH1D(h2.GetName()+"__","",binN,0.,55)
  for i in range(1,h2.GetNbinsX()+1):
    j=0
    for jj in range(1,h2.GetNbinsY()+1):
      if i>=jj:
        j+=1
        #ij = i*(h2.GetNbinsX()-1)+j
        ij = sum(range(0,i))+(j)
        h1.SetBinContent  (ij,h2.GetBinContent  (i,jj) )
        h1.SetBinError    (ij,h2.GetBinError    (i,jj) )
  return h1


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
  ttbbSF=1.62796470428
  ttcclfSF=0.916707908424
  k=0.842498214663
  #ttbb.Scale(ttbbSF*k)
  #ttb.Scale(ttbbSF*k)
  #tt2b.Scale(ttbbSF*k)
  #ttcclf.Scale(ttcclfSF*k)
  #ttot.Scale(k)

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


Step="S6"

histograms,freeTTB,freeTTCC,GEN=loadHistogram(arg1, arg2,Step,"csvweight")
orig_r,orig_err = 0.,0. 
#Chi2Test2D(GEN,histograms)

from math import *
cR10 = fitting(histograms, freeTTB, freeTTCC, GEN,False,False)

