from ROOT import *
#from mcsample_cfi import *

import os,commands
import subprocess

def files(path):
    #import socket
    #hostname = socket.gethostname()
    #if hostname.find("home")>-1:
    #  llll = [""]
    #  return llll

    cmd, xrdbase = "xrd cms-xrdr.sdfarm.kr ls ","/xrd"
    size = 0
    l = set()
    for x in subprocess.check_output(cmd + xrdbase + path, shell=True).strip().split('\n'):
        xx = x.split()
        if len(xx) == 0: continue
        if xx[0][0] not in ('d', '-'): continue
        xpath = xx[-1]
        if len(xpath) == 0: continue
        xsize = int(xx[1])
        if xpath.startswith(xrdbase): xpath = xpath[len(xrdbase):]
        if xpath in l: continue
        l.add(xpath)
        size += xsize
    lll ="root://cms-xrdr.sdfarm.kr:1094///xrd" 
    llll = [ lll+l1 for l1 in l]
    #print llll
    return llll

def addLegend(text):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,text)
  title.SetNDC()
  title.SetTextAlign(12)
  title.SetX(0.20)
  title.SetY(0.83)
  title.SetTextFont(42)
  title.SetTextSize(0.05)
  title.SetTextSizePixels(24)
  title.Draw()

  return title

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

import copy
def piechart(json,name):
  pie = TPie("pie", name,len(json.keys()))
  CS = ["#660000", "#ffcc00", "#cc6600", "#ff0000","#ff6565"]

  tot=0.
  for i,ii in enumerate(json.keys()):
    tot += json[ii]
  pieleg = make_legend(0.40,0.71, 0.86,0.9)
  hh={}
  for i,ii in enumerate(json.keys()):
    pie.SetEntryVal(i,json[ii])
    pie.SetEntryLabel(i,ii)
    ci = TColor.GetColor(CS[i])
    pie.SetEntryFillColor(i,ci)
    h1 = TH1F("h1"+ii,"",1,0,1)
    h1.SetFillColor(ci)
    text = ii+((" (%.5f)"%(json[ii]/tot)).rjust(10))
    text = text+((" %d"%json[ii]).rjust(9))
    hh[ii]=copy.deepcopy(h1)
    pieleg.AddEntry(hh[ii], text,"f")

  ci = TColor.GetColor("#ffffff")
  h1 = TH1F("h1all","",1,0,1)
  h1.SetFillColor(ci)
  h1.SetLineColor(ci)
  hh["all"]=copy.deepcopy(h1)
  text = ("all  "+((" (1.00000)").rjust(10))+((" %d"%tot).rjust(9)))
  pieleg.AddEntry(hh["all"], text,"f")
  pie.SetRadius(0.35)
  pie.SetY(.35)
  pie.SetLabelsOffset(.01)

  return pie,pieleg,hh


def getEntriesy(tree, sel1):
  htemp = TH1D("htemp1","",1,-20,20)
  tree.Project("htemp1","1",sel1)
  return htemp.GetEntries()

def loadfiles(files):
  chain = TChain("cattree/nom")
  #chain = TChain("cattree/genTop")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  return tree

def loadSel(tree,sel,sels):
  summary = {}
  for ii in sels.keys():
    summary[ii]=getEntriesy(tree, "("+sel+"&&"+sels[ii]+")" )
  return summary

def SavePDF(pow, name):
  pie,pieleg,hh=piechart(pow,name)
  c1 = TCanvas( "c1"+name, '',1)
  gStyle.SetOptTitle(1)
  pie.Draw("nol")
  pieleg.Draw()
  c1.Print(name+".pdf")
  c1.Print(name+".png")
  return c1


gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()

ttbarPOW = "TT_powheg"
#ttbarPOW = "TTJets_MG5"
loc = "/store/user/youngjo/Cattools/v7-6-2v1/"
z="v3"

tree=loadfiles(files(loc + ttbarPOW+z))
#tree=loadfiles(["/cms/home/chanwook/work/ttbb/cattools/src/CATTools/CatAnalyzer/test/TTBBGenAnalyzer_TT_powheg.root"])

##################
dileptonic0  ="(diLeptonic0==1 )"
dileptonicm1 ="(diLeptonicM1==1)"
dileptonicp1 ="(diLeptonicP1)"
semiLeptonic0 ="( semiLeptonic0 == 1)"
semiLeptonicm1 ="( semiLeptonicM1 == 1)"
semiLeptonicp1 ="( semiLeptonicP1 == 1)"
allHadronic ="( allHadronic == 1)"

TTJJ = "(NaddJets20 >= 2)"
TTBB = "(NaddbJets20 >= 2)"
TTBJ = "(NaddJets20 >= 2 && NaddbJets20 == 1)"
TTCC = "(NcJets20 >= 2 && NaddJets20 >= 2)"
TTLF = "("+TTJJ+" && !"+TTBB+" && !"+TTBJ+" && !"+TTCC+")"
#TTLF = "("+TTJJ+" && !("+TTBB+" || "+TTBJ+" || "+TTCC+"))"
TTNN ={
 "ttbb":TTBB, "ttbj":TTBJ, "ttcc":TTCC, "ttLF":TTLF
}

ETC = "(!"+dileptonic0+" && !"+semiLeptonic0+" && !"+allHadronic+")"
CHANNEL ={
  "dileptonic": dileptonicm1,
  "semileptonic": semiLeptonicm1,
  "hadronic": allHadronic,
  "etc": ETC
}

#################
#################
#dilepH = "("+dileptonic0+" && NJets20>=4 )"
#semilepH = "("+semiLeptonic0+" && NJets20>=6 )"
dilepH   = dileptonic0  
semilepH = semiLeptonic0
ttbbH = " (genTtbarId%100>52) "
ttbjH = " (genTtbarId%100>50 && genTtbarId%100<53) "
ttcjH = " (genTtbarId%100>40 && genTtbarId%100<43) "
ttccH = " (genTtbarId%100>42 && genTtbarId%100<49) "
ttlfH = " (genTtbarId%100 <41) "
TTNNH = {
  "ttbb":ttbbH,   "ttbj":ttbjH,   "ttcc":ttccH,   "ttlf":ttlfH 
}
dilepHv = "( lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4 && NJets20>=4 )"
semilepHv = "((((lepton1_pt>20 && abs(lepton1_eta)<2.4) && !(lepton2_pt>20  && abs(lepton2_eta)<2.4)) || (!(lepton1_pt>20 && abs(lepton1_eta)<2.4) && (lepton2_pt>20  && abs(lepton2_eta)<2.4))  ) && NJets20>=6 )"

#################
ttjjDiLeptonVis="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
ttbbvis = "(NbJets20>=4)" 
ttbjvis = "(NbJets20==3)" 
ttccvis = "((NcJets20>=2) && !(NbJets20>=3))"
ttlfvis = "(!"+ttbbvis+" && !"+ttbjvis+" && !"+ttccvis+")"
TTNNvis ={
  "ttbb":ttbbvis,   "ttbj":ttbjvis,   "ttcc":ttccvis,   "ttlf":ttlfvis 
}
#################
ttjjSemiLeptonVis = "((((lepton1_pt>20 && abs(lepton1_eta)<2.4) && !(lepton2_pt>20  && abs(lepton2_eta)<2.4)) || (!(lepton1_pt>20 && abs(lepton1_eta)<2.4) && (lepton2_pt>20  && abs(lepton2_eta)<2.4))  ) && NJets20>=6 && NbJets20>=2 )"
#ttjjSemiLeptonVis="(NJets20>=6 && NbJets20>=2 && ((lepton1_pt>20 && abs(lepton1_eta)<2.4) ^ (lepton2_pt>20  && abs(lepton2_eta)<2.4)))"
#################
#################
#################
pow0=loadSel(tree,"(1)",CHANNEL)
#pow1=loadSel(tree,"(1)",TTNN)
pow11=loadSel(tree,dileptonicm1,TTNN)
#pow2=loadSel(tree,semiLeptonic0,TTNN)
#pow3=loadSel(tree,allHadronic,TTNN)

pow4=loadSel(tree,ttjjDiLeptonVis,TTNNvis)
#pow5=loadSel(tree,ttjjSemiLeptonVis,TTNNvis)

#pow6=loadSel(tree,dilepH,TTNNH)
#pow7=loadSel(tree,semilepH,TTNNH)

#pow8=loadSel(tree,dilepHv,TTNNH)
#pow9=loadSel(tree,semilepHv,TTNNH)
#################
SavePDF(pow0,"POWttbarall")
#SavePDF(pow1,"POWttbarFullPhase")
SavePDF(pow11,"POWttbarDileptonicFullPhase")
#SavePDF(pow2,"POWttbarSemileptonicFullPhase")
#SavePDF(pow3,"POWttbarHadronicFullphase")

SavePDF(pow4,"POWttbarDileptonicVisiblePhase")
#SavePDF(pow5,"POWttbarSemileptonicVisiblePhase")

#SavePDF(pow6,"POWttbarDileptonicTTHFull")
#SavePDF(pow7,"POWttbarSemileptonicTTHFull")

#SavePDF(pow8,"POWttbarDileptonicTTHVisible")
#SavePDF(pow9,"POWttbarSemileptonicTTHVisible")

