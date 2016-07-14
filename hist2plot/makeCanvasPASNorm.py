#! /usr/bin/env python

#from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT,TGraphErrors
#from ROOT import RooRealVar,RooFormulaVar,RooDataHist,RooHistPdf,RooAddPdf,RooArgList,RooFit,RooMinuit,RooAbsData
import ROOT
from ROOT import *
from array import array
import copy

import sys
sys.path.append('../ntuple2hist')

###################################################
###################################################
###################################################
###################################################
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

def addLegendCMS():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"#it{Simulation}")
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

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("ME")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("MM")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("EE")>-1 : ll2="e^{#mp}e^{#pm} channel"
  chtitle = TLatex(-20.,50.,ll2)
  chtitle.SetNDC(),         chtitle.SetTextAlign(12)
  #chtitle.SetX(0.20),  chtitle.SetY(0.75)
  chtitle.SetX(0.20),  chtitle.SetY(0.66)
  chtitle.SetTextFont(42) #,  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)
  chtitle.SetTextSizePixels(34)
  #chtitle.SetTextFont(42),  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)

  return chtitle

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
def myPad1(name):
  pad1 = TPad(name, "",0,0.3,1,1)
  pad1.SetPad(0.01, 0.23, 0.99, 0.99), pad1.SetTopMargin(0.1), pad1.SetRightMargin(0.04)
  return pad1
def myPad2(name):
  pad2 = TPad(name, "",0,0,1,0.3)
  pad2.SetPad(0.01, 0.02, 0.99, 0.3),  gStyle.SetGridWidth(1),  gStyle.SetGridColor(14)
  pad2.SetGridx(),  pad2.SetGridy(),   pad2.SetTopMargin(0.05)
  pad2.SetBottomMargin(0.4),           pad2.SetRightMargin(0.04)
  return pad2

##################################################
##################################################
def StyleUp(histograms):
  for aa in histograms.keys():
    for bb in [0,1,2]:
      #print str(aa)+":"+str(histograms[aa]["h1"].keys())
      if len(histograms[aa]["h1"].keys())>0 :
        cc=histograms[aa]["h1"]["hMM"]
        if bb==1 : cc=histograms[aa]["h1"]["hEE"]
        if bb==2 : cc=histograms[aa]["h1"]["hME"] 
        if "LineColor"   in histograms[aa].keys(): cc.SetLineColor( TColor.GetColor(histograms[aa]["LineColor"])  )
        if "LineStyle"   in histograms[aa].keys(): cc.SetLineStyle(  histograms[aa]["LineStyle"]   )
        if "FillStyle"   in histograms[aa].keys(): cc.SetFillStyle(  histograms[aa]["FillStyle"]   )
        if "MarkerStyle" in histograms[aa].keys(): cc.SetMarkerStyle(histograms[aa]["MarkerStyle"] )
        if "MarkerSize"  in histograms[aa].keys(): cc.SetMarkerSize( histograms[aa]["MarkerSize"]  )
        if "FillColor"   in histograms[aa].keys(): cc.SetFillColor(  TColor.GetColor(histograms[aa]["FillColor"]) )
def copyStyleUp(hist, hist2):
  hist.SetLineColor(   hist2.GetLineColor()  )
  hist.SetLineStyle(   hist2.GetLineStyle()  )
  hist.SetFillStyle(   hist2.GetFillStyle()  )
  hist.SetMarkerStyle( hist2.GetMarkerStyle())
  hist.SetMarkerSize(  hist2.GetMarkerSize() )
  hist.SetFillColor(   hist2.GetFillColor()  )

def myDataHistStyleUp(hdata):
  hdata.GetYaxis().SetTitle("Events")
  #hdata.GetYaxis().SetTitleOffset(1.2)
  #hdata.GetYaxis().SetTitleSize(0.07)
  #debug
  hdata.GetYaxis().SetTitleOffset(0.8)
  hdata.GetYaxis().SetTitleSize(0.075)
  #hdata.GetYaxis().SetLabelSize(0.065)
  #hdata.GetYaxis().SetNdivisions(607)

  hdata.GetYaxis().SetLabelSize(0.060)
  #hdata.GetYaxis().SetLabelSize(0.055)
  hdata.GetYaxis().SetNdivisions(607)

  #hdata.GetYaxis().SetLabelSize(0.05)
  #hYaxis = hdata.GetYaxis()
  #hYaxis.SetMaxDigits(3)
  hdata.GetXaxis().SetLabelSize(0.0)
  #hdata.GetXaxis().SetTitle("")

  hdata.SetMarkerStyle(20)
  #hdata.SetMarkerSize(0.7)
  hdata.SetMarkerSize(1.0)

def myHist2TGraphError(hist1):
  xx,xxer,yy,yyer=[],[],[],[]
  for i in range(0, hist1.GetNbinsX()+2 ):
    yy.append(  float(hist1.GetBinContent(i)))
    yyer.append(float(hist1.GetBinError(i)))
    xx.append(  float(hist1.GetBinCenter(i)))
    xxer.append(float(hist1.GetBinWidth(i)/2))
  x,xer,y,yer   = array("d",xx), array("d",xxer), array("d",yy), array("d",yyer)
  gr = TGraphErrors(len(x), x,y,xer,yer)
  gr.SetFillStyle(1001)
  gr.SetFillColor( hist1.GetLineColor() )
  gr.SetLineColor( hist1.GetFillColor() )

  return gr

def styleBottomUp(hdata):
  hdata.SetMarkerStyle(20)
  #hdata.SetMarkerSize(0.5)
  hdata.SetMarkerSize(1.0)
  hdata.SetMarkerColor(1)
  hdata.SetLineColor(1)
  hdata.SetLineWidth(1)
  hdata.SetMaximum(2)
  hdata.SetMinimum(0)
  hdata.SetTitle("")
  
  hdata.GetYaxis().SetTitle("Obs/Exp")
  #hdata.GetYaxis().CenterTitle()
  #hdata.GetYaxis().SetTitleOffset(0.45)
  #hdata.GetXaxis().SetTitleOffset(1.1)

  hdata.GetYaxis().SetNdivisions(402)
  hdata.GetXaxis().SetNdivisions(509)
  #hdata.GetYaxis().SetLabelSize(0.15)
  #hdata.GetYaxis().SetLabelSize(0.20)
  #hdata.GetXaxis().SetLabelSize(0.20)
  hdata.GetYaxis().SetLabelSize(0.15)
  hdata.GetXaxis().SetLabelSize(0.15)


  #hdata.GetYaxis().SetTitleSize(0.16)
  #hdata.GetXaxis().SetTitleSize(0.16)

  #debug
  #hdata.GetYaxis().SetLabelSize(0.19)
  #hdata.GetXaxis().SetLabelSize(0.19)

  #hdata.GetYaxis().SetTitleOffset(0.35)
  #hdata.GetXaxis().SetTitleOffset(0.85)
  hdata.GetYaxis().SetTitleOffset(0.27)
  hdata.GetXaxis().SetTitleOffset(0.85)

  hdata.GetYaxis().SetTitleSize(0.21)
  hdata.GetXaxis().SetTitleSize(0.21)
  
  hdata.SetMinimum(0.6)
  hdata.SetMaximum(1.4)

def myRatioSyst(hdata):
  RatioSyst = hdata.Clone("ratioSyst")

  for b_r in range(1,RatioSyst.GetNbinsX()+1):
    RatioSyst.SetBinContent(b_r,1.0)

  thegraphRatioSyst = TGraphErrors(RatioSyst)
  thegraphRatioSyst.SetFillStyle( 1001 )
  thegraphRatioSyst.SetLineColor( hdata.GetLineColor() )
  thegraphRatioSyst.SetFillColor( TColor.GetColor("#cccccc") )
  thegraphRatioSyst.SetName("thegraphRatioSyst")

  return thegraphRatioSyst



##############################
##############################
##############################
##############################
##############################
def StackHist(channel, histograms2, plotSet,isPrint):
  hs = THStack("hs","")
  ls=["hMM","hEE","hME"]
  if channel=="MM":   ls = ["hMM"]
  if channel=="EE":   ls = ["hEE"]
  if channel=="ME":   ls = ["hME"]
  if channel=="MMEE": ls = ["hMM","hEE"]
  Stats = {}
  for aa in plotSet["mg5"]:
    h={}
    if len(histograms2[aa]["h1"].keys())>0 :
      for bb in ls: 
        if len(h.keys())==0:
          h[aa]=copy.deepcopy(histograms2[aa]["h1"][bb])
        else :
          h[aa].Add(copy.deepcopy(histograms2[aa]["h1"][bb]))
      if isPrint : 
        aaa=""
        if h[aa].GetBinContent(1)==0.   : aaa= " 0 " 
        elif h[aa].GetBinContent(1)<100 : aaa= " "+str(round(h[aa].GetBinContent(1)*10)/10)+" $\pm$ "+str(round(h[aa].GetBinError(1)*10)/10)+" "
        else                            : aaa= " "+str(int(round(h[aa].GetBinContent(1))))+" $\pm$ "+str(int(round(h[aa].GetBinError(1))))+" "
        Stats[aa]=aaa

  for aa in plotSet["ttbars"]:
    h={}
    if len(histograms2[aa]["h1"].keys())>0 :
      for bb in ls: 
        if len(h.keys())==0:
          h[aa]=copy.deepcopy(histograms2[aa]["h1"][bb])
        else :
          h[aa].Add(copy.deepcopy(histograms2[aa]["h1"][bb]))
      if isPrint : 
        aaa=""
        if h[aa].GetBinContent(1)==0.   : aaa= " 0 " 
        elif h[aa].GetBinContent(1)<100 : aaa= " "+str(round(h[aa].GetBinContent(1)*10)/10)+" $\pm$ "+str(round(h[aa].GetBinError(1)*10)/10)+" "
        else                            : aaa= " "+str(int(round(h[aa].GetBinContent(1))))+" $\pm$ "+str(int(round(h[aa].GetBinError(1))))+" "
        Stats[aa]=aaa
      
      h[aa].SetFillColor( TColor.GetColor(histograms2[aa]["FillColor"]) )
      #hs.Add(copy.deepcopy(h[aa]))
      hs.Add(h[aa])

      if aa.find("ttbb")>-1:
        #print "histograms2.keys(): "+str(histograms2.keys())
        aaaa=histograms2["ttV"]["h1"]
        hh={}
        for bb in ls:
          #print "ttV:"+bb+": "+str(type(aaaa[bb]))
          if len(hh.keys())==0:
            hh['ttV']=copy.deepcopy(aaaa[bb])
          else :
            hh['ttV'].Add(copy.deepcopy(aaaa[bb]))
        hh['ttV'].SetFillColor( TColor.GetColor(histograms2["ttV"]["FillColor"]) )
        #hs.Add(copy.deepcopy(hh["ttV"]))
        hs.Add(hh["ttV"])

  for aa in plotSet["bkg"]:
    h={}
    if len(histograms2[aa]["h1"].keys())>0 :
      for bb in ls: 
        if len(h.keys())==0:
          h[aa]=copy.deepcopy(histograms2[aa]["h1"][bb])
        else :
          h[aa].Add(copy.deepcopy(histograms2[aa]["h1"][bb]))
      if isPrint : 
        aaa=""
        if h[aa].GetBinContent(1)==0.   : aaa= " 0 " 
        elif h[aa].GetBinContent(1)<100 : aaa= " "+str(round(h[aa].GetBinContent(1)*10)/10)+" $\pm$ "+str(round(h[aa].GetBinError(1)*10)/10)+" "
        else                            : aaa= " "+str(int(round(h[aa].GetBinContent(1))))+" $\pm$ "+str(int(round(h[aa].GetBinError(1))))+" "
        Stats[aa]=aaa
          
      h[aa].SetFillColor( TColor.GetColor(histograms2[aa]["FillColor"]) )
      #if aa.find("ttV")==-1: hs.Add(copy.deepcopy(h[aa]))
      if aa.find("ttV")==-1: hs.Add(h[aa])

  return hs,Stats

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

def printStat():
  print ""

######################################
######################################
######################################
def aCanvas(mon,step,decay,isLogy,Weight,SFbyFitting):
  from makeMCHistSet import makeMCHistSet,load1stHistograms
  histograms=load1stHistograms(mon,step,Weight,SFbyFitting)
  histograms2,plotSet=makeMCHistSet(histograms)
  StyleUp(histograms2)

  step2="_S"+str(int(step[1])-1)
  canvasname=mon["name"]+step2+decay+"_"+Weight
  c1 = myCanvas(canvasname)#, myPad1(canvasname+"pad1"), myPad2(canvasname+"pad2")

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
  ttbb.SetLineStyle(1);
  ttb.SetLineStyle(2);
  ttcc.SetLineStyle(3);
  ttlf.SetLineStyle(4);

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

  ttbb.Draw("HIST")
  ttb.Draw("sameHIST")
  ttcc.Draw("sameHIST")
  ttlf.Draw("sameHIST")

  title=""
  if mon["Title"] is not None : 
    title = mon["Title"]

  pt,pt2,pt3,pt4 = addLegendCMS(),addLegendPreliminary(),addTitle(title),addLegendLumi()
  pt.Draw(),  pt2.Draw(),  pt3.Draw(), pt4.Draw()

  wid=0.23
  legx1 = 0.65

  leg  = make_legend(legx1,0.60, legx1+wid*0.9,0.86)
  plotSet2= {'bkg2':['Singlet','ZJets'],'bkg': ['ttlf','ttot',"ttV"], 'ttbars': ['ttbb',  'ttb', "ttcc","ttlf"]}
 
  for aa in plotSet2["ttbars"]:
    if len(histograms2[aa]["h1"].keys())>0:
      entry=leg.AddEntry(eval(aa), histograms2[aa]["label"], "l")
      entry.SetLineColor(1),    entry.SetLineStyle(1)
      entry.SetLineWidth(1),    entry.SetMarkerColor(1)
      entry.SetMarkerStyle(21), entry.SetMarkerSize(1)
      entry.SetTextFont(62)
  leg.Draw()
  c1.Print("plots_fit/TH1_Norm_"+canvasname+".eps")
  c1.Print("plots_fit/TH1_Norm_"+canvasname+".C")
 
  c1set = [c1,histograms2,ttbb,ttb,ttcc,ttlf,pt,pt2,pt3,leg]
  return c1set,plotSet#,Stats,plotSet

##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
def printStats(StatsAll,plotSet):
  s1,s2=40,25
  for mc in plotSet["mg5"]:
    label = plotSet["labels"][mc]
    aaa=(" "+label+" ").ljust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  print "\\hline\\hline"
  for mc in plotSet["ttbars"]:
    label = plotSet["labels"][mc]
    aaa=(" "+label+" ").ljust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  print "\\hline"
  for mc in plotSet["bkg"]:
    label = plotSet["labels"][mc]
    aaa=(" "+label+" ").rjust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  print "\\hline\\hline"
  for mc in ["MC","DATA"]:
    aaa=(" "+mc+" ").rjust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\\\hline"
    print aaa


##################################
##################################
##################################
def main():#step, moni):
  import sys
  if len(sys.argv) < 2:
    print "usage : python -i makeCanvas.py S2 I"
    from monitors_cfi import monitors,monitors2d
    for i in range(0,len(monitors)):
      print "I= "+str(i)+" : "+monitors[i]["name"]
    sys.exit()

  step = sys.argv[1]      # 
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

  from monitors_cfi import monitors,monitors2d
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
  SFbyFitting={'ttbbSF':1.62796470428,'ttcclfSF':0.916707908424,'k':0.842498214663}

  #SFbyFitting={'ttbbSF':1.0,'ttcclfSF':1.0,'k':1.0}
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
 

  if runStat : mon = monitors[0]
  else :
    #step="S2"
    #weight="CEN"#csvweight"
    weight="csvweight"
    isLogy = False
    #aaa[1]=aCanvas(mon,step,"MM",isLogy,weight,SFbyFitting)
    #aaa[2]=aCanvas(mon,step,"EE",isLogy,weight,SFbyFitting)
    #aaa[3]=aCanvas(mon,step,"ME",isLogy,weight,SFbyFitting)
    aaa[4]=aCanvas(mon,step,"LL",isLogy,weight,SFbyFitting)
    
  return aaa


if __name__ == "__main__":
  test=main()


