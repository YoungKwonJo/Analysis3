from ROOT import *

gStyle.SetOptStat(0)

import sys
if len(sys.argv) < 4:
  sys.exit()

a1 = int(sys.argv[1]) # 
a2 = int(sys.argv[2]) # 
a3 = int(sys.argv[3]) # 
a4 = int(sys.argv[4]) # 


f = None
fs = ["ttbar","ttcc"]
if a1<2 : f = TFile.Open(fs[a1]+".root")
else    : sys.exit()

folder = None
folders = ["NJets20","NbJets20","NcJets20","NaddcJets20","NaddbJets20"]
if a2<5: folder= folders[a2]

ch=""
chs=["SL","LL","HH"]
if a1 is 0 and a3<3: ch=chs[a3]


wi = folder+"/h"+folder+ch+"withCW"
wo = folder+"/h"+folder+ch+"withoutCW"

h  =  f.Get(wi).Clone("ttbar")
h2 =  f.Get(wo).Clone("ttbar2")
h2.GetXaxis().SetTitle(folder)
h.SetLineColor(2)
h2.SetLineColor(4)

if a4 is 0 : h.Scale( 1./h.Integral() ), h2.Scale( 1./h2.Integral() )

h2.SetMaximum( h2.GetMaximum()*1.5 )

c1 = TCanvas(1)
#if a4 is 0 : c1.SetLogy()

h2.Draw(), h.Draw("same")

leg = TLegend(0.55,0.8, 0.89,0.89)
leg.AddEntry(h,"with cq from W in "+ch+" for "+fs[a1] )
leg.AddEntry(h2,"without cq from W in "+ch+" for "+fs[a1] )
leg.Draw()


