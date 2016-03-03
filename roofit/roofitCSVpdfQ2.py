#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy


lumi = 2260.
#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160204_ttbb_roofit/histogram/"
loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160224_763/histogram20160225/"
loc2 = "/Users/youngkwonjo/Documents/CMS/Analysis/20160224_763/histogram20160225Q2/"

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

######################
def relpaceTTbarPOW(oldHistograms,updw):
  histograms2 = {}
  for key in oldHistograms.keys():
    if key.find(updw+"POW")>-1:
      name = key.replace(updw,"")
      histograms2[name]=oldHistograms[key]
  oldHistograms.update(histograms2)

def loadHistogramTTbarPOW(oldHistograms, Step, Weight1):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
  from mcsample_cfi import mcsamples
  mcsamples = [ x for x in mcsamples if x["name"].find("POW")>-1 ]
  #from sysWeightQ2_cfi import 

  GEN="POW"
  #histograms = ["name":"name","hist": ]
  histograms = {}
  f = TFile.Open(loc2+"/hist_pdfQ2.root")

  for mc in mcsamples:
    name = mc['name']
    #color = mc['ColorLabel']['color'] 
    #histnameMM = "h2_"+name+"_"+HN+"_mm_"+Step
    #print name
    #print name+"/"+Weight+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight
    h1 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1).Clone("h2_"+name+"_"+Step+"LL"+"_"+Weight1)
    h2 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_ee_"+Step+"_"+Weight1)
    h3 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_em_"+Step+"_"+Weight1)
    if h1.Integral()>0 :  h1.Scale(mc['cx']*lumi)
    if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
    if h3.Integral()>0 :  h3.Scale(mc['cx']*lumi)

    h1.Add(h2)
    h1.Add(h3)
  
    h1111 = "h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1
    h11 = TH1F(h1111,"",1,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1):
      h11 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1).Clone("h11_"+name+"_"+Step+"LL"+"_"+Weight1)
      h21 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_ee_"+Step+"_"+Weight1)
      h31 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_em_"+Step+"_"+Weight1)
      h11.Add(h21)
      h11.Add(h31)
  
    #ci = TColor.GetColor(mc['ColorLabel']['color'])  
    #h11.SetLineColor(ci)
    #h111.SetLineColor(ci)
  
    h1222 = "h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1
    h12 = TH1F(h1222,"",1,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1):
      h12 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1).Clone("h12_"+name+"_"+Step+"LL"+"_"+Weight1)
      h22 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_ee_"+Step+"_"+Weight1)
      h32 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_em_"+Step+"_"+Weight1)
      h12.Add(h22)
      h12.Add(h32)
  
    #ci = TColor.GetColor(mc['ColorLabel']['color'])  
    #h12.SetLineColor(ci)
    #h122.SetLineColor(ci)
  
    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12)}
    #print "FINAL2 "+name+"  "+str(histograms[name]["exp"])


  #print str(histograms.keys())
  #print "closingg... f "
  f.Close()
  oldHistograms.update(histograms)

######################
def loadHistogram(arg1, arg2, Step, Weight):
  HN = "jet3CSV_jet4CSV"                                                                                                          
  HN1 = "jet3CSV"
  HN2 = "jet4CSV"
  from mcsample_cfi import mcsamples,datasamples 
  #lumi = 2110. 
  #Step = "S6csvweight"
  #Step2 = "S6"
  
  freeTTB  = False
  freeTTCC = False
  if int(arg1)==1 : freeTTB=True
  if int(arg1)==2 : freeTTCC=True
  if int(arg1)==3 : 
    freeTTCC=True
    freeTTB=True
  
  GEN="MG5"
  if int(arg2)==1 : GEN="POW"
#  if int(arg2)==2 : GEN="AMC"
  
  #histograms = ["name":"name","hist": ]
  histograms = {}
  histograms2 = {}
  dy_ee_sf,dy_mm_sf = 1.14618572215,0.844371813284
  #dy_ee_sf = 1.17764007675
  #dy_mm_sf = 0.894244897143

  Weight1= Weight
  if Weight is "Scale_Up":   Weight1="csvweight"
  if Weight is "Scale_Down": Weight1="csvweight"
  scale=""
  if Weight is "Scale_Up":   scale="up"
  if Weight is "Scale_Down": scale="dw"

  f = TFile.Open(loc+"/hist_"+Weight1+".root")
  for mc in mcsamples:
    name = mc['name']
    #color = mc['ColorLabel']['color'] 
    #histnameMM = "h2_"+name+"_"+HN+"_mm_"+Step
    #print name
    #print name+"/"+Weight+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight
    h1 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_mm_"+Step+"_"+Weight1).Clone("h2_"+name+"_"+Step+"LL"+"_"+Weight1)
    h2 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_ee_"+Step+"_"+Weight1)
    h3 = f.Get(name+"/"+Weight1+"/h2_"+name+"_"+HN+"_em_"+Step+"_"+Weight1)
    if h1.Integral()>0 :  h1.Scale(mc['cx']*lumi)
    if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
    if h3.Integral()>0 :  h3.Scale(mc['cx']*lumi)
    if name.find("DYJets")>-1:
      h1.Scale(dy_mm_sf)
      h2.Scale(dy_ee_sf)

    h1.Add(h2)
    h1.Add(h3)
  
    h1111 = "h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1
    h11 = TH1F(h1111,"",1,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1):
      h11 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_mm_"+Step+"_"+Weight1).Clone("h11_"+name+"_"+Step+"LL"+"_"+Weight1)
      h21 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_ee_"+Step+"_"+Weight1)
      h31 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN1+"_em_"+Step+"_"+Weight1)
      if name.find("DYJets")>-1:
        h11.Scale(dy_mm_sf)
        h21.Scale(dy_ee_sf)
      
      h11.Add(h21)
      h11.Add(h31)
  
    #ci = TColor.GetColor(mc['ColorLabel']['color'])  
    #h11.SetLineColor(ci)
    #h111.SetLineColor(ci)
  
    h1222 = "h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1
    h12 = TH1F(h1222,"",1,0,1)
    if None != f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1):
      h12 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_mm_"+Step+"_"+Weight1).Clone("h12_"+name+"_"+Step+"LL"+"_"+Weight1)
      h22 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_ee_"+Step+"_"+Weight1)
      h32 = f.Get(name+"/"+Weight1+"/h1_"+name+"_"+HN2+"_em_"+Step+"_"+Weight1)
      if name.find("DYJets")>-1:
        h12.Scale(dy_mm_sf)
        h22.Scale(dy_ee_sf)
      h12.Add(h22)
      h12.Add(h32)
  
    #ci = TColor.GetColor(mc['ColorLabel']['color'])  
    #h12.SetLineColor(ci)
    #h122.SetLineColor(ci)
  
    histograms[name]={"h1":copy.deepcopy(h1),"exp":h1.Integral(),"h11":copy.deepcopy(h11),"h12":copy.deepcopy(h12)}
    #print "FINAL2 "+name+"  "+str(histograms[name]["exp"])


  #print str(histograms.keys())
  #print "closingg... f "
  f.Close()
  #for datesmaples
  #WeightData = Weight1.replace("csvweight_","")
  #WeightData2 = Weight1
  #if not Weight in ["JES_Up","JES_Down"]:
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
  
  signals1= [GEN+'ttbb', GEN+'ttb',GEN+'tt2b']
  signals2= [GEN+'ttcc', GEN+'ttlf']#, GEN+'ttot']
  backgrounds1= [GEN+"ttot"]
  backgrounds2= ['TTWlNu', 'TTWqq', 'TTZll', 'TTZqq', 'STbt', 'STt', 'STbtW', 'STtW', 'WJets', 'WW', 'WZ', 'ZZ']
  backgrounds3= [ 'DYJets','DYJets10']
  higgs= ['ttH2non', 'ttH2bb']
 
  #signals1up= ["up"+GEN+'ttbb', "up"+GEN+'ttb']
  #signals1dw= ["dw"+GEN+'ttbb', "dw"+GEN+'ttb']
  #signals2up = ["up"+GEN+'ttcc', "up"+GEN+'ttlf']
  #signals2dw = ["dw"+GEN+'ttcc', "dw"+GEN+'ttlf']
  #backgrounds1up= ["up"+GEN+"ttot"]
  #backgrounds1dw= ["dw"+GEN+"ttot"]
  bkghist = histograms[GEN+'ttot']["h1"].Clone("bkghist")
  bkghist.Reset()
  ddbkghist = histograms[GEN+'ttot']["h1"].Clone("ddbkghist")
  ddbkghist.Reset()
  
  ttcclfhist = histograms[GEN+'ttot']["h1"].Clone("ttcclfhist")
  ttcclfhist.Reset()

  for hh in signals1:
    h = histograms[scale+hh]
    #h = histograms[hh]
    histograms2[hh]=h 
 
  for hh in signals2:
    h = histograms[scale+hh]["h1"]
    #h = histograms[hh]["h1"]
    h2 = histograms[scale+hh]
    ttcclfhist.Add(h)
    histograms2[hh]=h2
  histograms2[GEN+"ttcclf"]={"h1":copy.deepcopy(ttcclfhist),"exp":ttcclfhist.Integral()}

  for hh in backgrounds1:
    h = histograms[scale+hh]
    #h = histograms[hh]
    histograms2[GEN+"ttot"]=h

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

  return histograms2, freeTTB, freeTTCC,GEN

##############################################
##############################################
##############################################
##############################################
def resultPrint(result, freeTTB, freeTTCC, GEN):
  return resultPrint2(result, freeTTB, freeTTCC, GEN, True)

def resultPrint2(result, freeTTB, freeTTCC, GEN, isPrint):

  if isPrint : print "FINAL: ----------------------   "
  if isPrint : print "FINAL: MC:"+ str(GEN)
  fsig = result["fsig"]
  rttbb = result["rttbb"]
  recoR      = fsig.getVal()
  recoRerror = fsig.getError()
  if isPrint : print "FINAL: prefit: R="+str(round(rttbb*10000)/10000)
  if isPrint : print "FINAL: $R = "+ str(round(recoR*10000)/10000)+" \pm "+str(round(recoRerror*10000)/10000)+"$"
  
  recoR2=1.
  recoR3=1.
  recoR2error=0.0
  recoR3error=0.0
  if freeTTB:
    if isPrint : print "FINAL: freeTTB : "+str(freeTTB)
    fsig2 = result["fsig2"]
    fsig3 = result["fsig3"]
    rttb = result["rttb"]
    rtt2b = result["rtt2b"]
    recoR2      = fsig2.getVal()
    recoR3      = fsig3.getVal()
    recoR2error = fsig2.getError()
    recoR3error = fsig3.getError()
    if isPrint : print "FINAL: prefit: R2="+str(round(rttb*10000)/10000)
    if isPrint : print "FINAL: $R2 = "+ str(round(recoR2*10000)/10000)+" \pm "+str(round(recoR2error*10000)/10000)+"$"
    if isPrint : print "FINAL: prefit: R3="+str(round(rtt2b*10000)/10000)
    if isPrint : print "FINAL: $R3 = "+ str(round(recoR3*10000)/10000)+" \pm "+str(round(recoR3error*10000)/10000)+"$"
  else:
    if isPrint : print "FINAL: freeTTB : "+str(freeTTB)
    fsig2con = result["fsig2con"]
    fsig3con = result["fsig3con"]
    recoR2      = fsig2con.getVal()
    recoR3      = fsig3con.getVal()
    rttb = result["rttb"]
    rtt2b = result["rtt2b"]
    #recoR2error = fsig2con.getError()
    if isPrint : print "FINAL: prefit: R2="+str(round(rttb*10000)/10000)
    if isPrint : print "FINAL: $R2 = "+ str(round(recoR2*10000)/10000)#+" \pm "+str(round(recoR2error*10000)/10000)+"$"
    if isPrint : print "FINAL: prefit: R3="+str(round(rtt2b*10000)/10000)
    if isPrint : print "FINAL: $R3 = "+ str(round(recoR3*10000)/10000)#+" \pm "+str(round(recoR3error*10000)/10000)+"$"
  
  recoRcc=1.
  recoRccerror=0.0
  if freeTTCC:
    if isPrint : print "FINAL: freeTTCC : "+str(freeTTCC)
    fsigcc = result["fsigcc"]
    rttcc = result["rttcc"]
    recoRcc      = fsigcc.getVal()
    recoRccerror = fsigcc.getError()
    if isPrint : print "FINAL: prefit: Rcc="+str(round(rttcc*10000)/10000)
    if isPrint : print "FINAL: $Rcc = "+ str(round(recoRcc*10000)/10000)+" \pm "+str(round(recoRccerror*10000)/10000)+"$"
  else:
    if isPrint : print "FINAL: freeTTCC : "+str(freeTTCC)
    #recoRcc      = fsigcc.getVal()
    #recoRccerror = fsigcc.getError()
    rttcc = result["rttcc"]
    if isPrint : print "FINAL: prefit: Rcc="+str(round(rttcc*10000)/10000)
    #if isPrint : print "FINAL: $Rcc = "+ str(round(recoRcc*10000)/10000)+" \pm "+str(round(recoRccerror*10000)/10000)+"$"
  
  
  k = result["k"]
  kVal      = k.getVal()
  kValerror = k.getError()
  if isPrint : print "FINAL: $k = "+str(round(kVal*10000)/10000)+" \pm "+str(round(kValerror*10000)/10000)+"$"
  result2 = {
      "recoR":copy.deepcopy(recoR), "recoRerror":copy.deepcopy(recoRerror),
      "recoR2":copy.deepcopy(recoR2), "recoR2error":copy.deepcopy(recoR2error),
      "recoR3":copy.deepcopy(recoR3), "recoR3error":copy.deepcopy(recoR3error),
      "recoRcc":copy.deepcopy(recoRcc), "recoRccerror":copy.deepcopy(recoRccerror),
      "kVal":copy.deepcopy(kVal), "kValerror":copy.deepcopy(kValerror)
      }

  return result2 
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

  
  rttbb = n_ttbb/n_ttjj
  rttb  = n_ttb/n_ttjj
  rtt2b  = n_tt2b/n_ttjj
  #rtt2b = n_tt2b/n_ttjj
  rttcc = (n_ttcc)/n_ttjj
  
  x=RooRealVar("x","x",histograms["bkg"]["h1"].GetXaxis().GetXmin(),histograms["bkg"]["h1"].GetXaxis().GetXmax()) 
  y=RooRealVar("y","y",histograms["bkg"]["h1"].GetYaxis().GetXmin(),histograms["bkg"]["h1"].GetYaxis().GetXmax()) 
  
  RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
  RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
  Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
  RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);
  
  fsig   =RooRealVar(    "fsig",                "fsig",           rttbb, 0.0, 0.18) 
  fsig2con  =RooFormulaVar("fsig2con",          "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )  # constraint fsig2 with fsig
  fsig3con  =RooFormulaVar("fsig3con",          "fsig3","@0/@1*@2",RooArgList(fsig,RttbbReco,Rtt2bReco) )  # constraint fsig2 with fsig
  fsig2  =RooRealVar(   "fsig2",                "fsig2",          rttb, 0.0, 0.3)  # free fsig2
  fsig3  =RooRealVar(   "fsig3",                "fsig3",          rtt2b, 0.0, 0.3)  # free fsig3
  fsigcc =RooRealVar(  "fsigcc",              "fsigcc",           rttcc, 0.0, 0.4)  # free fsigcc
  k      =RooRealVar(       "k","normalization factor",           1, 0.5, 1.5) 
  
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
  
  #for separate ttcc
  if freeTTB and not freeTTCC  : model  = RooAddPdf("model",   "model",RooArgList( ttbbpdf, ttbpdf,tt2bpdf, ttcclfpdf), RooArgList(fsig,fsig2,fsig3))
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
  result2=resultPrint2(result, freeTTB, freeTTCC, GEN, True)
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
  l1.AddEntry(lineTbb,"prefit: R="+str(round(rttbb*10000)/10000),"l")
  l1.AddEntry(lineKKK,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","l")
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
  l1K.AddEntry(lineKKK,"fit: k="+str(round(kVal*10000)/10000)+" #pm "+str(round(kValerror*10000)/10000)+"","l")
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
  chi2 = xframe.chiSquare(2)
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
  
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
  
    l2 = make_legend(0.49,0.7,0.93,0.88)
    l2.AddEntry(preM,"prefit: R="+str(round(rttbb*10000)/10000),"p")
    l2.AddEntry(preM,"prefit: R2="+str(round(rttb*10000)/10000),"p")
  
    l2.AddEntry(preM2,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","p")
    l2.AddEntry(preM2,"fit: R2="+str(round(recoR2*10000)/10000)+" #pm "+str(round(recoR2error*10000)/10000)+"","p")
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
    l21.AddEntry(preM21,"prefit: R="+str(round(rttbb*10000)/10000),"p")
    l21.AddEntry(preM21,"prefit: R3="+str(round(rtt2b*10000)/10000),"p")
  
    l21.AddEntry(preM22,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","p")
    l21.AddEntry(preM22,"fit: R3="+str(round(recoR3*10000)/10000)+" #pm "+str(round(recoR3error*10000)/10000)+"","p")
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
    l2.AddEntry(preM,"prefit: R="+str(round(rttbb*10000)/10000),"p")
    l2.AddEntry(preM,"prefit: Rcc="+str(round(rttcc*10000)/10000),"p")
    l2.AddEntry(preM2,"fit: R="+str(round(recoR*10000)/10000)+" #pm "+str(round(recoRerror*10000)/10000)+"","p")
    l2.AddEntry(preM2,"fit: Rcc="+str(round(recoRcc*10000)/10000)+" #pm "+str(round(recoRccerror*10000)/10000)+"","p")
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
  histograms[GEN+"ttbb"]["h11"].SetLineColor(kRed)
  histograms[GEN+"ttb"]["h11"].SetLineColor(kOrange)
  histograms[GEN+"tt2b"]["h11"].SetLineColor(kGreen)
  histograms[GEN+"ttcc"]["h11"].SetLineColor(kBlue)
  histograms[GEN+"ttlf"]["h11"].SetLineColor(kViolet)


  normH1=histograms[GEN+"ttbb"]["h11"].DrawNormalized()
  normH1.SetMaximum(normH1.GetMaximum()*2.0)

  normH1.Draw("HIST")
  histograms[GEN+"ttb"]["h11"].DrawNormalized("sameHIST")
  histograms[GEN+"tt2b"]["h11"].DrawNormalized("sameHIST")
  histograms[GEN+"ttcc"]["h11"].DrawNormalized("sameHIST")
  histograms[GEN+"ttlf"]["h11"].DrawNormalized("sameHIST")
  l21 = make_legend(0.69,0.6,0.85,0.88)
  l21.AddEntry(histograms[GEN+"ttbb"]["h11"],"ttbb","l")
  l21.AddEntry(histograms[GEN+"ttb"]["h11"],"ttb","l")
  l21.AddEntry(histograms[GEN+"tt2b"]["h11"],"tt2b","l")
  l21.AddEntry(histograms[GEN+"ttcc"]["h11"],"ttcc","l")
  l21.AddEntry(histograms[GEN+"ttlf"]["h11"],"ttlf","l")
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
  normH2.SetMaximum(normH2.GetMaximum()*2.8)
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
def roundStr(val,n):
  return str(round(val*pow(10,n))/pow(10,n))

def roundStrP(val,n):
  return str(round(val*pow(10,n+2))/pow(10,n))+" \\%"


def resultPrint(result, genInfo):

  #eR = genInfo["eR"]
  #acP = genInfo["acP"]
  ttjjAcp = genInfo["Acceptance"]["ttjj"]
  ttbbAcp = genInfo["Acceptance"]["ttbb"]

  ttjjEff = genInfo["effciency"]["ttjj"]
  ttbbEff = genInfo["effciency"]["ttbb"]

  rttbb= result["rttbb"][0]

  n_ttjj = result["n_ttbb"] + result["n_ttb"] + result["n_ttcc"] + result["n_ttlf"]
  print "FINAL2:  "+str(result["n_ttbb"]) +"  "+ str(result["n_ttb"]) +"  "+ str(result["n_ttcc"]) +"   "+ str(result["n_ttlf"])
  print "FINAL2: "+str(n_ttjj)

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

  print "FINAL2: ---------------------"

  print "FINAL2: R full : "+roundStrP(genInfo["Rfull"],4)+"  "
  print "FINAL2: R_vis : " +roundStrP(genInfo["Rvis"],4)+"  "

  print "FINAL2: Acceptance ttjj : "+roundStrP(ttjjAcp,4)+"  "
  print "FINAL2: Acceptance ttbb : "+roundStrP(ttbbAcp,4)+"  "

  print "FINAL2: efficiency ttjj : "+roundStrP(ttjjEff,4)+" "
  print "FINAL2: efficiency ttbb : "+roundStrP(ttbbEff,4)+" "

  print "FINAL2: ---------------------"

  print "FINAL2: #ttjj prefit = "+str(round(n_ttjj*100)/100)+"  "
  print "FINAL2: #ttjj fitting = "+str(round(NewNttjj*100)/100)+"  "
  print "FINAL2: #ttbb fitting = "+str(round(NewNttbb*100)/100)+"  "


  print "FINAL2:Reco  R = "+ str(round(recoR*10000)/10000)+" \pm "+str(round(recoRerror*10000)/10000)+" "
  print "FINAL2:vis   R = "+ str(round(genR*10000)/10000)+" \pm "+str(round(genRerror*10000)/10000)+" "
  fullR    = (genR*ttjjAcp/ttbbAcp)
  fullRerr = (genR*ttjjAcp/ttbbAcp)*(genRerror/genR)
  print "FINAL2:full  R = "+ str(round(fullR*10000)/10000)+" \pm "+str(round(fullRerr*10000)/10000)+" "

  print "FINAL2:vis   ttbb :"+str(NewCXttbbvis)+" pb"
  print "FINAL2:vis   ttjj :"+str(NewCXttjjvis)+" pb"

  print "FINAL2:full ll   ttbb :"+str(NewCXttbbfull)+" pb"
  print "FINAL2:full ll  ttjj :"+str(NewCXttjjfull)+" pb"
  print "FINAL2:ll r : "+str(RdilepPOW)
  print "FINAL2:full   ttbb :"+str(NewCXttbbfull/RdilepPOW)+" pb"
  print "FINAL2:full   ttjj :"+str(NewCXttjjfull/RdilepPOW)+" pb"
 


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
#POWHEG###################################
POWhadronic,POWdileptonic,POWsemileptonic,POWetc=44760741.,10286981.,42910959.,13251918.
POWttbbF,POWttbjF,POWttccF,POWttlfF=43181.,160433.,91034.,3637828.
POWttbbV,POWttbjV,POWttccV,POWttlfV=8204.,31131.,15380.,546875.
POWttbarall    =POWhadronic+POWdileptonic+POWsemileptonic+POWetc
POWttjjF = POWttbbF+POWttbjF+POWttccF+POWttlfF
ttjjRatioTTPOW = (POWttjjF/POWttbarall)
POWttjjV = POWttbbV+POWttbjV+POWttccV+POWttlfV

POWttbbS6 = 2248.0
POWttjjS6 = 71719.0

ttjjAcceptancePOW = (POWttjjV/POWttjjF)
ttbbAcceptancePOW = (POWttbbV/POWttbbF)
ttjjEffPOW = POWttjjS6 / POWttjjV
ttbbEffPOW = POWttbbS6 / POWttbbV
RfullPOW = POWttbbF/POWttjjF
RvisPOW =  POWttbbV/POWttjjV
RdilepPOW = POWdileptonic/POWttbarall

#MG5 ########################################
MG5hadronic,MG5dileptonic,MG5semileptonic,MG5etc=4542315.,1135379.,4538140.,1416369.0
MG5ttbbF,MG5ttbjF,MG5ttccF,MG5ttlfF=4911.,18816.,10817.,428760.
MG5ttbbV,MG5ttbjV,MG5ttccV,MG5ttlfV=949.,3758.,1881.,66365.
MG5ttbarall = MG5hadronic+MG5dileptonic+MG5semileptonic+MG5etc
MG5ttjjF = MG5ttbbF+MG5ttbjF+MG5ttccF+MG5ttlfF
MG5ttjjRatioTT = (MG5ttjjF/MG5ttbarall)
MG5ttjjV = MG5ttbbV+MG5ttbjV+MG5ttccV+MG5ttlfV

MG5ttbbS6 = 261.0
MG5ttjjS6 = 9017.0

ttjjAcceptanceMG5= (MG5ttjjV/MG5ttjjF)
ttbbAcceptanceMG5= (MG5ttbbV/MG5ttbbF)
ttjjEffMG5 = (MG5ttjjS6/MG5ttjjV)
ttbbEffMG5 = (MG5ttbbS6/MG5ttbbV)
RfullMG5   = (MG5ttbbF/MG5ttjjF)
RvisMG5    = (MG5ttbbV/MG5ttjjV)
RdilepMG5 = MG5dileptonic/MG5ttbarall

eRPOW = ttjjEffPOW/ttbbEffPOW 
acPPOW = ttjjAcceptancePOW/ttbbAcceptancePOW
#eRAMC = ttjjEffAMC/ttbbEffAMC 
#acPAMC = ttjjAcceptanceAMC/ttbbAcceptanceAMC
eRMG5 = ttjjEffMG5/ttbbEffMG5 
acPMG5 = ttjjAcceptanceMG5/ttbbAcceptanceMG5

genInfoPOW = {"Acceptance":{"ttjj":ttjjAcceptancePOW,"ttbb":ttbbAcceptancePOW }, "effciency":{ "ttjj":ttjjEffPOW,"ttbb":ttbbEffPOW  }, "eR":eRPOW, "acP":acPPOW, "Rfull": RfullPOW, "Rvis":RvisPOW ,"Rll":RdilepPOW}
#genInfoAMC = {"Acceptance":{"ttjj":ttjjAcceptanceAMC,"ttbb":ttbbAcceptanceAMC }, "effciency":{ "ttjj":ttjjEffAMC,"ttbb":ttbbEffAMC  }, "eR":eRAMC, "acP":acPAMC, "Rfull": RfullAMC, "Rvis":RvisAMC  }
genInfoMG5 = {"Acceptance":{"ttjj":ttjjAcceptanceMG5,"ttbb":ttbbAcceptanceMG5 }, "effciency":{ "ttjj":ttjjEffMG5,"ttbb":ttbbEffMG5  }, "eR":eRMG5, "acP":acPMG5, "Rfull": RfullMG5, "Rvis":RvisMG5, "Rll":RdilepMG5  }

#print "FINAL2: POW eR= "+str(eRPOW)+"  , acceptance ttjj:"+str(ttjjAcceptancePOW)+", (effS6: "+str(ttjjEffPOW)+")  ,  ttbb:"+str(ttbbAcceptancePOW)+", (effS6: "+str(ttbbEffPOW)+")"
#print "FINAL2: AMC eR= "+str(eRAMC)+"  , acceptance ttjj:"+str(ttjjAcceptanceAMC)+", (effS6: "+str(ttjjEffAMC)+")  ,  ttbb:"+str(ttbbAcceptanceAMC)+", (effS6: "+str(ttbbEffAMC)+")"
#print "FINAL2: MG5 eR= "+str(eRMG5)+"  , acceptance ttjj:"+str(ttjjAcceptanceMG5)+", (effS6: "+str(ttjjEffMG5)+")  ,  ttbb:"+str(ttbbAcceptanceMG5)+", (effS6: "+str(ttbbEffMG5)+")"

##############################################################################
##############################################################################
##############################################################################
##############################################################################

import sys
if len(sys.argv) < 2:
  sys.exit()

arg1 = sys.argv[1] # default, freeB, freeC and, (freeB and freeC)
arg2 =  sys.argv[2] #

#if len(sys.argv) > 3:
#  arg3 = sys.argv[3]


Step="S6"

from math import *
histograms,freeTTB,freeTTCC,GEN=loadHistogram(arg1, "1",Step,"csvweight")
orig_r,orig_err,result=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)
kVal = result["kVal"]
#"""
SystematicUnc,SystematicUnck ={},{}
sumRerr, sumKerr = 0.,0.
#for i in range(1,212):
for i in range(1,101):
  if int(arg2) is 1:
    loadHistogramTTbarPOW(histograms,Step,"pdf_N"+str(i))
    orig_r2,bbb,resultPDF=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)
    sysUnc = (orig_r-orig_r2)/orig_r
    sysUnck = (kVal-resultPDF["kVal"])/kVal
    print "FINAL2: pdf_N"+str(i)+": R "+ str(round(sysUnc*10000)/100)+" %     ,     R = "+ str(round(orig_r2*10000)/10000)+" "
    print "FINAL2: pdf_N"+str(i)+": k "+str(round(sysUnck*10000)/100)+"      ,     k = "+ str(round(resultPDF["kVal"]*10000)/10000)+" "
    SystematicUnc[sys]=copy.deepcopy(sysUnc)
    SystematicUnck[sys]=copy.deepcopy(sysUnck)
#    sumRerr+=sysUnc*sysUnc
#    sumKerr+=sysUnck*sysUnck
    if fabs(sysUnc)>sumRerr : sumRerr=fabs(sysUnc)
    if fabs(sysUnck)>sumKerr : sumKerr=fabs(sysUnck)


#print "FINAL2: sumRerr : "+str(round(sqrt(sumRerr)*10000)/100)+" %"
#print "FINAL2: sumKerr : "+str(round(sqrt(sumKerr)*10000)/100)+" %"
print "FINAL2: sumRerr : "+str(round(sumRerr*10000)/100)+" %"
print "FINAL2: sumKerr : "+str(round(sumKerr*10000)/100)+" %"


#"""
SystematicUncQ2,SystematicUncQ2k ={},{}
sumRerrQ2, sumKerrQ2 = 0.,0.
for i in range(1,8):
  if int(arg2) is 1:
    loadHistogramTTbarPOW(histograms,Step,"Q2_N"+str(i))
    orig_r2,bbb,resultQ2=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)
    relpaceTTbarPOW(histograms,"up")
    orig_r3,bbb,resultQ22=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)
    relpaceTTbarPOW(histograms,"dw")
    orig_r4,bbb,resultQ23=fitting(histograms, freeTTB, freeTTCC, GEN,True,False)

    sysUnc = (orig_r-orig_r2)/orig_r
    sysUnck = (kVal-resultQ2["kVal"])/kVal
    print "FINAL2: Q2_N"+str(i)+": R "+ str(round(sysUnc*10000)/100)+" %     ,     R = "+ str(round(orig_r2*10000)/10000)+" "
    print "FINAL2: Q2_N"+str(i)+": k "+str(round(sysUnck*10000)/100)+"      ,     k = "+ str(round(resultQ2["kVal"]*10000)/10000)+" "

    sysUnc2 = (orig_r-orig_r3)/orig_r
    sysUnck2 = (kVal-resultQ22["kVal"])/kVal
    print "FINAL2: Q2_Nup"+str(i)+": R "+ str(round(sysUnc2*10000)/100)+" %     ,     R = "+ str(round(orig_r3*10000)/10000)+" "
    print "FINAL2: Q2_Nup"+str(i)+": k "+str(round(sysUnck2*10000)/100)+"      ,     k = "+ str(round(resultQ22["kVal"]*10000)/10000)+" "
 
    sysUnc3 = (orig_r-orig_r4)/orig_r
    sysUnck3 = (kVal-resultQ23["kVal"])/kVal
    print "FINAL2: Q2_Ndw"+str(i)+": R "+ str(round(sysUnc3*10000)/100)+" %     ,     R = "+ str(round(orig_r4*10000)/10000)+" "
    print "FINAL2: Q2_Ndw"+str(i)+": k "+str(round(sysUnck3*10000)/100)+"      ,     k = "+ str(round(resultQ23["kVal"]*10000)/10000)+" "

    SystematicUncQ2[sys]=copy.deepcopy(sysUnc)
    SystematicUncQ2k[sys]=copy.deepcopy(sysUnck)

    if fabs(sysUnc)>sumRerrQ2  : sumRerrQ2=fabs(sysUnc)
    if fabs(sysUnck)>sumKerrQ2 : sumKerrQ2=fabs(sysUnck)
    if fabs(sysUnc2)>sumRerrQ2  : sumRerrQ2=fabs(sysUnc2)
    if fabs(sysUnck2)>sumKerrQ2 : sumKerrQ2=fabs(sysUnck2)
    if fabs(sysUnc3)>sumRerrQ2  : sumRerrQ2=fabs(sysUnc3)
    if fabs(sysUnck3)>sumKerrQ2 : sumKerrQ2=fabs(sysUnck3)
 
print "FINAL2:Q2: sumRerr : "+str(round(sumRerrQ2*10000)/100)+" %"
print "FINAL2:Q2: sumKerr : "+str(round(sumKerrQ2*10000)/100)+" %"


