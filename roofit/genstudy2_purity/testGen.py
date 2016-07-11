from ROOT import *

def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0),  leg.SetLineColor(1), leg.SetTextFont(62),  leg.SetTextSize(0.04)
  leg.SetBorderSize(1), leg.SetLineStyle(1), leg.SetLineWidth(1),  leg.SetLineColor(0)
  return leg

gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000),    gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)

c1 = TCanvas("c1","",500,500)
loc="/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/Analysis3/roofit/genstudy2_purity"
f = TFile.Open(loc+"/output_TT.root")

h1=f.Get("h1_diVisTTJets_MG5_Ngenbjet_")
h2=f.Get("h1_diVisTTJets_aMC_Ngenbjet_")
h3=f.Get("h1_diVisTT_powheg_Ngenbjet_")

h1.Scale(1./h1.Integral())
h2.Scale(1./h2.Integral())
h3.Scale(1./h3.Integral())
h1.SetLineColor(kBlue)
h2.SetLineColor(kGreen)
h3.SetLineColor(kRed)

h1.SetTitle("")
h1.GetXaxis().SetTitle("# of bjet_{GEN}")


h1.SetMaximum(h1.GetMaximum()*2)
h1.Draw("H")
h2.Draw("sameH")
h3.Draw("sameH")


leg  = make_legend(0.6,0.6, 0.89,0.88)
leg.AddEntry(h1, "Madgraph", "l")
leg.AddEntry(h2, "aMC@NLO", "l")
leg.AddEntry(h3, "POWHEG", "l")
leg.Draw()



mg5=h1.GetBinContent(5) / h1.GetBinContent(4)
amc=h2.GetBinContent(5) / h2.GetBinContent(4)
powheg=h3.GetBinContent(5) / h3.GetBinContent(4)

mg5sys= (powheg-mg5)/powheg
amcsys= (powheg-amc)/powheg


print "mg5:"+str(mg5)+",(sys):"+str(mg5sys)+" , amc:"+str(amc)+",(sys):"+str(amcsys)+" , powheg"+str(powheg)




