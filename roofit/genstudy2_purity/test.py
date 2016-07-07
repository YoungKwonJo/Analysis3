from ROOT import *
import copy

def addText():
  chtitle = TLatex(-20.,50.,("matching efficiency") )
  chtitle.SetNDC(),         chtitle.SetTextAlign(12)
  chtitle.SetX(0.40),  chtitle.SetY(0.65)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)

  return chtitle
def addText2(ll):
  chtitle = TLatex(-20.,50.,("(DR<0.5) : "+str(round(ll*100)/100)+" %") )
  chtitle.SetNDC(),         chtitle.SetTextAlign(12)
  chtitle.SetX(0.40),  chtitle.SetY(0.6)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)

  return chtitle


def getTH1DFlat(f1):
  tgs = []
  ytitle=""
  for key in [x.GetName() for x in f1.GetListOfKeys()]:
    obj = f1.Get(key)
    if obj == None: continue
    elif obj.IsA().InheritsFrom("TH1D"):
     if ytitle=="" : ytitle=obj.GetYaxis().GetTitle()
     tgs.append( copy.deepcopy(obj) )
  return tgs,ytitle

def getTH2DFlat(f1):
  tgs = []
  ytitle=""
  for key in [x.GetName() for x in f1.GetListOfKeys()]:
    obj = f1.Get(key)
    if obj == None: continue
    elif obj.IsA().InheritsFrom("TH2F"):
     if ytitle=="" : ytitle=obj.GetYaxis().GetTitle()
     tgs.append( copy.deepcopy(obj) )
  return tgs,ytitle

def drawCanvas(tg,outputfolder,option):
  print ""
  print ""
  c1 = TCanvas("c1","",400,400)
  tg.SetLineColor(kRed)
  tg.GetYaxis().SetTitleOffset(1.2)
  tg.GetXaxis().SetTitleOffset(1.2)
  tg.GetXaxis().SetTitle("DR")
  tg.Scale(1./tg.GetEntries())
  tg.Draw()
  tg.Draw(option)
  leg1=addText()
  leg2=addText2(tg.Integral(1,5)/tg.Integral(1,51)*100.)
  leg1.Draw()
  leg2.Draw()

  c1.Print(outputfolder+"/"+tg.GetName()+".pdf")
  return c1,tg

def drawCanvas2d(tg,outputfolder,option):
  print ""
  print ""
  c1 = TCanvas("c1","",400,400)
  tg.SetLineColor(kRed)
  tg.SetTitle("")
  tg.GetXaxis().SetTitle("1st b-jet")
  tg.GetYaxis().SetTitle("2nd b-jet")
  tg.GetYaxis().SetTitleOffset(1.2)
  tg.GetXaxis().SetTitleOffset(0.9)
  tg.GetYaxis().SetTitleSize(0.06)
  tg.GetXaxis().SetTitleSize(0.06)

  tg.GetXaxis().SetLabelSize(0.06);
  tg.GetYaxis().SetLabelSize(0.06);
  tg.GetXaxis().SetBinLabel(1,"False");
  tg.GetXaxis().SetBinLabel(2,"True");
  tg.GetYaxis().SetBinLabel(1,"False");
  tg.GetYaxis().SetBinLabel(2,"True");

  tg.SetMarkerSize(3)
  tg.Scale(1./tg.GetEntries())
  tg.SetBinContent(1,1, round(tg.GetBinContent(1,1)*100.)/100.)
  tg.SetBinContent(1,2, round(tg.GetBinContent(1,2)*100.)/100.)
  tg.SetBinContent(2,1, round(tg.GetBinContent(2,1)*100.)/100.)
  tg.SetBinContent(2,2, round(tg.GetBinContent(2,2)*100.)/100.)

  tg.Draw()
  tg.Draw("samecolz")
  tg.Draw(option)
  #leg1=addText()
  #leg2=addText2(tg.Integral(1,5)/tg.Integral(1,51)*100.)
  #leg1.Draw()
  #leg2.Draw()
  c1.Print(outputfolder+"/"+tg.GetName()+".pdf")
  return c1,tg


gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)

#gROOT.ProcessLine(".L tdrStyle.C")
#setTDRStyle()
gStyle.SetCanvasDefH(400)
gStyle.SetCanvasDefW(400)
#gStyle.SetPadTickX(0)
#gStyle.SetPadTickY(0)


gStyle.SetPadTopMargin(0.12);
gStyle.SetPadLeftMargin(0.19);
gStyle.SetPadRightMargin(0.05);
gStyle.SetPadBottomMargin(0.12);


#loc = "/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/temp"
loc="/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/Analysis3/roofit/genstudy2_purity"
f = TFile.Open(loc+"/output.root")

th1ds,ytitle = getTH1DFlat(f)#.Get("cattree"))
th2ds,ytitle = getTH2DFlat(f)#.Get("cattree"))
outputfolder = "plots"

for i,th1 in enumerate(th1ds):
  drawCanvas(th1,outputfolder,"samehist")

for i,th2 in enumerate(th2ds):
  drawCanvas2d(th2,outputfolder,"sametext")




