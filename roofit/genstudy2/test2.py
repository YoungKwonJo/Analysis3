from ROOT import *

from q2Weight_Run  import POW2, dwPOW2, upPOW2, AMC2, MG52, POHP2 

def addLegendLumi():#lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"2.3 fb^{-1} (13 TeV)")
  title.SetNDC(),        title.SetTextAlign(12)
  title.SetX(0.67),      title.SetY(0.94)
  title.SetTextFont(42), title.SetTextSize(0.059)#,  title.SetTextSizePixels(24)
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


def addText(text,x,y):
  title  = TLatex(-20.,50.,text)
  title.SetNDC(),        title.SetTextAlign(12)
  title.SetX(x),      title.SetY(y)
  title.SetTextFont(42)#, title.SetTextSize(0.05),  title.SetTextSizePixels(24)
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

def drawCXWithError(cen,err,yc):
  x=[cen]
  y=[yc]
  ex=[err]
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

def drawSMbar(cen,err,color_):
  line = TLine(cen,0,cen,1)
  ci = TColor.GetColor("#000000")
  line.SetLineColor(ci)
  line.SetLineWidth(2)
  line.SetLineStyle(2)
  box = TBox(cen-cen*err,0,cen+cen*err,1)
  ci = TColor.GetColor(color_)
  #ci = TColor.GetColor("#d0efd0")
  box.SetFillColor(ci)
  #box.Draw()
  #line.Draw()
  return box,line


gROOT.SetStyle("Plain")
gStyle.SetOptFit(1000)
gStyle.SetOptStat("emruo")
gStyle.SetOptStat(kFALSE)

gROOT.ProcessLine(".L tdrStyle.C")
setTDRStyle()
gStyle.SetCanvasDefH(600)
gStyle.SetCanvasDefW(800)
gStyle.SetPadTickX(0)
gStyle.SetPadTickY(0)


gStyle.SetPadTopMargin(0.09);
gStyle.SetPadLeftMargin(0.05);
gStyle.SetPadRightMargin(0.05);


c1 = TCanvas()

h1 = TH1D("cx","",50,0,600)
#h1 = TH1D("cx","",50,0,10)
#h1 = TH1D("cx","",50,0,0.08)
h1.GetYaxis().SetLabelSize(0)
h1.GetYaxis().SetNdivisions(1)
#h1.GetXaxis().SetTitle("#sigma [pb] or ratio ")
h1.GetXaxis().SetTitle("#sigma [pb] ")
h1.Draw()

pt1,pt2=addLegendLumi(),addLegendPreliminary()
pt1.Draw(), pt2.Draw()

##########################
##########################
##########################
ttjjFSsim2 = {"cen":257, "err":26 }
from math import sqrt

ttjjAccSysErr = sqrt(0.0013**2+  0.021**2)
ttjjEffSysErr = sqrt(0.022**2 + 0.12**2)
ttjjSysErr = sqrt(0.0013**2+  0.021**2 + 0.022**2 + 0.12**2  )
ttjjStatErr = sqrt(POW2["nom"]["statAcc_ttjj"]**2+POW2["nom"]["statEff_ttjj"]**2)
ttjjStatSysErr = sqrt(POW2["nom"]["statAcc_ttjj"]**2+POW2["nom"]["statEff_ttjj"]**2 + 0.0013**2+  0.021**2 + 0.022**2 + 0.12**2 )
k= 0.842498214663

ttjjFSsim = {"cen":POW2["nom"]["ttjjFSCX"]   , "StatErr":ttjjStatErr  ,"SysErr":ttjjSysErr, "StatSysErr":ttjjStatErr  }
ttjjFSsim3 = {"cen":POW2["nom"]["ttjjFSCX"]*k, "StatErr":ttjjStatErr  ,"SysErr":ttjjSysErr, "StatSysErr":ttjjStatErr  }
print ttjjFSsim
print ttjjFSsim2

ttjjFSfit = {"cen":176, "stat":5, "syst":33 }

box01,line01=drawSMbar(ttjjFSsim["cen"],ttjjFSsim["StatErr"],"#efd0d0")
box02,line02=drawSMbar(ttjjFSsim["cen"],ttjjFSsim["StatSysErr"],"#e0a3a3")
box02.Draw()
box01.Draw(), line01.Draw()


box11,line11=drawSMbar(ttjjFSsim3["cen"],ttjjFSsim3["StatErr"],"#d0efd0")
box12,line12=drawSMbar(ttjjFSsim3["cen"],ttjjFSsim3["StatSysErr"],"#a3e0a3")
box12.Draw()
box11.Draw(), line11.Draw()


gr,l1,l2=drawCXWithError(ttjjFSfit["cen"],ttjjFSfit["stat"],0.8)
gr2,l3,l4=drawCXWithError(ttjjFSfit["cen"],ttjjFSfit["syst"],0.8)
gr.Draw("LP"),l1.Draw(),l2.Draw()
gr2.Draw("LP"),l3.Draw(),l4.Draw()


ttjjFS=addText("t#bar{t}jj_{full phase space}",0.1,0.8)
ttjjFS.Draw()
ttjjFS2=addText("176 #pm 5 #pm 33 pb",0.5,0.8)
ttjjFS2.Draw()

ttjjFS22text = str(int(ttjjFSsim["cen"]))+" #pm "+str(int(ttjjFSsim["cen"]*ttjjFSsim["StatErr"] ))+" #pm "+str(int(ttjjFSsim["cen"]*ttjjFSsim["SysErr"] ))+" pb"
ttjjFS22=addText( ttjjFS22text,0.5,0.6)
ttjjFS22.SetTextColor(TColor.GetColor("#e0a3a3") )
ttjjFS22.Draw()

ttjjFS23text = str(int(ttjjFSsim3["cen"]))+" #pm "+str(int(ttjjFSsim3["cen"]*ttjjFSsim3["StatErr"] ))+" #pm "+str(int(ttjjFSsim3["cen"]*ttjjFSsim3["SysErr"] ))+" pb"
ttjjFS23=addText(ttjjFS23text+" within k = 0.84" ,0.5,0.4)
ttjjFS23.SetTextColor(TColor.GetColor("#a3e0a3") )
ttjjFS23.Draw()





"""
##########################
##########################
##########################
ttbbFSsim = {"cen":3.17, "err":0.41 }
ttbbFSfit = {"cen":3.86, "stat":0.55, "syst":1.32 }

boxBB,lineBB=drawSMbar(ttbbFSsim["cen"],ttbbFSsim["err"])
boxBB.Draw(), lineBB.Draw()

grBB,l1BB,l2BB=drawCXWithError(ttbbFSfit["cen"],ttbbFSfit["stat"],0.5)
gr2BB,l3BB,l4BB=drawCXWithError(ttbbFSfit["cen"],ttbbFSfit["syst"],0.5)
grBB.Draw("LP"),l1BB.Draw(),l2BB.Draw()
gr2BB.Draw("LP"),l3BB.Draw(),l4BB.Draw()

ttbbFS=addText("t#bar{t}b#bar{b}_{full phase space}",0.1,0.55)
ttbbFS.Draw()
ttbbFS2=addText("3.86 #pm 0.55 #pm 1.32 pb",0.55,0.55)
ttbbFS2.Draw()


##########################
##########################
##########################
rFSsim = {"cen":0.012, "err":0.0001 }
rFSfit = {"cen":0.022, "stat":0.003, "syst":0.006 }

boxR,lineR=drawSMbar(rFSsim["cen"],rFSsim["err"])
boxR.Draw(), lineR.Draw()

grR,l1R,l2R=drawCXWithError(rFSfit["cen"],rFSfit["stat"],0.25)
gr2R,l3R,l4R=drawCXWithError(rFSfit["cen"],rFSfit["syst"],0.25)
grR.Draw("LP"),l1R.Draw(),l2R.Draw()
gr2R.Draw("LP"),l3R.Draw(),l4R.Draw()

rFS=addText("#frac{t#bar{t}b#bar{b}}{t#bar{t}jj}_{full phase space}",0.1,0.30)
rFS.Draw()
rFS2=addText("0.022 #pm 0.003 #pm 0.006 pb",0.55,0.30)
rFS2.Draw()
"""

