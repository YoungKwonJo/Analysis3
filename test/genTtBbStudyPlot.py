from ROOT import *

#import sys
#sys.path.append('../ntuple2hist')
import os,commands
import subprocess

loc = "/afs/cern.ch/user/y/youngjo/eos/cms/store/user/youngjo/Cattools/v7-6-4v2/"

def files(path):
  return [os.path.join(loc+path,f) for f in os.listdir(loc+path) if os.path.isfile(os.path.join(loc+path,f))]

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


#from mcsample_cfi import fileList,ttbarSelections,ttbarMCsamples,mAND
#from cut_cfi import cut_maker,ll_cuts

def draw(tree, info, weight, sel):
  htemp = TH1D(info["name"],"",info["Nbin"],info["min"],info["max"])
  htemp.Reset()
  htemp.Sumw2()
  tree.Project(info["name"],info["value"],"weight"+"*"+sel)
  htemp.GetXaxis().SetTitle(info["xtitle"])
  return htemp

def loadTree(files):
  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  return chain

def makeHistogram(filename,filelist,weight,color,info_,summary):
  import copy
  tree = loadTree(filelist)
  #value,xtitle="NbJets20","# of bJet20"
  info ={"name":filename+"_"+info_["value"],"Nbin":info_["Nbin"],"min":info_["min"],"max":info_["max"],"value":info_["value"],"xtitle":info_["xtitle"]}
  summary[filename] = {"name":filename,"h1":copy.deepcopy(draw(tree,info,weight,"(1)")),"color":color }


def drawS(histograms,h1,l1,scale,ymin):
  ii,jj=0,0
  for i,mc1 in enumerate(histograms.keys()):
    mc = histograms[mc1]
    if not(mc["name"].find("POW")==0) :
      mc[h1].SetLineColor(TColor.GetColor(mc["color"]))
    else :
      mc[h1].SetMarkerStyle(20)
      mc[h1].SetFillColor(kGray)
    
    l1.AddEntry(mc[h1],mc["name"],"lp")
    mc[h1].Scale(1/mc[h1].Integral())
    if i==0:
      mc[h1].GetYaxis().SetTitle("")
      mc[h1].SetMaximum(mc["h1"].GetMaximum()*scale )
      mc[h1].SetMinimum(ymin)
      mc[h1].Draw()
    #elif mc["name"].find("POWtt")==0 and mc["name"].find("csvweight")>-1:
    #  mc[h1].Draw("e3SAME")
    #  mc[h1].Draw("e1SAME")
    else   : mc[h1].Draw("same")

def makeoutput(outputname, h,h1):
  fout = TFile(""+outputname,"RECREATE")
  for a in h.keys():
    dirA = fout.mkdir(a)
    dirA.cd()
    for b in h[a].keys():
      h[a][b][h1].Write()
  fout.Write()
  fout.Close()

#########################################################
#########################################################
#########################################################
infos ={
 "Nbjet"  :{"Nbin":10,"min":0.,"max":10.,"value":"NbJets","xtitle":"# of bJet"},
 "Nbjet20":{"Nbin":10,"min":0.,"max":10.,"value":"NbJets20","xtitle":"# of bJet20"},
 "Nbjet30":{"Nbin":10,"min":0.,"max":10.,"value":"NbJets30","xtitle":"# of bJet30"},

 "NaddbJets"  :{"Nbin":10,"min":0.,"max":10.,"value":"NaddbJets","xtitle":"# of additional bJet"},
 "NaddbJets20"  :{"Nbin":10,"min":0.,"max":10.,"value":"NaddbJets20","xtitle":"# of additional bJet20"},

 "dRaddbJets"  :{"Nbin":10,"min":0.,"max":2.,"value":"dRaddbJets","xtitle":"DR of additional bJet"},
 "dRaddcJets"  :{"Nbin":10,"min":0.,"max":2.,"value":"dRaddcJets","xtitle":"DR of additional cJet"},
 "dRcJets"     :{"Nbin":10,"min":0.,"max":2.,"value":"dRcJets","xtitle":"DR of  cJet"},
 "dRaddbJetsHad"  :{"Nbin":10,"min":0.,"max":2.,"value":"dRaddbJetsHad","xtitle":"DR of additional bHJet"},
 "dRaddcJetsHad"  :{"Nbin":10,"min":0.,"max":2.,"value":"dRaddcJetsHad","xtitle":"DR of additional cHJet"},
 "dRcJetsHad"  :{"Nbin":10,"min":0.,"max":2.,"value":"dRcJetsHad","xtitle":"DR of cHJet"},

}
allsummary = {}
weights = {"nom":"weight"
  ,"Q2_Up1":"scaleWeightsUp[0]"
  ,"Q2_Up2":"scaleWeightsUp[1]"
  ,"Q2_Up3":"scaleWeightsUp[2]"
  ,"Q2_Dw1":"scaleWeightsDown[0]"
  ,"Q2_Dw2":"scaleWeightsDown[1]"
  ,"Q2_Dw3":"scaleWeightsDown[2]"
}

weights2 = {"nom":"1","weight":"weight"}
ttbarMCsamples = {  "MG5":"TTJets_MG5",         "AMC":"TTJets_aMC",            "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp" ,"upPOW":"TT_powheg_scaleup", "dwPOW":"TT_powheg_scaledown" }
#ttbarMCsamples = {  "POW":"TT_powheg",        "POHP":"TT_powheg-herwigpp" }
colors = ["#FF0000", "#0000FF", "#008000", "#00FFFF", "#800080", "#FF00FF", "#00FF00", "#000000", "#808080", "#FFA500", "#008080", "#000080", "#DDA0DD", "#FFE4C4", "#B0C4DE", "#ffd700"]

for j,y in enumerate(infos.keys()):
  summary={}
  info_ = infos[y] 
  for i,x in enumerate(ttbarMCsamples.keys()):
    fileList=files(ttbarMCsamples[x]+"v1")
    makeHistogram(x,fileList,weights2["nom"],colors[i],info_,summary)
  allsummary[j]=summary

#print allsummary

""""
l1 = make_legend(0.29,0.26,0.73,0.88)
l2 = make_legend(0.39,0.46,0.73,0.88)

c1 = TCanvas("c1","",900,600)
c1.Divide(3,2)
h1="h1"
#hh=int(arg1)+1
#if hh==2: h1="h2"
scale=100.
ymin=0.0000001

c1.cd(1).SetLogy(), drawS(allsummary[0],h1, l1,scale,ymin)
c1.cd(2).SetLogy(), drawS(allsummary[1],h1, l2,scale,ymin)
c1.cd(3).SetLogy(), drawS(allsummary[2],h1, l2,scale,ymin)
c1.cd(4).SetLogy(), drawS(allsummary[3],h1, l2,scale,ymin)
c1.cd(5).SetLogy(), drawS(allsummary[4],h1, l2,scale,ymin)
c1.cd(6).SetLogy(), drawS(allsummary[5],h1, l2,scale,ymin)
c1.cd(6), l1.Draw()
c1.Print("plots/genjet2.eps")
"""

makeoutput("genjet.root", allsummary,h1)

