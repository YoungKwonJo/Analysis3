#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

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


def newTemplateGausian(h1):
  test_h1 = h1.Clone(h1.GetName()+"_test")
  test_h1.Reset()
  for x in range(1, 11):
    for y in range(1, 11):
      newXY = gRandom.Gaus(h1.GetBinContent(x,y), h1.GetBinError(x,y))
      test_h1.SetBinContent(x,y,newXY)
      test_h1.SetBinError(x,y,h1.GetBinError(x,y))
  return test_h1


def fitting(histograms, freeTTB, freeTTCC):
  res = {}
  GEN="POW"

  h1_data  = histograms["DATA"]["h1"]
  h1_ttbb  = newTemplateGausian(histograms[GEN+"ttbb"]["h1"])
  h1_ttb   = newTemplateGausian(histograms[GEN+"ttb"]["h1"])
  h1_tt2b  = newTemplateGausian(histograms[GEN+"tt2b"]["h1"])
  h1_ttcc  = newTemplateGausian(histograms[GEN+"ttcc"]["h1"])
  h1_ttcclf= newTemplateGausian(histograms[GEN+"ttcclf"]["h1"])
  h1_ttlf  = newTemplateGausian(histograms[GEN+"ttlf"]["h1"])
  h1_ttot  = newTemplateGausian(histograms[GEN+"ttot"]["h1"])
  h1_bkg   = newTemplateGausian(histograms["bkg"]["h1"])
  h1_ddbkg = newTemplateGausian(histograms["ddbkg"]["h1"])

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
  """ 

  n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  n_ttbar = n_ttjj+n_ttot

  luminosity_data = 2318.278305882
  ttbarCX = 831.76 
  luminosity_eff= n_ttbar/ttbarCX
  scale = luminosity_data / luminosity_eff

  print "scale: "+str(scale)


  """
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
  """
  
  if n_ttjj==0:  return False,False,False
  
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
  fsig3con  =RooFormulaVar("fsig3con",          "fsig3","@0/@1*@2",RooArgList(fsig,RttbbReco,Rtt2bReco) )  # constraint fsig3 with fsig
  fsig2  =RooRealVar(   "fsig2",                "fsig2",          rttb, 0.0, 0.3)  # free fsig2
  fsig3  =RooRealVar(   "fsig3",                "fsig3",          rtt2b, 0.0, 0.3)  # free fsig3
  fsig32con  =RooFormulaVar(   "fsig32con",    "fsig32con", "@0/@1*@2",RooArgList(fsig2,RttbReco,Rtt2bReco))  # free fsig32 with fsig2
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


  recoR      = fsig.getVal()
  recoRerror = fsig.getError()
  kVal      = k.getVal()
  kValerror = k.getError()
 

 #############################3
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

  cRho = TCanvas("cRho00", "Rvsk", 1)#500, 500)
  nll_ratio = model2.createNLL(data)
  roominimizer=RooMinimizer(nll_ratio)
  roominimizer.migrad()
  roominimizer.hesse()
  rsav = RooFitResult(roominimizer.save())
  rsav.correlationHist().Draw("coltext")
  cRho.Print("plots/correlation_KvsR.eps")
  cRho.Print("plots/correlation_KvsR.png")
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
  
  


f = TFile.Open("ttbb_top-16-010.root")
sam1=["POWttbb","POWttb","POWtt2b","POWttcc","POWttlf","POWttot"]
sam2=["bkg","ddbkg"]
sam3=["DATA"]
histograms={}
for i in sam1:
  print "h2_"+i+"_S6LL_csvweight"
  h1= f.Get("h2_"+i+"_S6LL_csvweight").Clone(i)
  histograms[i]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}
httcclf=histograms['POWttcc']['h1'].Clone("POWttcclf")
httcclf.Add(histograms['POWttlf']['h1'] )
histograms['POWttcclf']={"h1":copy.deepcopy(httcclf),"exp":httcclf.Integral()}

for i in sam2:
  h1=f.Get(i+"hist").Clone(i)
  histograms[i]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}
for i in sam3:
  h1=f.Get("h2_"+i+"_S6LL_CEN").Clone(i)
  histograms[i]={"h1":copy.deepcopy(h1),"exp":h1.Integral()}
f.Close()

#ttbarCX = 831.76 
#print histograms['POWttot']['exp']/ttbarCX


freeTTB=False
freeTTCC=False
fitting(histograms, freeTTB, freeTTCC)
   
