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
  leg.SetFillColor(0),  leg.SetLineColor(1), leg.SetTextFont(62),  leg.SetTextSize(0.03)
  leg.SetBorderSize(1), leg.SetLineStyle(1), leg.SetLineWidth(1),  leg.SetLineColor(0)
  return leg

def addLegendLumi():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"CMS #sqrt{s} = 13TeV, L = 2.2 fb^{-1}")
  title.SetNDC(),        title.SetTextAlign(12),   title.SetX(0.20),      title.SetY(0.83)
  title.SetTextFont(42)#, title.SetTextSize(0.05),  title.SetTextSizePixels(24)
  #title.SetTextFont(42), title.SetTextSize(0.1),  title.SetTextSizePixels(24)
  title.Draw()
  return title

def addLegendCMS():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"Preliminary")
  tex2.SetNDC(),          tex2.SetTextAlign(12),  tex2.SetX(0.25),        tex2.SetY(0.93)
  tex2.SetTextColor(2),   tex2.SetTextFont(42) #,   tex2.SetTextSize(0.2), tex2.SetTextSizePixels(24)
  #tex2.SetTextColor(2),   tex2.SetTextFont(42),   tex2.SetTextSize(0.05), tex2.SetTextSizePixels(24)
  return tex2

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("ME")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("MM")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("EE")>-1 : ll2="e^{#mp}e^{#pm} channel"
  chtitle = TLatex(-20.,50.,ll2)
  chtitle.SetNDC(),         chtitle.SetTextAlign(12),   chtitle.SetX(0.20),  chtitle.SetY(0.75)
  chtitle.SetTextFont(42) #,  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)
  #chtitle.SetTextFont(42),  chtitle.SetTextSize(0.05),  chtitle.SetTextSizePixels(24)

  return chtitle

def myCanvas(name):
  c1 = TCanvas( name, '',1)#, 500, 500 )
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
  hdata.GetYaxis().SetTitleOffset(1.2)
  hdata.GetYaxis().SetTitleSize(0.07)
  hdata.GetYaxis().SetLabelSize(0.055)
  hdata.GetYaxis().SetNdivisions(607)
  #hdata.GetYaxis().SetLabelSize(0.05)
  #hYaxis = hdata.GetYaxis()
  #hYaxis.SetMaxDigits(3)
  hdata.GetXaxis().SetLabelSize(0.0)
  #hdata.GetXaxis().SetTitle("")

  hdata.SetMarkerStyle(20)
  hdata.SetMarkerSize(0.7)

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
  hdata.SetMarkerSize(0.5)
  hdata.SetMarkerColor(1)
  hdata.SetLineColor(1)
  hdata.SetLineWidth(1)
  hdata.SetMaximum(2)
  hdata.SetMinimum(0)
  hdata.SetTitle("")
  
  hdata.GetYaxis().SetTitle("Obs/Exp")
  hdata.GetYaxis().CenterTitle()
  hdata.GetYaxis().SetTitleOffset(0.45)
  hdata.GetYaxis().SetTitleSize(0.16)
  hdata.GetYaxis().SetLabelSize(0.15)
  hdata.GetYaxis().SetNdivisions(402)
  hdata.GetXaxis().SetNdivisions(509)
  hdata.GetXaxis().SetTitleOffset(1.1)
  hdata.GetXaxis().SetLabelSize(0.20)
  hdata.GetXaxis().SetTitleSize(0.16)
  
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
      hs.Add(copy.deepcopy(h[aa]))

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
        hs.Add(copy.deepcopy(hh["ttV"]))

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
      if aa.find("ttV")==-1: hs.Add(copy.deepcopy(h[aa]))

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
def aCanvas(mon,step,decay,isLogy,Weight):
  from makeMCHistSet import makeMCHistSet,load1stHistograms
  histograms=load1stHistograms(mon,step,Weight)
  histograms2,plotSet=makeMCHistSet(histograms)
  StyleUp(histograms2)

  canvasname=mon["name"]+step+decay+"_"+Weight
  c1,pad1,pad2 = myCanvas(canvasname), myPad1(canvasname+"pad1"), myPad2(canvasname+"pad2")
  c1.Divide(1,2)
  pad1.Draw(), pad1.cd()
  if isLogy : pad1.SetLogy()
  ########################
  ########################
  ########################
  DATA   =  AddHist(decay,histograms2["DATA"])
  MCtot1 =  AddHist(decay,histograms2["MCtot1"])
  MCtot1gr =  myHist2TGraphError(MCtot1)
  MCtot2 =  AddHist(decay,histograms2["MCtot2"])
  MCtot3 =  AddHist(decay,histograms2["MCtot3"])

  isPrint =  (mon["name"] is "Stat")
  #if isPrint : print "channel : "+str(decay)+", Step:"+str(step)+" "+str(mon["name"])
  hs,Stats = StackHist(decay,histograms2,plotSet,isPrint)
  name = MCtot1.GetName()
  if isPrint : 
    aaa=""
    if MCtot1.GetBinContent(1)<100 : aaa= " "+str(round(MCtot1.GetBinContent(1)*10)/10)+" $\pm$ "+str(round(MCtot1.GetBinError(1)*10)/10)+" "
    else                           : aaa= " "+str(int(round(MCtot1.GetBinContent(1))))+" $\pm$ "+str(int(round(MCtot1.GetBinError(1))))+" "
    Stats["MC"]=aaa
    Stats["DATA"]= " "+str(int(round(DATA.GetBinContent(1))) )+" "

  ####################################
  if isLogy : 
    scale = MCtot1.GetMaximum()
    maxY,minY=0., 1.
    for i in range(int(DATA.GetNbinsX()*0.7)+1, DATA.GetNbinsX()+2):
       if maxY<DATA.GetBinContent(i): maxY=DATA.GetBinContent(i)
    ttbbMuMu=histograms2["ttbb"]["h1"]["hMM"]
    for i in range(1, ttbbMuMu.GetNbinsX()+2):
      if ttbbMuMu.GetBinContent(i)>0 and minY>ttbbMuMu.GetBinContent(i): minY=ttbbMuMu.GetBinContent(i)

    DATA.SetMaximum(maxY*10000)
    if maxY*10000 < scale*140 : DATA.SetMaximum(scale*140)
    if   minY>1     :  DATA.SetMinimum( 4.0 )
    elif minY>0.4   :  DATA.SetMinimum( 0.4 )
    elif minY>0.04  :  DATA.SetMinimum( 0.04 )
    elif minY<0.04  :  DATA.SetMinimum( 0.004 )
  else :
    DATA.SetMaximum( 2.2*max(DATA.GetMaximum(),MCtot1.GetMaximum()) )

  ##################################
  myDataHistStyleUp(DATA)
  DATA.GetYaxis().SetTitle("Events")
  DATA.GetXaxis().SetTitle("")
  DATA.Draw(), hs.Draw("same,hist"), MCtot1gr.Draw("e2same"), MCtot2.Draw("same"), MCtot3.Draw("same")
  DATA.Draw("same")

  ########################
  ########################
  pt,pt2,pt3 = addLegendLumi(),addLegendCMS(),addDecayMode(decay)
  pt.Draw(),  pt2.Draw(),  pt3.Draw()
  ########################
  ########################
  legx1 = 0.8
  wid=0.12
  legx2 = 0.67
  leg  = make_legend(legx1,0.64, legx1+wid,0.88)
  leg2 = make_legend(legx2,0.68, legx2+wid,0.88)
  leg3 = make_legend(legx1,0.56, legx1+wid,0.63)
  #leg3 = make_legend(legx1,0.54, legx1+wid,0.63)
  for aa in plotSet["ttbars"]:
    if len(histograms2[aa]["h1"].keys())>0:
      leg.AddEntry(histograms2[aa]["h1"]["hMM"], histograms2[aa]["label"], "f")
  leg.AddEntry(histograms2["DATA"]["h1"]["hMM"], histograms2["DATA"]["label"], "p")
  for aa in plotSet["bkg"]:
    #print ""+str(histograms2[aa])
    if len(histograms2[aa]["h1"].keys())>0:
      leg2.AddEntry( histograms2[aa]["h1"]["hMM"], histograms2[aa]["label"], "f")

  for aa in plotSet["others"]:
    if len(histograms2[aa]["h1"].keys())>0:
      leg3.AddEntry(histograms2[aa]["h1"]["hMM"], histograms2[aa]["label"], "l")
  #leg3.AddEntry(histograms2["ttH"]["h1"]["hMM"], histograms2["ttH"]["label"], "l")
  ###############
  leg.Draw(),  leg2.Draw(),  leg3.Draw()
  pad1.Modified()
  c1.cd(),  pad2.Draw(),  pad2.cd()
  ########################
  ########################
  ratio3,ratio2,ratio1 = DATA.Clone("AMC"),DATA.Clone("MG5"),DATA.Clone("POW")
  ratio1.Divide(MCtot1),  copyStyleUp(ratio1, MCtot1) 
  ratio2.Divide(MCtot2),  copyStyleUp(ratio2, MCtot2) 
  ratio3.Divide(MCtot3),  copyStyleUp(ratio3, MCtot3) 
  styleBottomUp(ratio1)
  ratio1.GetXaxis().SetTitle(mon['unit'])
  ratio1.Draw()
  ratioSyst=myRatioSyst(ratio1)
  ratioSyst.Draw("e2")
  ratio1.Draw("e1SAME")
  ratio2.Draw("histSAME")
  ratio3.Draw("histSAME")

  ########################
  ########################
  pad2.Modified()
  c1.cd(), c1.Modified(), c1.cd()
  if isLogy : c1.Print("plots/TH1_"+canvasname+".eps")
  else      : c1.Print("plots/TH1_"+canvasname+"_Li.eps")
  c1set = [c1,pad1,pad2,histograms2,hs,MCtot1,MCtot2,MCtot3,DATA,pt,pt2,pt3,leg,leg2,leg3,ratio1,ratio2,ratio3,ratioSyst]
  return c1set,Stats,plotSet

##################################
##################################
##################################
##################################
##################################
##################################
##################################
##################################
def printStats(StatsAll,plotSet):
  s1,s2=10,25
  for mc in plotSet["mg5"]:
    aaa=(" "+mc+" ").ljust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  for mc in plotSet["ttbars"]:
    aaa=(" "+mc+" ").ljust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  for mc in plotSet["bkg"]:
    aaa=(" "+mc+" ").rjust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa
  for mc in ["MC","DATA"]:
    aaa=(" "+mc+" ").rjust(s1)
    for step in sorted(StatsAll.keys()):
      aaa+=(" & "+StatsAll[step][mc]).ljust(s2)
    aaa+="  \\\\"
    print aaa


##################################
##################################
##################################
def main():#step, moni):
  import sys
  if len(sys.argv) < 2:
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
  mon = monitors[moni]
  if runStat : mon = monitors[0]
  else :
    #step="S2"
    weight="csvweight"
    isLogy = True
    aaa[1]=aCanvas(mon,step,"MM",isLogy,weight)
    aaa[2]=aCanvas(mon,step,"EE",isLogy,weight)
    aaa[3]=aCanvas(mon,step,"ME",isLogy,weight)
    aaa[4]=aCanvas(mon,step,"LL",isLogy,weight)
    
  if runStat:
    mon = monitors[0]
    decay = "LL"
    if moni==1 : decay = "MM"
    if moni==2 : decay = "ME"
    if moni==3 : decay = "EE"
    aaa[4],StatsAll["S2"],plotSet=aCanvas(mon,"S2",decay,True,"csvweight")
    aaa[4],StatsAll["S3"],plotSet=aCanvas(mon,"S3",decay,True,"csvweight")
    aaa[4],StatsAll["S4"],plotSet=aCanvas(mon,"S4",decay,True,"csvweight")
    aaa[4],StatsAll["S5"],plotSet=aCanvas(mon,"S5",decay,True,"csvweight")
    aaa[4],StatsAll["S6"],plotSet=aCanvas(mon,"S6",decay,True,"csvweight")
    
    #print str(StatsAll)
    printStats(StatsAll,plotSet)  

  return aaa


if __name__ == "__main__":
  test=main()


