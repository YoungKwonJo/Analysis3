#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy
from math import *


lumi = 2318.278305882

################
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
  #tex2.SetTextSizePixels(24)

  return tex2

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("em")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("mm")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("ee")>-1 : ll2="e^{#mp}e^{#pm} channel"

  chtitle = TLatex(-20.,40.,ll2)
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

################
def getIntegralAll(h2):
  aaa=h2.Integral()
  aaa+=h2.GetBinContent(0,0)
  for i in range(1,11):
    aaa+=h2.GetBinContent(i,0)
  return aaa


############################################################################################
############################################################################################
def fitting(histograms, freeTTB, freeTTCC):
  GEN="POW"
  res = {}
  n_ttbb = histograms[GEN+"ttbb"]["exp"]
  n_ttb  = histograms[GEN+"ttb"]["exp"]
  n_tt2b  = histograms[GEN+"tt2b"]["exp"]
  #n_tt2b = histograms[GEN+"tt2b"]["exp"]
  n_ttcc = histograms[GEN+"ttcc"]["exp"]
  #n_ttc = histograms[GEN+"ttc"]["exp"]
  n_ttlf = histograms[GEN+"ttlf"]["exp"]
  n_ttcclf = histograms[GEN+"ttcclf"]["exp"]
  n_ttot = histograms[GEN+"ttot"]["exp"]
  n_bkg = histograms["bkg"]["exp"]
  n_ddbkg = histograms["ddbkg"]["exp"]
  n_data = histograms["DATA"]["exp"]

  n2_ttbb  = copy.deepcopy( getIntegralAll(histograms[GEN+"ttbb"]["h1"]) )
  n2_ttb   = copy.deepcopy( getIntegralAll(histograms[GEN+"ttb"]["h1"]) )
  n2_tt2b  = copy.deepcopy( getIntegralAll(histograms[GEN+"tt2b"]["h1"]) )
  n2_ttcc  = copy.deepcopy( getIntegralAll(histograms[GEN+"ttcc"]["h1"]) )
  n2_ttlf  = copy.deepcopy( getIntegralAll(histograms[GEN+"ttlf"]["h1"]) )
  n2_ttjj  = copy.deepcopy( n2_ttbb+n2_ttb+n2_tt2b+n2_ttcc+n2_ttlf )
  n2_ttot  = copy.deepcopy( getIntegralAll(histograms[GEN+"ttot"]["h1"]) )
  n2_bkg   = copy.deepcopy( getIntegralAll(histograms["bkg"]["h1"]) )
  n2_ddbkg = copy.deepcopy( getIntegralAll(histograms["ddbkg"]["h1"]) )
  n2_data  = copy.deepcopy( getIntegralAll(histograms["DATA"]["h1"]) )

  n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  n_ttbar = n_ttjj+n_ttot
  llratio_ = n_ttjj/n_ttbar

  print  "FINAL2 : ttbb r:"+str( (n_ttbb/n2_ttbb) )
  print  "FINAL2 : ttjj r:"+str( (n_ttjj/n2_ttjj) )
  print  "FINAL2 : ttot r:"+str( (n_ttot/n2_ttot) )
  print  "FINAL2 : data r:"+str( (n_data/n2_data) )

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

  ttjjCXFS=n_ttjj/(lumi*ttjjEff*ttjjAcc) 
  ttbbCXFS=n_ttbb/(lumi*ttbbEff*ttbbAcc) 
  ttjjCXVS=n_ttjj/(lumi*ttjjEff) 
  ttbbCXVS=n_ttbb/(lumi*ttbbEff)

  fsrttbb_ = rttbb/(ttbbEff*ttbbAcc/ttjjEff/ttjjAcc)
 
  fsrttbb = RooRealVar("fsrttbb","fsrttbb",fsrttbb_,fsrttbb_*0.5,fsrttbb_*2.5)
  print "aaaaaaaaaaaaaaaaaaaaaaaaaa"
  print "FINAL2 ttjjCXFS : "+str(ttjjCXFS)
  print "aaaaaaaaaaaaaaaaaaaaaaaaaa"

  precxttjjVS=5.1   #VS
  precxttbbVS=0.070 #VS
  precxttjjFS=257.  #FS
  #precxttjjFS=ttjjCXFS*1000.
  precxttbbFS=3.2   #FS
  #precxttbbFS=ttbbCXFS*1000. #FS
  ttjj_ttbarratio_ = 0.307036#*0.8425

  accttbb   = RooRealVar(       "accttbb","normalization factor",           ttbbAcc, ttbbAcc, ttbbAcc) 
  accttjj   = RooRealVar(       "accttjj","normalization factor",           ttjjAcc, ttjjAcc, ttjjAcc)

  ttjj_ttbarratio   = RooRealVar( "ttjjttbarratio","normalization factor", ttjj_ttbarratio_,ttjj_ttbarratio_,ttjj_ttbarratio_)
  #ttjj_ttbarratio   = RooRealVar( "ttjjttbarratio","normalization factor", 0.307036, 0.307036, 0.307036)
  #ttjj_ttbarratio   = RooRealVar( "ttjjttbarratio","normalization factor", ttjj_ttbarratio_,ttjj_ttbarratio_,ttjj_ttbarratio_)

  effttbb   = RooRealVar(       "effttbb","normalization factor",  ttbbEff, ttbbEff, ttbbEff) 
  effttjj   = RooRealVar(       "effttjj","normalization factor",  ttjjEff, ttjjEff, ttjjEff) 

  RttbbReco=RooRealVar("RttbbReco","RttbbReco",rttbb,rttbb,rttbb);
  RttbReco =RooRealVar("RttbReco", "RttbReco", rttb, rttb, rttb);
  Rtt2bReco=RooRealVar("Rtt2bReco","Rtt2bReco",rtt2b,rtt2b,rtt2b);
  RttccReco=RooRealVar("RttccReco","RttccReco",rttcc,rttcc,rttcc);

  cxttjj     = RooRealVar(       "cxttjj","normalization factor",   precxttjjFS, precxttjjFS*0.35, precxttjjFS*1.4)
  #cxttjjVS     = RooRealVar(    "cxttjjVS","normalization factor",  precxttjjVS, precxttjjVS*0.3, precxttjjVS*1.5)

  ############################################################################################################################
  ############################################################################################################################
  ############################################################################################################################
  k      = RooFormulaVar("k","number of ttjj events after fitting","@0/@1",  RooArgList(cxttjj,ttjj_ttbarratio) )
  fsig   = RooFormulaVar("fsig",          "fsig",         "@0*@1*@2/@3/@4",  RooArgList(fsrttbb,effttbb,accttbb,effttjj,accttjj) )

  fsig2con  =RooFormulaVar("fsig2con",          "fsig2","@0/@1*@2",RooArgList(fsig,RttbbReco,RttbReco) )  # constraint fsig2 with fsig
  fsig3con  =RooFormulaVar("fsig3con",          "fsig3","@0/@1*@2",RooArgList(fsig,RttbbReco,Rtt2bReco) )  # constraint fsig3 with fsig

  ############################################################################################################################
  nttjj   =RooRealVar(    "nttjj","number of ttjj events",                            n_ttjj , n_ttjj, n_ttjj)
  knttjj  =RooFormulaVar("knttjj","number of ttjj events after fitting","k*nttjj",    RooArgList(k,nttjj) )
  nttot   =RooRealVar(    "nttot","number of ttot events",                            n_ttot , n_ttot, n_ttot)
  knttot  =RooFormulaVar("knttot","number of ttot events after fitting","k*nttot",    RooArgList(k,nttot) )
  nbkg    =RooRealVar(     "nbkg","number of background events",                      n_bkg , n_bkg, n_bkg)
  nddbkg  =RooRealVar(   "nddbkg","number of background events",                    n_ddbkg , n_ddbkg, n_ddbkg)
  
  ######
  nttcc =RooRealVar(   "nttcc","number of ttcc events",                         n_ttcc , n_ttcc, n_ttcc)
  knttcc=RooFormulaVar("knttcc","number of ttcc events after fitting","k*nttcc",RooArgList(k,nttcc) )
  #####
 
  #histogram
  xyArg = RooArgList(x, y)
  data    = RooDataHist("data",    "data set with (x)",   xyArg, histograms["DATA"]["h1"])

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

  ##########################################################################################
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
  RFrame = fsrttbb.frame()
  nll.plotOn(RFrame,RooFit.ShiftToZero()) 
  RFrame.SetMaximum(4.);RFrame.SetMinimum(0)
  RFrame.GetXaxis().SetTitle("R_{FS} ")
  RFrame.SetTitle("")
  RFrame.Draw()

  boxR = TBox(fsrttbb_-0.001/2.,0,fsrttbb_+0.001/2.,4.)
  ci = TColor.GetColor("#d0efd0")
  boxR.SetFillColor(ci)
  boxR.Draw()

  line = TLine(RFrame.GetXaxis().GetXmin() ,0.5,RFrame.GetXaxis().GetXmax(),0.5)
  line.SetLineColor(kRed)
  line.Draw()
  
  lineTbb = TLine(fsrttbb_,RFrame.GetMaximum(),fsrttbb_,0)
  lineTbb.SetLineStyle(2)
  lineTbb.Draw()

  l1 = make_legend(0.39,0.76,0.93,0.88)
  l1.AddEntry(lineTbb,"prefit: R_{FS} = "+str(roudV(fsrttbb_)),"l")
  l1.AddEntry(lineKKK,"fit: R_{FS} = "+str(roudV(fsrttbb.getVal()))+" #pm "+str(roudV(fsrttbb.getError() ))+"","l")

  l1.SetTextSize(0.04)
  l1.SetFillColor(0)
  l1.SetLineColor(0)
  l1.Draw()

  cenTtbbCX= fsrttbb.getVal()*cxttjj.getVal()
  errTtbbCX=sqrt( fsrttbb.getError()/fsrttbb.getVal()*fsrttbb.getError()/fsrttbb.getVal() + cxttjj.getError()/cxttjj.getVal()*cxttjj.getError()/cxttjj.getVal() )*cenTtbbCX

  cR10.cd(1).Update()

  ##########################################################################################
  ##########################################################################################
  cR10.cd(1)
  nllK = model2.createNLL(data)
  RFrameK = cxttjj.frame()
  nllK.plotOn(RFrameK,RooFit.ShiftToZero())

  RFrameK.SetMaximum(4.);RFrameK.SetMinimum(0)
  RFrameK.GetXaxis().SetTitle("#sigma_{FS}^{t#bar{t}jj}")
  RFrameK.SetTitle("")
  RFrameK.Draw()
  print "RFameK: "+str(type(RFrameK))

  box = TBox(precxttjjFS-5./2.,0,precxttjjFS+5./2.,4.)
  #ci = TColor.GetColor("#d0efd0")
  box.SetFillColor(ci)
  box.Draw() 

  lineTbbK = TLine(precxttjjFS,RFrameK.GetMaximum(),precxttjjFS,0)
  lineTbbK.SetLineStyle(2)
  lineTbbK.Draw()
  
  
  l1K = make_legend(0.49,0.76,0.93,0.88)
  l1K.AddEntry(lineTbbK,"prefit: #sigma_{FS}^{t#bar{t}jj} = "+str(roudV(precxttjjFS)),"l")
  l1K.AddEntry(lineKKK,"fit: #sigma_{FS}^{t#bar{t}jj} = "+str(roudV(cxttjj.getVal()))+" #pm "+str(roudV(cxttjj.getError() ))+"","l")

  l1K.SetTextSize(0.04)
  l1K.SetFillColor(0)
  l1K.SetLineColor(0)
  l1K.Draw()
 
  pt.Draw()
  #pt2.Draw()
  pt3.Draw()

  ptBB  = addLegend2("prefit: #sigma_{FS}^{t#bar{t}bb} = "+str(roudV(precxttbbFS)),0.55,0.68)
  ptBB2 = addLegend2("fit: #sigma_{FS}^{t#bar{t}bb} = "+str(roudV(cenTtbbCX))+" #pm "+str(round( errTtbbCX*1000. )/1000. ),0.55,0.62)
  ptBB2.Draw()
  ptBB.Draw()

  lineK = TLine(RFrameK.GetXaxis().GetXmin() ,0.5,RFrameK.GetXaxis().GetXmax(),0.5)
  lineK.SetLineColor(kRed)
  lineK.Draw()

  cR10.cd(2).Update()
  cR10.Print("plots2/"+GEN+"_FS.eps")
  cR10.Print("plots2/"+GEN+"_FS.png")

  print "FINAL2 : "+str( (cxttjj.getVal())/precxttjjFS)
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


##############################################################################
##############################################################################
##############################################################################

f = TFile.Open("ttbb_top-16-010.root")
sam1=["POWttbb","POWttb","POWtt2b","POWttcc","POWttlf","POWttot"]
sam2=["bkg","ddbkg"]
sam3=["DATA"]
histograms={}
for i in sam1:
  print "h2_"+i+"_S6LL_csvweight"
  h1= f.Get("h2_"+i+"_S6LL_csvweight").Clone(i)
  h1.Scale(1./831.76)
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
cR10 = fitting(histograms, freeTTB, freeTTCC)
###################

