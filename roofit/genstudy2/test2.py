from ROOT import *
import copy

#from q2Weight_Run  import POW2, dwPOW2, upPOW2, AMC2, MG52, POHP2 
from q2result import POW, dwPOW, upPOW, AMC, MG5, POHP 

def make_legend(xmin,ymin,xmax,ymax):
  #leg = TLegend(0.65,0.7, 0.89,0.89)
  leg = TLegend(xmin,ymin,xmax,ymax)
  leg.SetFillColor(0),  leg.SetLineColor(1), leg.SetTextFont(62),
  #leg.SetTextSize(0.03)
  leg.SetTextSize(0.1)
  leg.SetBorderSize(0), leg.SetLineStyle(1), leg.SetLineWidth(1),  leg.SetLineColor(0)
  return leg

def addLegendLumi():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  #title  = TLatex(-20.,50.,"2.3 fb^{-1} (13 TeV)")
  title  = TLatex(-20.,50.,"#sqrt{s}= 13 TeV, 2.3 fb^{-1}")
  title.SetNDC(),        title.SetTextAlign(12)
  title.SetX(0.10),      title.SetY(0.74)
  title.SetTextFont(42)#, title.SetTextSize(0.059)#,
  title.SetTextSizePixels(40)
  #title.SetTextFont(42), title.SetTextSize(0.1),  title.SetTextSizePixels(24)
  title.Draw()
  return title

def addLegendPreliminary():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"#bf{CMS} Preliminary")
  tex2.SetNDC(),          tex2.SetTextAlign(12)
  tex2.SetX(0.10),        tex2.SetY(0.84)
  #tex2.SetTextColor(2),
  tex2.SetTextSizePixels(44)
  tex2.SetTextFont(42) #,   tex2.SetTextSize(0.2), tex2.SetTextSizePixels(24)
  #tex2.SetTextColor(2),   tex2.SetTextFont(42),   tex2.SetTextSize(0.05), tex2.SetTextSizePixels(24)
  return tex2


def addText(text,x,y):
  title  = TLatex(-20.,50.,text)
  title.SetNDC(),        title.SetTextAlign(12)
  title.SetX(x),      title.SetY(y)
  title.SetTextSizePixels(34)
  title.SetTextFont(62)#, title.SetTextSize(0.05),  title.SetTextSizePixels(24)
  #title.SetTextFont(42), title.SetTextSize(0.1),  title.SetTextSizePixels(24)
  return title

def getEtch(cen,error,y,ey):
  line = TLine(cen-error,y-ey,cen-error,y+ey)
  ci = TColor.GetColor("#FF0000")
  line.SetLineColor(ci)
  line.SetLineWidth(2)
  #line.SetLineStyle(2)
  line2 = TLine(cen+error,y-ey,cen+error,y+ey)
  line2.SetLineColor(ci)
  line2.SetLineWidth(2)
  #line2.SetLineStyle(2)

  return line,line2

def getError(num,denum):
  h1 = TH1D("h1","",1,0,10)
  h2 = TH1D("h2","",1,0,10)
  h1.Sumw2()
  h2.Sumw2()
#ttbbF': 18594.0, 'ttbb': 8194.0,ttbb': 2236.0,
  for i in range(int(num)):
    h1.Fill(1)
  for i in range(int(denum)):
    h2.Fill(1)
  h1.Divide(h2)
  #h1.Draw()
  #print h1.GetBinContent(1)
  #print h1.GetBinError(1)
  return h1.GetBinError(1)


def drawMCSample(cen,err,yc):
  x=[cen]
  y=[yc]
  ex=[err*cen]
  ey=[0.0]

  from array import array
  xx = array("d", x)
  exx = array("d", ex)
  yy = array("d", y)
  eyy = array("d", ey)

  gr =TGraphErrors(len(xx),xx,yy,exx,eyy)
  gr.SetLineColor(kRed), gr.SetLineWidth(2)
  gr.SetMarkerColor(kRed), gr.SetMarkerStyle(20)
  #gr.Draw("LP")
  l1,l2 =getEtch(x[0],ex[0],y[0],0.025)
  #l1.Draw(), l2.Draw()
  return gr,l1,l2

def drawMarker(cen,yc,color,marker):
  x=[cen]
  y=[yc]

  from array import array
  xx = array("d", x)
  yy = array("d", y)

  gr =TGraph(len(xx),xx,yy)
  gr.SetLineColor(color), gr.SetLineWidth(1)
  gr.SetMarkerColor(color), gr.SetMarkerStyle(marker)
  gr.SetMarkerSize(1)
  #gr.Draw("LP")
  #l1,l2 =getEtch(x[0],ex[0],y[0],0.025)
  #l1.Draw(), l2.Draw()
  return gr #,l1,l2



def drawFitResult(cen,err,color_):
  line = TLine(cen,0,cen,1)
  ci = TColor.GetColor("#000000")
  line.SetLineColor(ci)
  line.SetLineWidth(2)
  line.SetLineStyle(2)
  #box = TBox(cen-cen*err,0,cen+cen*err,1)
  box = TBox(cen-err,0,cen+err,1)
  ci = TColor.GetColor(color_)
  #ci = TColor.GetColor("#d0efd0")
  box.SetFillColor(ci)
  #box.Draw()
  #line.Draw()
  return box,line


def drawCanvas(ttjjFSsim, ttjjFSfit,canvas):

  h1 = TH1D("cx"+canvas["Name"],"",canvas["N"],canvas["xmin"],canvas["xmax"])
  h1.GetYaxis().SetLabelSize(0)
  h1.GetYaxis().SetNdivisions(1)
  h1.GetXaxis().SetTitleFont(42)
  h1.GetXaxis().SetTitleSize(0.1)
  h1.GetXaxis().SetTitleOffset(0.6)
  #h1.GetXaxis().SetTitle("#sigma [pb] or ratio ")
  h1.GetXaxis().SetTitle(canvas["title"])
  h1.Draw()

  pt1,pt2=addLegendLumi(),addLegendPreliminary()
  pt1.Draw(), pt2.Draw()


  gr,l1,l2=drawMCSample(ttjjFSsim["cen"],ttjjFSsim["StatErr"],0.7)
  #box02,line02=drawMCSample(ttjjFSsim["cen"],ttjjFSsim["StatSysErr"],0.8,"#e0a3a3")
  #box02.Draw()
  gr.Draw("LP"),l1.Draw(),l2.Draw()
  #box01.Draw(), line01.Draw()


  box01,line01=drawFitResult(ttjjFSfit["cen"],ttjjFSfit["StatErr"],"#efd0d0")
  box02,line02=drawFitResult(ttjjFSfit["cen"],ttjjFSfit["StatSysErr"],"#e0a3a3")
  box02.Draw()
  box01.Draw(), line01.Draw()
  gr.Draw("LP"),l1.Draw(),l2.Draw()
  h1.Draw("same")

  ttjjFStext = ttjjFSfit["title"]
  ttjjFS=addText(ttjjFStext,0.7,0.8)
  ttjjFS.Draw()
  ttjjFS2text = str(int(ttjjFSfit["cen"]))+" #pm "+str(int(ttjjFSfit["StatErr"] ))+" #pm "+str(int(ttjjFSfit["SysErr"] ))+" pb"
  ttjjFS2=addText( ttjjFS2text,0.5,0.5)
  #ttjjFS2.Draw()

  return [h1, gr, l1,l2,],ttjjFS,ttjjFS2,line01,box01,box02,gr


##############################
gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()
gStyle.SetCanvasDefH(600)
gStyle.SetCanvasDefW(1000)
gStyle.SetPadTickX(0)
gStyle.SetPadTickY(0)


gStyle.SetPadTopMargin(0.09);
gStyle.SetPadLeftMargin(0.00);
gStyle.SetPadRightMargin(0.00);
gStyle.SetPadBottomMargin(0.15);

from math import sqrt
ttjjAccSysErr = sqrt(0.0013**2+  0.021**2)
ttjjEffSysErr = sqrt(0.022**2 + 0.12**2)
ttjjSysErr = sqrt(0.0013**2+  0.021**2 + 0.022**2 + 0.12**2  )
ttjjStatErr = sqrt(POW["nom"]["statAcc_ttjj"]**2+POW["nom"]["statEff_ttjj"]**2)
ttjjFSsim = {"cen":POW["nom"]["ttjjFSCX"]   , "StatErr":ttjjStatErr  ,"SysErr":ttjjSysErr, "StatSysErr":ttjjStatErr  }

ttjjFSfit = {"cen":176, "StatErr":5, "SysErr":33,"StatSysErr":sqrt(5**2+33**2), "title":"t#bar{t}jj" }
ttjjCanvas = {"can":"c1","N":9,"xmin":110,"xmax":310,"title":"#sigma [pb]","Name":"ttjj" } 

c1 = TCanvas("c1","",800,400)
c1.Divide(4,1)
c1.cd(2)
ttjjCanvas1,ttjj1,ttjj2,line01,box01,box02,gr1 = drawCanvas(ttjjFSsim,ttjjFSfit,ttjjCanvas)


ttjjAMC = drawMarker(AMC["nom"]["ttjjFSCX"],0.5,kBlue,21)
ttjjAMC.Draw("P")
ttjjMG5 = drawMarker(MG5["nom"]["ttjjFSCX"],0.3,kGreen,22)
ttjjMG5.Draw("P")


ttbbAccSysErr =sqrt(0.11**2 + 0.77**2 )
ttbbEffSysErr =sqrt(2.3**2 + 15.**2 )
ttbbSysErr =sqrt( 0.11**2 + 0.77**2 + 2.3**2 + 15.**2 )
ttbbStatErr = sqrt(POW["nom"]["statAcc_ttbb"]**2+POW["nom"]["statEff_ttbb"]**2)
ttbbFSsim = {"cen":POW["nom"]["ttbbFSCX"]   , "StatErr":ttbbStatErr  ,"SysErr":ttbbSysErr, "StatSysErr":ttbbStatErr  }

#ttbbFSfit = {"cen":3.86, "StatErr":0.55, "SysErr":1.29, "StatSysErr":sqrt(0.55**2+1.29**2), "title":"t#bar{t}b#bar{b}" }
ttbbFSfit = {"cen":3.86, "StatErr":0.55, "SysErr":1.32, "StatSysErr":sqrt(0.55**2+1.32**2), "title":"t#bar{t}b#bar{b}" }
ttbbCanvas = {"can":"c2","N":7,"xmin":0.5,"xmax":9.5,"title":"#sigma [pb]","Name":"ttbb" } 

c1.cd(1)
ttbbCanvas2,ttbb1,ttbb2,line11,box11,box12,gr2 = drawCanvas(ttbbFSsim,ttbbFSfit,ttbbCanvas)
ttbbAMC = drawMarker(AMC["nom"]["ttbbFSCX"],0.5,kBlue,21)
ttbbAMC.Draw("P")
ttbbMG5 = drawMarker(MG5["nom"]["ttbbFSCX"],0.3,kGreen,22)
ttbbMG5.Draw("P")



rAccSysErr = ttjjAccSysErr/ttbbAccSysErr
rEffSysErr = ttjjEffSysErr/ttbbEffSysErr
rSysErr = rAccSysErr*rEffSysErr
rStatErr = getError(POW["nom"]["ttbbFS"],POW["nom"]["ttjjFS"] )
rFSsim = {"cen":POW["nom"]["ttbbFS"]/POW["nom"]["ttjjFS"]*100.   , "StatErr":rStatErr*100.  ,"SysErr":rSysErr*100., "StatSysErr":rStatErr*100.  }

rFSfit = {"cen":2.2, "StatErr":0.3, "SysErr":0.6, "StatSysErr":sqrt(0.3**2+0.6**2), "title":"#frac{t#bar{t}b#bar{b}}{t#bar{t}jj} " }
rCanvas = {"can":"c2","N":5,"xmin":0.2,"xmax":4.5,"title":"ratio as t#bar{t}b#bar{b}/t#bar{t}jj [%]","Name":"r" } 

c1.cd(3)
rCanvas2,r1,r2,line21,box21,box22,gr3 = drawCanvas(rFSsim,rFSfit,rCanvas)
rAMC = drawMarker(AMC["nom"]["ttbbFS"]/AMC["nom"]["ttjjFS"]*100.,0.5,kBlue,21)
rAMC.Draw("P")
rMG5 = drawMarker(MG5["nom"]["ttbbFS"]/MG5["nom"]["ttjjFS"]*100.,0.3,kGreen,22)
rMG5.Draw("P")



c1.cd(4)
y1=0.6
y2=0.5
y3=0.2
height=0.1

leg1=make_legend(0.1,y1,0.8,y1+height)
leg1.AddEntry(line01, "Measurement ", "l")

leg2=make_legend(0.1,y2,0.45+0.3,y2+height)
leg2.AddEntry(box21, "Stat.", "f")
leg3=make_legend(0.45,y2,0.88+0.2,y2+height)
leg3.AddEntry(box22, "Sys.", "f")

leg4=make_legend(0.1,y3,0.88,y3+height*3)
leg4.AddEntry(gr1, "POWHEG", "p")
leg4.AddEntry(ttjjAMC, "aMC@NLO", "p")
leg4.AddEntry(ttjjMG5, "Madgraph", "p")

leg1.Draw()
leg2.Draw()
leg3.Draw()
leg4.Draw()

cmslegend=addLegendPreliminary()
cmslegend.Draw()
lumilegend=addLegendLumi()
lumilegend.Draw()

c1.cd(1).RedrawAxis()
c1.cd(2).RedrawAxis()
c1.cd(3).RedrawAxis()
c1.cd(4).RedrawAxis()


c1.Print("ttbb_dilepton_13TeV_summary.C")
c1.Print("ttbb_dilepton_13TeV_summary.eps")
