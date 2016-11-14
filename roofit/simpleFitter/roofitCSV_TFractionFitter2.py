#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

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



################
def fitting(histograms, freeTTB, freeTTCC):
  GEN='POW'
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
  n_all = n_ttbar+n_bkg+n_ddbkg

  print "FINAL2 : ttot / all  =  "+str(n_ttot/n_all )
  print "FINAL2 : bkg / all  =  "+str(n_bkg/n_all )
  print "FINAL2 : ddbkg / ttbar  =  "+str(n_ddbkg/n_all )

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
  #h1_data2.Add(h1_ttot,-0.8425)

  h1_ttb3 = h1_ttb.Clone("ttb3")
  h1_ttb3.Add(h1_tt2b)
  h1_ttb3.Add(h1_ttbb)
  
  h1_bkgAll3 = h1_bkg.Clone("BkgAll")
  h1_bkgAll3.Add(h1_ddbkg)

  h1_ttcclf3 = h1_ttcclf.Clone("ttcclf3")
  #h1_ttcclf1b2b3.Add(h1_ttb)
  #h1_ttcclf1b2b3.Add(h1_tt2b)

  mc = TObjArray(5)
  #mc.Add(h1_ttbb)
  mc.Add(h1_ttb3)
  mc.Add(h1_ttcclf3)
  ##mc.Add(h1_ttlf)
  mc.Add(h1_ttot)
  mc.Add(h1_bkg)
  mc.Add(h1_ddbkg)

  #FINAL2 : ttot / all  =  0.0741054146837
  #FINAL2 : bkg / all  =  0.0392637404208
  #FINAL2 : ddbkg / ttbar  =  0.00417416116344

  fit = TFractionFitter(h1_data2, mc)
  fit.Constrain(0,0.0001,0.4)
  #fit.Constrain(1,0.0001,0.4)
  fit.Constrain(1,0.7,0.999)
  #fit.Constrain(2,0.0765,0.0775)#0.07747)
  fit.Constrain(2,0.07410,0.074105)#0.07747)
  fit.Constrain(3,0.03926,0.039264)
  fit.Constrain(4,0.00417,0.004174)
  #fit.Constrain(5,0.0765,0.0775)
  #fit.SetRangeX(2,0.0,0.2)
  fit.SetRangeX(1,100)
  #fit.SetMC(parameter , );

  status = int(fit.Fit())
  print "status : "+str(status)
  ###############
  print "NDF:"+str(fit.GetNDF() )
  print "Chi^2:"+str(fit.GetChisquare())
  rrr,rrr_error=ROOT.Double(0),ROOT.Double(0)
  rr22,rr22_error=ROOT.Double(0),ROOT.Double(0)
  rr33,rr33_error=ROOT.Double(0),ROOT.Double(0)
  rr44,rr44_error=ROOT.Double(0),ROOT.Double(0)
  rr55,rr55_error=ROOT.Double(0),ROOT.Double(0)
  fit.GetResult(0,rrr,rrr_error)
  fit.GetResult(1,rr22,rr22_error)
  fit.GetResult(2,rr33,rr33_error)
  fit.GetResult(3,rr44,rr44_error)
  fit.GetResult(4,rr55,rr55_error)
  print "Rbb : "+str(rrr)+" +- "+str(rrr_error)
  print "Rlf : "+str(rr22)+" +- "+str(rr22_error)
  print "Rot : "+str(rr33)+" +- "+str(rr33_error)
  print "Rbkg : "+str(rr44)+" +- "+str(rr44_error)
  print "Rddbkg : "+str(rr55)+" +- "+str(rr55_error)

  cRAAA = TCanvas("RAAA", "AAA", 1)#500, 500)
  result = h1_bkg.Clone("result")
  result.Reset()
  result.Add(fit.GetPlot())
  result.SetLineColor(kRed)
  h1_data2.Draw("")
  result.Draw("same")
  #"""
  leg=make_legend(0.5,0.8,0.88,0.88)
  leg.AddEntry(result, "t#bar{t}jj + t#bar{t} others + Bkg ", "l")
  leg.AddEntry(h1_data2, "Data ", "ep")
  leg.Draw()
  #n_ttjj = n_ttbb+n_ttb+n_ttcc+n_ttlf+n_tt2b
  #n_ttbar = n_ttjj+n_ttot
  r_ttbb_ttb = n_ttbb/(n_ttbb+n_ttb+n_tt2b) 

  ffff = (rrr+rr22)
  rrrN=rrr/ffff #(rrr+rr22)
  leg2=addLegend2("(ttbj+ttbb)/ttjj : "+str(round(rrrN *10000)/10000)+" #pm "+str(round(rrr_error*ffff*100000)/100000),0.46,0.75)
  leg3=addLegend2("ttbb/ttjj : "+str(round(rrrN * r_ttbb_ttb*10000)/10000)+" #pm "+str(round(rrr_error*ffff*100000*r_ttbb_ttb)/100000),0.46,0.7)
  leg4=addLegend2("NDF : "+str(fit.GetNDF())+", #chi^2 : "+str(round(fit.GetChisquare()*10)/10),0.46,0.65)
  leg2.Draw()
  leg3.Draw()
  leg4.Draw()
  #"""
  cRAAA.Print("plots2/TFraction.pdf")
  cRAAA.Print("plots2/TFraction.png")

  return cRAAA,h1_data2,result,leg,leg2,leg3,leg4



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

freeTTB=False
freeTTCC=False
aaaa=fitting(histograms, freeTTB, freeTTCC)
    
