#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

import sys
sys.path.append('../ntuple2hist')


def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0),  leg.SetLineColor(1), leg.SetTextFont(62)
  #leg.SetTextSize(0.03)
  leg.SetTextSize(0.055)
  leg.SetBorderSize(1), leg.SetLineStyle(1), leg.SetLineWidth(1),  leg.SetLineColor(0)
  return leg

def make_legend2(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0),  leg.SetLineColor(1), leg.SetTextFont(62),  leg.SetTextSize(0.03)
  leg.SetBorderSize(1), leg.SetLineStyle(1), leg.SetLineWidth(1),  leg.SetLineColor(0)
  return leg

def addLegendCMS(text):#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"#it{"+text+"}")
  #title  = TLatex(-20.,50.,"#it{Simulation}")
  title.SetNDC(),        title.SetTextAlign(12),   title.SetX(0.20),      title.SetY(0.83)
  title.SetTextFont(42)#, title.SetTextSize(0.57),
  title.SetTextSizePixels(34)
  #title.SetTextFont(42), title.SetTextSize(0.1),  title.SetTextSizePixels(24)
  title.Draw()
  return title

def addLegendLumi():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"(13 TeV)")
  title.SetNDC(),        title.SetTextAlign(12)
  title.SetX(0.77),      title.SetY(0.94)
  title.SetTextSizePixels(34)
  #title.SetX(0.67),      title.SetY(0.93)
  title.SetTextFont(42)#, title.SetTextSize(0.059)#,  title.SetTextSizePixels(24)
  #title.SetTextFont(42), title.SetTextSize(0.1),  title.SetTextSizePixels(24)
  title.Draw()
  return title


def addLegendPreliminary():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"#bf{CMS} Preliminary")
  tex2.SetNDC(),          tex2.SetTextAlign(12)
  tex2.SetX(0.20),        tex2.SetY(0.94)
  #tex2.SetTextColor(2),
  tex2.SetTextSizePixels(34)
  tex2.SetTextFont(42) #,   tex2.SetTextSize(0.2), tex2.SetTextSizePixels(24)
  #tex2.SetTextColor(2),   tex2.SetTextFont(42),   tex2.SetTextSize(0.05), tex2.SetTextSizePixels(24)
  return tex2

def addTitle(ll):
  chtitle = TLatex(-20.,50.,ll)
  chtitle.SetNDC(),         chtitle.SetTextAlign(12),   chtitle.SetX(0.20),  chtitle.SetY(0.75)
  chtitle.SetTextFont(42) #,  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)
  chtitle.SetTextSizePixels(34)
  #chtitle.SetTextFont(42),  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)

  return chtitle


def myCanvas(name):
  c1 = TCanvas( name, '',1)#, 500, 500 )
  c1.SetTopMargin(0.09)
  return c1

def AddHist(channel,histograms):
  ls=["hMM","hEE","hME"]
  if channel=="MM":   ls = ["hMM"]
  if channel=="EE":   ls = ["hEE"]
  if channel=="ME":   ls = ["hME"]
  if channel=="MMEE": ls = ["hMM","hEE"]
  h={}
  if len(histograms["h1"].keys())>0 :
    for bb in ls: 
      if len(h.keys())==0:
        h["aa"]=copy.deepcopy(histograms["h1"][bb])
      else :
        h["aa"].Add(copy.deepcopy(histograms["h1"][bb]))
    return h["aa"]
  else : False

def makeSetTTjj(decay,histograms2):
  ttbb = AddHist(decay,histograms2["ttbb"])
  ttb = AddHist(decay,histograms2["ttb"])
  ttcc = AddHist(decay,histograms2["ttcc"])
  ttlf = AddHist(decay,histograms2["ttlf"])

  ttbb.Scale(1./ttbb.Integral() )
  ttb.Scale(1./ttb.Integral() )
  ttcc.Scale(1./ttcc.Integral() )
  ttlf.Scale(1./ttlf.Integral() )

  #isPrint =  (mon["name"] is "Stat")
  ttbb.SetLineWidth(2);
  ttb.SetLineWidth(2);
  ttcc.SetLineWidth(2);
  ttlf.SetLineWidth(2);

  ttbb.SetLineColor(kRed);
  ttb.SetLineColor(kOrange+3);
  ttcc.SetLineColor(kGreen);
  ttlf.SetLineColor(kBlue);
  ttbb.SetFillColor(0);
  ttb.SetFillColor(0);
  ttcc.SetFillColor(0);
  ttlf.SetFillColor(0);

  return ttbb,ttb,ttcc,ttlf

######################################
######################################
######################################
def aCanvas(mon,step,decay,isLogy,Syss,SFbyFitting):
  from makeMCHistSet import makeMCHistSet,load1stHistograms
  histograms=load1stHistograms(mon,step,"csvweight",SFbyFitting)
  histograms2,plotSet=makeMCHistSet(histograms)

  histogramsUp=load1stHistograms(mon,step,Syss[0]+"_Up",SFbyFitting)
  histogramsUp2,plotSet=makeMCHistSet(histogramsUp)

  histogramsDw=load1stHistograms(mon,step,Syss[0]+"_Down",SFbyFitting)
  histogramsDw2,plotSet=makeMCHistSet(histogramsDw)


  step2="_S"+str(int(step[1])-1)
  canvasname=mon["name"]+step2+"_"+Syss[0]
  c1 = myCanvas(canvasname)#, myPad1(canvasname+"pad1"), myPad2(canvasname+"pad2")
  ttbb,ttb,ttcc,ttlf=makeSetTTjj(decay,histograms2)
  ttbbUp,ttbUp,ttccUp,ttlfUp=makeSetTTjj(decay,histogramsUp2)
  ttbbDw,ttbDw,ttccDw,ttlfDw=makeSetTTjj(decay,histogramsDw2)
  ttbbUp.SetLineStyle(2),ttbUp.SetLineStyle(2),ttccUp.SetLineStyle(2),ttlfUp.SetLineStyle(2)
  ttbbDw.SetLineStyle(3),ttbDw.SetLineStyle(3),ttccDw.SetLineStyle(3),ttlfDw.SetLineStyle(3)
  #ttb.SetLineStyle(2);
  #ttcc.SetLineStyle(3);
  #ttlf.SetLineStyle(4);

  ttbb.SetMaximum(ttbb.GetMaximum()*1.5)
  if ttbb.GetMaximum()<ttlf.GetMaximum()*1.5 :
    ttbb.SetMaximum(ttlf.GetMaximum()*1.5)
  #ttbb.SetMinimum(ttbb.GetMinimum()*0.5)
  ttbb.GetXaxis().SetTitle("")


  ########################
  ########################
  if mon["Xtitle"] is not None :
    ttbb.GetXaxis().SetTitle(mon["Xtitle"])
    ttbb.GetYaxis().SetTitle("Normalized entries")

  #debug
  ttbb.GetYaxis().SetTitleOffset(0.8)
  ttbb.GetYaxis().SetTitleSize(0.075)
  ttbb.GetXaxis().SetTitleOffset(0.8)
  ttbb.GetXaxis().SetTitleSize(0.075)

  ttbb.Draw("HIST"),ttbbUp.Draw("sameHIST"),ttbbDw.Draw("sameHIST")
  ttb.Draw("sameHIST"),ttbUp.Draw("sameHIST"),ttbDw.Draw("sameHIST")
  ttcc.Draw("sameHIST"),ttccUp.Draw("sameHIST"),ttccDw.Draw("sameHIST")
  ttlf.Draw("sameHIST"),ttlfUp.Draw("sameHIST"),ttlfDw.Draw("sameHIST"),

  title=""
  if mon["Title"] is not None : 
    title = mon["Title"]

  pt,pt2,pt3,pt4 = addLegendCMS(Syss[1]),addLegendPreliminary(),addTitle(title),addLegendLumi()
  pt.Draw(),  pt2.Draw(),  pt3.Draw(), pt4.Draw()

  wid=0.23
  legx1 = 0.65

  leg  = make_legend(legx1,0.60, legx1+wid*0.9,0.86)
  plotSet2= {'ttbars': ['ttbb',  'ttb', "ttcc","ttlf"]}
 
  for aa in plotSet2["ttbars"]:
    if len(histograms2[aa]["h1"].keys())>0:
      entry=leg.AddEntry(eval(aa), histograms2[aa]["label"], "l")
      entry.SetLineColor(1),    entry.SetLineStyle(1)
      entry.SetLineWidth(1),    entry.SetMarkerColor(1)
      entry.SetMarkerStyle(21), entry.SetMarkerSize(1)
      entry.SetTextFont(62)
  leg.Draw()
  c1.Print("plots_fit/TH1_Sys_"+canvasname+".eps")
  c1.Print("plots_fit/TH1_Sys_"+canvasname+".C")
 
  c1set = [c1,histograms2,ttbb,ttb,ttcc,ttlf,pt,pt2,pt3,leg]
  return c1set,plotSet#,Stats,plotSet


##################################
##################################
##################################
def main():#step, moni):
  import sys
  if len(sys.argv) < 3:
    print "usage : python -i makeCanvas.py S2 I sys des"
    from monitors_cfi import monitors
    for i in range(0,len(monitors)):
      print "I= "+str(i)+" : "+monitors[i]["name"]
    sys.exit()

  step = sys.argv[1]      # 
  Sys = sys.argv[3]      # 
  des = Sys
  if len(sys.argv) > 3:
    des = sys.argv[4]      # 
  Syss=[Sys,des]
  st=step.replace("S","")
  runStat=False
  if int(st)==0 : runStat=True

  moni = int(sys.argv[2]) #
  print ""+step+" moni:"+str(moni)
 
  gROOT.SetStyle("Plain")
  gStyle.SetOptFit(1000),    gStyle.SetOptStat("emruo")
  gStyle.SetOptStat(kFALSE)
  gStyle.SetPadTickY(1),     gStyle.SetPadTickX(1)
  
  gROOT.ProcessLine(".L tdrStyle.C")
  setTDRStyle()

  from monitors_cfi import monitors
  aaa = {}
  StatsAll = {}
  #['Stat', 'nGoodPV', 'MET', 'ZMass',            # 0-3
  # 'nBJet30L', 'nBJet30M', 'NJet30', 'nBJet30T', # 4-7
  # 'lep1Pt', 'lep2Pt', 'lep1Eta', 'lep2Eta',     # 8-11
  # 'lep1Phi', 'lep2Phi', 'lep1Iso', 'lep2Iso'    #12-15
  # 'jet1Pt', 'jet2Pt', 'jet3Pt', 'jet4Pt',       #16-19
  # 'jet1Eta', 'jet2Eta', 'jet3Eta', 'jet4Eta',   #20-23
  # 'jet1Phi', 'jet2Phi', 'jet3Phi', 'jet4Phi',   #24-27
  # 'jet1CSV', 'jet2CSV', 'jet3CSV', 'jet4CSV']   #28-31
  ####SFbyFitting={'ttbbSF':1.64035858441,'ttcclfSF':0.915145850803,'k':0.82474951077}
  #SFbyFitting={'ttbbSF':1.62796470428,'ttcclfSF':0.916707908424,'k':0.842498214663}

  SFbyFitting={'ttbbSF':1.0,'ttcclfSF':1.0,'k':1.0}
  mon = monitors[moni]

  if moni ==30 or moni==31 : 
    mon["Xtitle"] = "b jet discriminator"
    mon["Ytitle"] = "Jets / 0.1 units"
  if moni == 30 :  mon["Title"] = "Third jet"
  if moni == 31 :  mon["Title"] = "Fouth jet"

  if moni ==5 : 
    mon["Xtitle"] = "Number of b-tagged jets"
    mon["Ytitle"] = "Events"
    mon["Title"] = ""
 
  isLogy=False
  #step="S2"
  #weight="CEN"#csvweight"
  #aaa[1]=aCanvas(mon,step,"MM",isLogy,weight,SFbyFitting)
  #aaa[2]=aCanvas(mon,step,"EE",isLogy,weight,SFbyFitting)
  #aaa[3]=aCanvas(mon,step,"ME",isLogy,weight,SFbyFitting)
  aaa[4]=aCanvas(mon,step,"LL",isLogy,Syss,SFbyFitting)
    
  return aaa


if __name__ == "__main__":
  test=main()


