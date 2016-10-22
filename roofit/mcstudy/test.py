#! /usr/bin/env python

from ROOT import *
import copy

loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/"

def loadHistogramMC(mc,label,total):
  f = TFile.Open(loc+"/hist_csvweight.root")
  HN="jet3CSV_jet4CSV"
  h1 = f.Get(mc+"/csvweight/h2_"+mc+"_"+HN+"_mm_S6_csvweight").Clone("h2_"+mc+"_S6mm"+"_csvweight")
  h2 = f.Get(mc+"/csvweight/h2_"+mc+"_"+HN+"_ee_S6_csvweight").Clone("h2_"+mc+"_S6ee"+"_csvweight")
  h3 = f.Get(mc+"/csvweight/h2_"+mc+"_"+HN+"_em_S6_csvweight").Clone("h2_"+mc+"_S6em"+"_csvweight")
  h1.Add(h2)
  h1.Add(h3)
  if mc is "POWttb":
    mc2="POWtt2b"
    h12 = f.Get(mc2+"/csvweight/h2_"+mc2+"_"+HN+"_mm_S6_csvweight").Clone("h2_"+mc2+"_S6mm"+"_csvweight")
    h22 = f.Get(mc2+"/csvweight/h2_"+mc2+"_"+HN+"_ee_S6_csvweight").Clone("h2_"+mc2+"_S6ee"+"_csvweight")
    h32 = f.Get(mc2+"/csvweight/h2_"+mc2+"_"+HN+"_em_S6_csvweight").Clone("h2_"+mc2+"_S6em"+"_csvweight")
    h1.Add(h12)
    h1.Add(h22)
    h1.Add(h32)
 
  h1.SetTitle(mc)
  h1.Scale(total)
  for i in range(1,11):
    for j in range(1,11):
       h1.SetBinContent(i,j,round(h1.GetBinContent(i,j)) )

  h1.GetYaxis().SetTitleOffset(1.)
  h1.GetYaxis().SetTitleSize(0.08)
  h1.GetYaxis().SetLabelSize(0.060)
#  h1.GetYaxis().SetNdivisions(607)

#  h1.GetXaxis().SetNdivisions(509)
  h1.GetXaxis().SetLabelSize(0.06)
  h1.GetXaxis().SetTitleOffset(0.88)
  h1.GetXaxis().SetTitleSize(0.076)

  #h1.GetYaxis().SetTitle("b discriminator of jet_{4th}")
  #h1.GetXaxis().SetTitle("b discriminator of jet_{3rd}")
  h1.GetYaxis().SetTitle("b discriminator of 4^{th} jet")
  h1.GetXaxis().SetTitle("b discriminator of 3^{rd} jet")


  return {"name":mc,"h2":copy.deepcopy(h1),"label":label } 

def addLegend(name):
  tex = TLatex(0.3,0.83,name)
  tex.SetNDC()
  tex.SetTextAlign(12)
  tex.SetTextFont(42)
  tex.SetTextSize(0.07913043)
  #tex.SetTextSize(0.05913043)
  #tex.SetTextSize(0.05913043)
  tex.SetLineWidth(2)
  return tex

POWttbar = ["POWttbb","POWttb","POWttcc","POWttlf","POWttot"]
POWttbar2 = ["t#bar{t}b#bar{b}","t#bar{t}bj","t#bar{t}cc","t#bar{t}LF","t#bar{t} others"]#,"POWttot"]

#POLLttbar = ["POLLttbb","POLLttb","POLLtt2b","POLLttcc","POLLttlf"]#,"POWttot"]
h2All=[]

#for i in POLLttbar:
#  h2All.append(loadHistogramMC(i,107163544.0))
for i,mc in enumerate(POWttbar):
  h2All.append(loadHistogramMC(mc,POWttbar2[i],97994442.0))

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()

c1 = TCanvas("c1","",900,600)
c1.SetGrayscale(True)
c1.Divide(3,2)
label = {}
for i in range(1,6):
  c1.cd(i)
  #pad1 = TPad("pad"+str(i),"",0,0,1,1)
  #pad1.Draw()
  #pad1.cd()
  h1 = h2All[i-1]["h2"]
  label[i] = addLegend(h2All[i-1]["label"])
  #h1.Draw("colz")
  h1.Draw("col")
  label[i].Draw();
  #h1.Draw("colztext")
  print h1.GetTitle()+":"+str(h1.Integral())


c1.cd(6)
tex = TLatex(0.1,0.63,"CMS #it{Simulation}")
tex.SetNDC()
tex.SetTextAlign(12)
tex.SetTextFont(42)
tex.SetTextSize(0.09913043)
#tex.SetTextSize(0.05913043)
tex.SetLineWidth(2)
tex.Draw()

tex2 = TLatex(0.1,0.45,"(13 TeV)")
tex2.SetNDC()
tex2.SetTextAlign(12)
tex2.SetTextFont(42)
tex2.SetTextSize(0.09913043)
#tex2.SetTextSize(0.05913043)
tex2.SetLineWidth(2)
tex2.Draw()

c1.Print("TH2D_jet3CSV_jet4CSV_colg.eps")
c1.Print("TH2D_jet3CSV_jet4CSV_colg.C")
c1.Print("TH2D_jet3CSV_jet4CSV_colg.png")
