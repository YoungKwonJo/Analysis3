from ROOT import *
import copy
from array import array
from math import sqrt

################
log = False
#log = True
mainlumi=2170.
ci = 920

###################################################
DYsfmva = {
 "kMM" : 0.564035113137,
 "kEE" : 0.443234816729,
  # EE MM
 "S2":(1.0,1.0),
 "S3":(0.969986566176,0.916420581219),
 "S4":(1.04666179925,0.950433756095),
 "S5":(1.04666179925,0.950433756095),
 "S6":(1.04666179925,0.950433756095)
}
DYsf = {
 "kMM" : 0.600653370713,
 "kEE" : 0.416213430557,
  # EE MM
 "S2":(1.0,1.0),
 "S3":(0.992418427487,0.916387197892),
 "S4":(1.06777384456,0.949934750951),
 "S5":(1.06777384456,0.949934750951),
 "S6":(1.06777384456,0.949934750951)
# "S5":(1.17764007675,0.894244897143),
# "S6":(,)
}



def drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out,
                       rd_ee_in, rd_mm_in, rd_em_in,kMM,kEE):    
    #kMM = sqrt(rd_mm_in/rd_ee_in)/2.
    #kEE = sqrt(rd_ee_in/rd_mm_in)/2.
    #kMM=0.592512945972
    #kEE=0.421931709171
    #kMM=0.590181280767
    #kEE=0.423598660525
    print "    kMM="+str(kMM)
    print "    kEE="+str(kEE)

    rMC_mm = mc_mm_out/mc_mm_in
    rMC_ee = mc_ee_out/mc_ee_in
    print "Rout/in MM: "+str(rMC_mm)+", EE:"+str(rMC_ee)
    nOutEst_mm = rMC_mm*(rd_mm_in - rd_em_in*kMM)
    nOutEst_ee = rMC_ee*(rd_ee_in - rd_em_in*kEE)
    print "SF MM: "+str(nOutEst_mm/mc_mm_out)+", EE:"+str(nOutEst_ee/mc_ee_out)
    return nOutEst_ee/mc_ee_out,nOutEst_mm/mc_mm_out

###################################################
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

def addLegendLumi(lumi):
  #lumi2 = str(round(lumi/100)/10)
  title  = TLatex(-20.,50.,"CMS #sqrt{s} = 13TeV, L = 2.1 fb^{-1}")
  title.SetNDC()
  title.SetTextAlign(12)
  title.SetX(0.20)
  title.SetY(0.83)
  title.SetTextFont(42)
  title.SetTextSize(0.05)
  title.SetTextSizePixels(24)
  title.Draw()

  return title

def addLegendCMS():
  #tex2 = TLatex(0.3715952,0.9146667,"Preliminary")
  tex2 = TLatex(-20.,50.,"Preliminary")
  tex2.SetNDC()
  tex2.SetTextAlign(12)
  tex2.SetX(0.25)
  tex2.SetY(0.93)
  tex2.SetTextColor(2)
  tex2.SetTextFont(42)
  tex2.SetTextSize(0.05)
  tex2.SetTextSizePixels(24)
  tex2.Draw()

  return tex2

def addDecayMode(ll):
  ll2="l^{#mp}l^{#pm} channel"
  if ll.find("em")>-1 : ll2="e^{#mp}#mu^{#pm} channel"
  if ll.find("mm")>-1 : ll2="#mu^{#mp}#mu^{#pm} channel"
  if ll.find("ee")>-1 : ll2="e^{#mp}e^{#pm} channel"

  chtitle = TLatex(-20.,50.,ll2)
  chtitle.SetNDC()
  chtitle.SetTextAlign(12)
  chtitle.SetX(0.20)
  chtitle.SetY(0.75)
  chtitle.SetTextFont(42)
  chtitle.SetTextSize(0.05)
  chtitle.SetTextSizePixels(24)

  return chtitle


#########################
def plotTH2F(filename,mon,step,mcsamples):
  f = TFile.Open(filename,"read")
  n=len(mcsamples)
  gStyle.SetOptStat(0)
  c1 = TCanvas( 'c2', '', 500*3, 500*2 ) 
  c1.Divide(3,2)
  legs = []
  #pts  = []
  for i,mc in enumerate(mcsamples):
    c1.cd(i+1)
    histname = "h2_"+mc['name']+"_"+mon+"_"+step+"_Sumw2"
    h1 = f.Get(histname)
    if type(h1) is not TH2F :  
      return
    h1.SetTitle("")
    ci = TColor.GetColor(mc["ColorLabel"]['color']);
    h1.SetLineColor(ci)
    h1.Draw("colz")

    leg = make_legend(0.5,0.91, 0.75,0.99)
    leg.AddEntry(h1, ("%s : "%mc["ColorLabel"]['label']) + ("%.0f"%h1.Integral()), "l");
    legs.append(copy.deepcopy(leg))
    legs[i].Draw()
  output = "plots/eps/TH2_"+mon+"_"+step+weight+".eps"
  output2 = "plots/png/TH2_"+mon+"_"+step+weight+".png"
  c1.Print(output)
  c1.Print(output2)
  f.Close()
  c1.Close()


#########################
#########################
#########################
#########################
#########################
#########################
#########################
#########################
def myCanvas(name):
  c1 = TCanvas( name, '',1)#, 500, 500 )
  return c1
def myPad1(name):
  pad1 = TPad(name, "",0,0.3,1,1)
  pad1.SetPad(0.01, 0.23, 0.99, 0.99)
  pad1.SetTopMargin(0.1)
  pad1.SetRightMargin(0.04)

  return pad1

def myPad2(name):
  pad2 = TPad(name, "",0,0,1,0.3)
  pad2.SetPad(0.01, 0.02, 0.99, 0.3)
  #gStyle.SetGridWidth(0.5)
  gStyle.SetGridWidth(1)
  gStyle.SetGridColor(14)
  pad2.SetGridx()
  pad2.SetGridy()
  pad2.SetTopMargin(0.05)
  pad2.SetBottomMargin(0.4)
  pad2.SetRightMargin(0.04)

  return pad2

#################
def myMCHistSet(hdata):
  hdata.GetYaxis().SetTitle("Events")
  hdata.GetYaxis().SetTitleOffset(1.2)
  hdata.GetYaxis().SetTitleSize(0.07)
  hdata.GetYaxis().SetLabelSize(0.055)
  hdata.GetYaxis().SetNdivisions(607)
  #hdata.GetYaxis().SetLabelSize(0.05)
  #hYaxis = hdata.GetYaxis()
  #hYaxis.SetMaxDigits(3)
  hdata.GetXaxis().SetLabelSize(0.0)
  hdata.GetXaxis().SetTitle("")


def myDataHistSet(hdata):
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

  return hdata

def myAmcNLOHistSet(hdata):
  hdata.SetLineColor(6)
  hdata.SetLineStyle(2)
  hdata.SetFillColor(0)

def myMG5HistSet(hdata):
  hdata.SetLineColor(8)
  hdata.SetLineStyle(4)
  hdata.SetFillColor(0)

def myAmcNLORatioSet(hdata):
  hdata.SetLineColor(6)
  hdata.SetLineStyle(2)
  hdata.SetLineWidth(2)
  hdata.SetFillColor(0)

def myMG5RatioSet(hdata):
  hdata.SetLineColor(8)
  hdata.SetLineStyle(4)
  hdata.SetLineWidth(2)
  hdata.SetFillColor(0)


def myRatio(hdata):
  Ratio = hdata.Clone("ratio")

  Ratio.SetMarkerStyle(20)
  Ratio.SetMarkerSize(0.5)
  Ratio.SetMarkerColor(1)
  Ratio.SetLineColor(1)
  Ratio.SetLineWidth(1)
  Ratio.SetMaximum(2)
  Ratio.SetMinimum(0)
  Ratio.SetTitle("")
  
  Ratio.GetYaxis().SetTitle("Obs/Exp")
  Ratio.GetYaxis().CenterTitle()
  Ratio.GetYaxis().SetTitleOffset(0.45)
  Ratio.GetYaxis().SetTitleSize(0.16)
  Ratio.GetYaxis().SetLabelSize(0.15)
  Ratio.GetYaxis().SetNdivisions(402)
  Ratio.GetXaxis().SetNdivisions(509)
  Ratio.GetXaxis().SetTitleOffset(1.1)
  Ratio.GetXaxis().SetLabelSize(0.20)
  Ratio.GetXaxis().SetTitleSize(0.16)
  
  Ratio.SetMinimum(0.6)
  Ratio.SetMaximum(1.4)

  return Ratio

def myRatioSyst(hdata):
  RatioSyst = hdata.Clone("ratioSyst")

  for b_r in range(1,RatioSyst.GetNbinsX()+1):
    RatioSyst.SetBinContent(b_r,1.0)

  thegraphRatioSyst = TGraphErrors(RatioSyst)
  thegraphRatioSyst.SetFillStyle(1001)
  thegraphRatioSyst.SetFillColor(ci)
  thegraphRatioSyst.SetName("thegraphRatioSyst")

  return thegraphRatioSyst

def myHist2TGraphError(hist1):
  xx=[]
  xxer=[]
  yy=[]
  yyer=[]
  for i in range(0, hist1.GetNbinsX()+2 ):
    yy.append(  float(hist1.GetBinContent(i)))
    yyer.append(float(hist1.GetBinError(i)))
    xx.append(  float(hist1.GetBinCenter(i)))
    xxer.append(float(hist1.GetBinWidth(i)/2))

  x   = array("d",xx)
  xer = array("d",xxer)
  y   = array("d",yy)
  yer = array("d",yyer)
  gr = TGraphErrors(len(x), x,y,xer,yer)
#####
  #gr.SetName("gr")
  gr.SetFillStyle(1001)
  gr.SetFillColor(ci)
  gr.SetLineColor(ci)
###	#
  #gr.SetFillColor(kBlack);
  ##gr.SetFillStyle(3144);
  ##gr.SetFillStyle(3005);
  ##gr.SetFillStyle(3244);
  #gr.SetFillStyle(3444);

  return gr
#####################


#####################
def drellYanEstimationRun(f,step): #,mcsamples,datasamples):
 
  step=step.replace("mm_","")
  step=step.replace("ee_","")
  step=step.replace("em_","")
  mcs = ["DYJets","DYJets10"]
  #mcxs = [6025.2,23914.65]
  mcxs = [6025.2,18610.0]
  datas = ["1","2"]

  hrdeein_s2 = TH1D("rd_ee_in_s2","",60,0,300)
  hrdmmin_s2 = TH1D("rd_mm_in_s2","",60,0,300)

  hmceein = TH1D("mc_ee_in","",60,0,300)
  hmcmmin = TH1D("mc_mm_in","",60,0,300)
  hmcemin = TH1D("mc_em_in","",60,0,300)

  hmceeout = TH1D("mc_ee_out","",60,0,300)
  hmcmmout = TH1D("mc_mm_out","",60,0,300)

  hrdeein = TH1D("rd_ee_in","",60,0,300)
  hrdmmin = TH1D("rd_mm_in","",60,0,300)
  hrdemin = TH1D("rd_em_in","",60,0,300)


  for i,mc in enumerate(mcs) :
    inee =  mc+"/CEN/"+"/h1_"+mc+"_ZMass_ee_"+step+"_in"
    h1=f.Get(inee).Clone("hhhh_ee_"+mc) 
    h1.Scale(mainlumi*mcxs[i])
    hmceein.Add(h1)

    inmm = mc+"/CEN/"+"/h1_"+mc+"_ZMass_mm_"+step+"_in"
    h2=f.Get(inmm).Clone("hhhh_mm_"+mc) 
    h2.Scale(mainlumi*mcxs[i])
    hmcmmin.Add(h2)

    inem = mc+"/CEN/"+"/h1_"+mc+"_ZMass_em_"+step+"_in"
    h3=f.Get(inem).Clone("hhhh_em_"+mc) 
    h3.Scale(mainlumi*mcxs[i])
    hmcemin.Add(h3)

    outee = mc+"/CEN/"+"/h1_"+mc+"_ZMass_ee_"+step+"_out"
    h11=f.Get(outee).Clone("hhhh_ee_"+mc) 
    h11.Scale(mainlumi*mcxs[i])
    hmceeout.Add(h11)

    outmm = mc+"/CEN/"+"/h1_"+mc+"_ZMass_mm_"+step+"_out"
    h22=f.Get(outmm).Clone("hhhh_mm_"+mc) 
    h22.Scale(mainlumi*mcxs[i])
    hmcmmout.Add(h22)

  for data in datas :
    eein = "ElEl"+data+"/CEN/"+"/h1_ElEl"+data+"_ZMass_ee_"+step+"_in"
    h1=f.Get(eein).Clone("hhhh_rd_ee"+data)
    hrdeein.Add(h1)

    mmin = "MuMu"+data+"/CEN/"+"/h1_MuMu"+data+"_ZMass_mm_"+step+"_in"
    h2=f.Get(mmin).Clone("hhhh_rd_mm"+data)
    hrdmmin.Add(h2)

    emin = "MuEl"+data+"/CEN/"+"/h1_MuEl"+data+"_ZMass_em_"+step+"_in"
    h3=f.Get(emin).Clone("hhhh_rd_em"+data)
    hrdemin.Add(h3)

    eein2 = "ElEl"+data+"/CEN/"+"/h1_ElEl"+data+"_ZMass_ee_S2_in"
    h12=f.Get(eein2).Clone("hhhh_rd_ee_s2"+data)
    hrdeein_s2.Add(h12)

    mmin2 = "MuMu"+data+"/CEN/"+"/h1_MuMu"+data+"_ZMass_mm_S2_in"
    h22=f.Get(mmin2).Clone("hhhh_rd_mm_s2"+data)
    hrdmmin_s2.Add(h22)


  mc_ee_in   = hmceein.Integral()
  mc_ee_out  = hmceeout.Integral()
  mc_mm_in   = hmcmmin.Integral()
  mc_mm_out  = hmcmmout.Integral()
  rd_ee_in   = hrdeein.Integral()
  rd_mm_in   = hrdmmin.Integral()
  rd_em_in   = hrdemin.Integral()
  rd_ee_in_s2   = hrdeein_s2.Integral()
  rd_mm_in_s2   = hrdmmin_s2.Integral()
  kMM = sqrt(rd_mm_in_s2/rd_ee_in_s2)/2.
  kEE = sqrt(rd_ee_in_s2/rd_mm_in_s2)/2.
 
  return drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out, rd_ee_in, rd_mm_in, rd_em_in,kMM,kEE)
 
def singleplotStack2(filename,mon,weight,step,mcsamples,datasamples,useReturn):
  f = TFile.Open(filename,"read")
  singleplotStack(f,mon,weight,step,mcsamples,datasamples,useReturn)
  f.Close()

def singleplotStack(f,mon1,weight,step,mcsamples,datasamples,useReturn):

  #dyest = drellYanEstimationRun(f,step)
  dyest = DYsf[step[3:5]]
  mon = mon1["name"]
  channel = step[0:2]
  step2 = step[3:]

  #f = TFile.Open(filename,"read")
  canvasname = mon+step
  c1 = myCanvas(canvasname)
  #c1 = TCanvas( 'c1', '', 500, 500 )
  if log : print mon+step
  #gStyle.SetOptFit(1)
  #gStyle.SetOptStat(0)
###############
  c1.Divide(1,2)
  
  #Plot Pad
  pad1 = myPad1(canvasname+"pad1")
  #Ratio Pad
  pad2 = myPad2(canvasname+"pad2")
##############
  pad1.Draw()
  pad1.cd()

  legx1 = 0.8
  wid=0.12
  legx2 = 0.67
  leg  = make_legend(legx1,0.64, legx1+wid,0.88)
  leg2 = make_legend(legx2,0.68, legx2+wid,0.88)
  leg3 = make_legend(legx1,0.54, legx1+wid,0.63)
  lumi = mainlumi

  hs = THStack("hs","")
  #POWttbb/CEN/h1_POWttbb_MET_mm_S5_out
  hmctotName = mcsamples[0]['name']+"/"+weight+"/h1_"+mcsamples[0]['name']+"_"+mon+"_"+step+"_"+weight
  #if log : print "hmcTotal: "+hmctotName
  hmctot = f.Get(hmctotName).Clone("hmctot")
  hmcmerge = f.Get(hmctotName).Clone("hmcmerge")
  hmcSig = f.Get(hmctotName).Clone("hmcSig")

  hmctot.Reset()
  hmcmerge.Reset()
  hmcSig.Reset()

  hmcAmcNLO = hmctot.Clone("hmcAmcNLO")
  hmcMG5   = hmctot.Clone("hmcMG5")
  hdata = hmctot.Clone("hdata")
  myMCHistSet(hmctot)
  myMCHistSet(hmcmerge)
  myDataHistSet(hdata)

  isStat = mon.find("Stat")>-1
  if isStat : 
    print "Stat: step: "+step

  for i,mc in enumerate(mcsamples):
    isMC = mc["ColorLabel"]['label'].find("DATA")==-1
    if not isMC: continue

    histnameS = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_"+step+"_"+weight
    h2 = f.Get(histnameS).Clone("h"+histnameS)
    if type(h2) is not TH1D :
      continue
    h2.GetYaxis().SetTitle("Events")

    h2.AddBinContent(h2.GetNbinsX(),h2.GetBinContent(h2.GetNbinsX()+1))
    #if h2.Integral()>0 :  h2.Scale(mc['cx']/Ntot*lumi)
    if h2.Integral()>0 :  h2.Scale(mc['cx']*lumi)
    #if h2.Integral()>0 :  h2.Scale(lumi)

    ###############
    isDY = mc['name'].find("DYJet")>-1
    if isDY and int(step[4:5])>1: 
      if step.find("ee")>-1:
        h2.Scale(dyest[0])
      if step.find("mm")>-1:
        h2.Scale(dyest[1])

    isTTH = mc['name'].find("ttH")>-1
    isPowheg = mc['name'].find("POW")>-1
    isAmcNLO = mc['name'].find("AMC")>-1
    isMG5 = mc['name'].find("MG5")>-1
    if not isPowheg and not isTTH and not isMG5:
      hmcAmcNLO.Add(h2)
      if isStat and isAmcNLO:
        if h2.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2.GetBinContent(1)*10)/10)+" \pm "+str(round(h2.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2.GetBinContent(1)))+" \pm "+str(round(h2.GetBinError(1)))+" $"
      if isAmcNLO:  continue
    if not isPowheg and not isTTH and not isAmcNLO:
      hmcMG5.Add(h2)
      if isStat and isMG5:
        if h2.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2.GetBinContent(1)*10)/10)+" \pm "+str(round(h2.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2.GetBinContent(1)))+" \pm "+str(round(h2.GetBinError(1)))+" $"
      if isMG5:  continue

    if not isTTH and not isMG5 and not isAmcNLO:
      hmctot.Add( h2 )
    hmcmerge.Add(h2)
    #hs.Add(h2)
    ci = TColor.GetColor(mc["ColorLabel"]['color']);

    selEvet=h2.Integral() 
    selEnts=h2.GetEntries()
    if log : print "mc:"+mc['file']+":"+str(round(selEvet))+", "+str(selEnts)
    isSameNext=False
    if i<len(mcsamples)-1 : isSameNext= mc["ColorLabel"]['label'] is mcsamples[i+1]["ColorLabel"]["label"]
    if  (not isSameNext) and isPowheg: 
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)
      label = ("%s"%mc["ColorLabel"]['label']) #+ (" %.0f"%(h3.Integral()) ).rjust(7)
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
      leg.AddEntry(h3, label, "f")
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and not isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)

      label = ("%s"%mc["ColorLabel"]['label']) #+ (" %.0f"%(h3.Integral()) ).rjust(7)
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      leg2.AddEntry(h3, label, "f")
      hs.Add(h3)
      #hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and  isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      #h3.SetLineColor(kBlack)
      hmcSig.Add(h3)
      hmcSig.SetLineColor(ci)
      hmcSig.SetTitle(mc["ColorLabel"]['label'])
#      label = ("%s"%mc['label']) + (" %.0f"%(hmcSig.Integral()) ).rjust(7)
#      leg2.AddEntry(hmcSig, label, "l")
      hmcmerge.Reset()

  hdata.Reset()
  for i,mc in enumerate(datasamples):
    histnameS = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_"+step+"_CEN"
    #histnameS = "h1_"+mc['name']+"_"+mon+"_"+step[0:5]
    channel = step[0:2]
    h1 = f.Get(histnameS).Clone("h"+histnameS)
    if type(h1) is not TH1D :
      continue
    h1.GetYaxis().SetTitle("Events")

    h1.AddBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX()+1))
    selEvet=h1.Integral() 
    selEnts=h1.GetEntries()
 
    checkDataChannel = (channel=="mm" and mc['name'].find("MuMu")>-1 ) or (channel=="ee" and mc['name'].find("ElEl")>-1 ) or (channel=="em" and mc['name'].find("MuEl")>-1 )
    if checkDataChannel : 
      hdata.Add(h1)
      if log : print "data:"+mc['file']+": "+str(round(selEvet))+", "+str(selEnts)
################################
  scale = hmctot.GetMaximum()
  minimum = 0.05

  h1data = hdata.Clone("h1data")
  h2data = myDataHistSet(h1data)

  maxY=0.
  for i in range(int(h1data.GetNbinsX()*0.7)+1, h1data.GetNbinsX()+2):
     if maxY<h1data.GetBinContent(i): maxY=h1data.GetBinContent(i)

  h2data.SetMaximum(maxY*10000)

  if maxY*10000 < scale*140 : h2data.SetMaximum(scale*140)
  #h2data.SetMaximum(scale*40)
  h2data.SetMinimum(minimum)
  labeltot = ("MC Total") #+ (" %.0f"%hmctot.Integral()).rjust(8)
  #leg2.AddEntry(hmctot,labeltot,"")
  if isStat:
    if hmctot.GetBinContent(1)<100 : print " Stat: "+("MC Total").rjust(10)+" & $ "+str(round(hmctot.GetBinContent(1)*10)/10)+" \pm "+str(round(hmctot.GetBinError(1)*10)/10)+" $"
    else                           : print " Stat: "+("MC Total").rjust(10)+" & $ "+str(round(hmctot.GetBinContent(1)))+" \pm "+str(round(hmctot.GetBinError(1)))+" $"
 
  label = ("%s"%hmcSig.GetTitle()) #+ (" %.0f"%(hmcSig.Integral()) ).rjust(7)
  if isStat and (hmcSig.Integral()>0):
    if hmcSig.GetBinContent(1)<100 : print " Stat: "+("tth").rjust(10)+" & $ "+str(round(hmcSig.GetBinContent(1)*10)/10)+" \pm "+str(round(hmcSig.GetBinError(1)*10)/10)+" $"
    else                           : print " Stat: "+("tth").rjust(10)+" & $ "+str(round(hmcSig.GetBinContent(1)))+" \pm "+str(round(hmcSig.GetBinError(1)))+" $"
 
  labeldata = ("DATA     ")# + (" %.0f"%h2data.Integral()).rjust(8)
  leg.AddEntry(h2data,labeldata,"p")
  if isStat :
    print " Stat: "+("DATA ").rjust(10)+" & $ "+str(round(h2data.GetBinContent(1)))+" $" # +" +- "+str(h2data.GetBinError(1))

#########################################
  h2data.GetYaxis().SetTitle("Events")
  h2data.GetXaxis().SetTitle("")
  h2data.Draw()
  gr = myHist2TGraphError(hmctot)
  hs.Draw("same,hist")
  #gr.Draw("same,2")
  #leg.AddEntry(gr,"Uncertainty","f")
  gr.Draw("e2SAME")
  myAmcNLOHistSet(hmcAmcNLO)
  #hmcAmcNLO.Draw("histoSAME")
  myMG5HistSet(hmcMG5)
  hmcMG5.Draw("histoSAME")
  #leg3.AddEntry(hmcAmcNLO,"MC@NLO","l")
  leg3.AddEntry(hmcMG5,"Madgraph","l")
  leg3.AddEntry(hmcSig, label, "l")

  hmcSig.Draw("same")
  h2data.Draw("same")
#  h2data.Draw("sameaxis")

  leg.Draw()
  leg2.Draw()
  leg3.Draw()
  pad1.SetLogy()
  pt = addLegendLumi(lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode(channel)
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  pad1.Modified()
  c1.cd()
###########################################
  if log :  print "pad1 step"
  #pad2 = TPad("pad2", "",0,0,1,0.3)
  pad2 = myPad2(canvasname+"pad2")

  if log :  print "pad2 step1"
  pad2.Draw()
  pad2.cd()
  hdataAMC=hdata.Clone("hdataAMC")
  hdataMG5=hdata.Clone("hdataMG5")
  hdata.Divide(hmctot)
  hdataAMC.Divide(hmcAmcNLO)
  hdataMG5.Divide(hmcMG5)
  myAmcNLORatioSet(hdataAMC)
  myMG5RatioSet(hdataMG5)

  hratio = myRatio(hdata)
  hratio.GetXaxis().SetTitle(mon1['unit'])
  hratio.Draw()
  hratiosyst = myRatioSyst(hdata)
  hratiosyst.Draw("e2")
  hratio.Draw("e1SAME")
  #hdataAMC.Draw("histSAME")
  hdataMG5.Draw("histSAME")
 
  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  Weight2=weight.replace("CEN","")  
  output = "plots/eps/TH1_"+mon+"_"+step2+channel+Weight2+".eps"
  output2 = "plots/png/TH1_"+mon+"_"+step2+channel+Weight2+".png"
  c1.Print(output)
  c1.Print(output2)

  #f.Close()
  #c1.Close()
  if useReturn : return c1,pad1,pad2,hs,gr,h2data,hdataMC,leg,leg2
  else : c1.Close() 
    
############################################
############################################
##################################################
##################################################
############################################
############################################
def singleplotStackLL2(filename,mon,weight,step,mcsamples,datasamples,useReturn):
  f = TFile.Open(filename,"read")
  singleplotStackLL(f,mon,weight,step,mcsamples,datasamples,useReturn)
  f.Close()

def singleplotStackLL(f,mon1,weight,step,mcsamples,datasamples,useReturn):

  #dyest = drellYanEstimationRun(f,step[0:2])
  dyest = DYsf[step[0:2]]
  print "step : "+step+":"+str(dyest)
  #f = TFile.Open(filename,"read")
  mon = mon1["name"]
  canvasname = mon+step
  c1 = myCanvas(canvasname)
  #c1 = TCanvas( 'c1', '', 500, 500 )
  if log : print mon+step
  #c1.Divide(1,2)

   #Plot Pad
  pad1 = myPad1(canvasname+"pad1")
  #Ratio Pad
  pad2 = myPad2(canvasname+"pad2")
##############
  pad1.Draw()
  pad1.cd() 

  legx1 = 0.8
  wid=0.12
  legx2 = 0.67
  leg  = make_legend(legx1,0.64, legx1+wid,0.88)
  leg2 = make_legend(legx2,0.68, legx2+wid,0.88)
  leg3 = make_legend(legx1,0.54, legx1+wid,0.63)
 
  lumi = mainlumi

  hs = THStack("hs","")
  hmctotName = mcsamples[0]['name']+"/"+weight+"/h1_"+mcsamples[0]['name']+"_"+mon+"_mm_"+step+"_"+weight
  #hmctotName = "h1_"+mcsamples[0]['name']+"_"+mon+"_mm_"+step
  if log : print "hmcTotal: "+hmctotName
  hmctot = f.Get(hmctotName).Clone("hmctot")
  hmcmerge = f.Get(hmctotName).Clone("hmcmerge")
  hmcSig = f.Get(hmctotName).Clone("hmcSig")
  hmctot.Reset()
  hmcmerge.Reset()
  hmcSig.Reset()

  hmcAmcNLO = hmctot.Clone("hmcAmcNLO")
  hmcMG5   = hmctot.Clone("hmcMG5")
  hdata = hmctot.Clone("hdata")
  myMCHistSet(hmctot)
  myMCHistSet(hmcmerge)
  myDataHistSet(hdata)

  isStat = mon.find("Stat")>-1
  if isStat : 
    print "Stat: step: "+step

  for i,mc in enumerate(mcsamples):
    isMC = mc["ColorLabel"]['label'].find("DATA")==-1
    if not isMC: continue

    histnameSmm = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_mm_"+step+"_"+weight
    histnameSee = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_ee_"+step+"_"+weight
    histnameSem = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_em_"+step+"_"+weight
    #channel = step[2:4]
    h2ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h2ee = f.Get(histnameSee).Clone("h"+histnameSee)
    h2em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h2ll) is not TH1D :
      continue


    h2ll.AddBinContent(h2ll.GetNbinsX(),h2ll.GetBinContent(h2ll.GetNbinsX()+1))
    h2ee.AddBinContent(h2ee.GetNbinsX(),h2ee.GetBinContent(h2ee.GetNbinsX()+1))
    h2em.AddBinContent(h2em.GetNbinsX(),h2em.GetBinContent(h2em.GetNbinsX()+1))
    ###############
    isDY = mc['name'].find("DYJet")>-1
    if isDY and int(step[1:2])>1: 
        h2ee.Scale(dyest[0])
        h2ll.Scale(dyest[1])


    #if h2.Integral()>0 :  h2.Scale(mc['cx']/Ntot*lumi)
    h2ll.Add(h2ee)
    h2ll.Add(h2em)

    if h2ll.Integral()>0 :  h2ll.Scale(mc['cx']*lumi)
    #if h2ll.Integral()>0 :  h2ll.Scale(lumi)

    ###############
    ci = TColor.GetColor(mc["ColorLabel"]['color']);
    h2ll.SetFillColor(ci)
    h2ll.SetLineColor(kBlack)

    isTTH = mc['name'].find("ttH")>-1
    isPowheg = mc['name'].find("POW")>-1
    isAmcNLO = mc['name'].find("AMC")>-1
    isMG5 = mc['name'].find("MG5")>-1
    if not isPowheg and not isTTH and not isMG5:
      hmcAmcNLO.Add(h2ll)
      if isStat and isAmcNLO:
        if h2ll.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)*10)/10)+" \pm "+str(round(h2ll.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)))+" \pm "+str(round(h2ll.GetBinError(1)))+" $"
      if isAmcNLO : continue
    if not isPowheg and not isTTH and not isAmcNLO:
      hmcMG5.Add(h2ll)
      if isStat and isMG5:
        if h2ll.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)*10)/10)+" \pm "+str(round(h2ll.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)))+" \pm "+str(round(h2ll.GetBinError(1)))+" $"
      if isMG5 : continue

    if not isTTH and not isMG5 and not isAmcNLO:
      hmctot.Add(h2ll)

    hmcmerge.Add(h2ll)
    #hs.Add( h2ll )

    selEvet=h2ll.Integral() 
    selEnts=h2ll.GetEntries()
    if log : print "mc:"+mc['file']+":"+str(round(selEvet))+", "+str(selEnts)
    isSameNext=False
    if i<len(mcsamples)-1 : isSameNext= mc["ColorLabel"]['label'] is mcsamples[i+1]["ColorLabel"]["label"]
    if  (not isSameNext) and isPowheg:
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)
      label = ("%s"%mc["ColorLabel"]['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and not isTTH :
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)
      label = ("%s"%mc["ColorLabel"]['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg2.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and  isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      #h3.SetLineColor(kBlack)
      hmcSig.Add(h3)
      hmcSig.SetLineColor(ci)
      hmcSig.SetTitle(mc["ColorLabel"]['label'])
      #label = ("%s"%mc['label']) + (" %.0f"%(hmcSig.Integral()) ).rjust(7)
      #leg2.AddEntry(hmcSig, label, "l")
      hmcmerge.Reset()

  hdata.Reset()
  for i,mc in enumerate(datasamples):
    histnameSmm = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_mm_"+step+"_CEN"
    histnameSee = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_ee_"+step+"_CEN"
    histnameSem = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_em_"+step+"_CEN"
    #channel = step[2:4]
    h1ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h1ee = f.Get(histnameSee).Clone("h"+histnameSee)
    h1em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h1ll) is not TH1D :
      continue
    h1ll.GetYaxis().SetTitle("Events")

    isMuMu = mc['name'].find("MuMu")==-1
    isElEl = mc['name'].find("ElEl")==-1
    isMuEl = mc['name'].find("MuEl")==-1
    if not isMuMu :
      h1ee.Reset()
      h1em.Reset()
    if not isElEl :
      h1ll.Reset()
      h1em.Reset()
    if not isMuEl :
      h1ee.Reset()
      h1ll.Reset()

    h1ll.AddBinContent(h1ll.GetNbinsX(),h1ll.GetBinContent(h1ll.GetNbinsX()+1))
    h1ee.AddBinContent(h1ee.GetNbinsX(),h1ee.GetBinContent(h1ee.GetNbinsX()+1))
    h1em.AddBinContent(h1em.GetNbinsX(),h1em.GetBinContent(h1em.GetNbinsX()+1))
    h1ll.Add(h1ee)
    h1ll.Add(h1em)

    selEvet=h1ll.Integral() 
    selEnts=h1ll.GetEntries()
 
    hdata.Add(h1ll)
    if log : print "data:"+mc['file']+": "+str(round(selEvet))+", "+str(selEnts)
    #if not (round(selEvet) == round(selEnts)) : return 
################################
  scale = hmctot.GetMaximum()
  minimum = 0.05

  h1data = hdata.Clone("h1data")
  h2data = myDataHistSet(h1data)

  maxY=0.
  for i in range(int(h1data.GetNbinsX()*0.7)+1, h1data.GetNbinsX()+2):
     if maxY<h1data.GetBinContent(i): maxY=h1data.GetBinContent(i)

  h2data.SetMaximum(maxY*10000)
  #if maxY is 0. : h2data.SetMaximum(scale*100)
  if maxY*10000 < scale*140 : h2data.SetMaximum(scale*140)

  #h2data.SetMaximum(scale*40)
  h2data.SetMinimum(minimum)
  #if log :  print "dddd"+str(type(hmctot))+("bbbb: %f"%hmctot.Integral())
  labeltot = ("MC Total") + (" %.0f"%hmctot.Integral()).rjust(8)
  #leg2.AddEntry(hmctot,labeltot,"")
  if isStat:
    if hmctot.GetBinContent(1)<100 : print " Stat: "+("MC Total").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)*10)/10)+" \pm "+str(round(hmctot.GetBinError(1)*10)/10)+" $"
    else                           : print " Stat: "+("MC Totlal").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)))+" \pm "+str(round(hmctot.GetBinError(1)))+" $"
 
  label = ("%s"%hmcSig.GetTitle()) #+ (" %.0f"%(hmcSig.Integral()) ).rjust(7)
  if isStat and (hmcSig.Integral()>0):
    if hmcSig.GetBinContent(1)<100 : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)*10)/10)+" \pm "+str(round(hmcSig.GetBinError(1)*10)/10)+" $"
    else                       : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)))+" \pm "+str(round(hmcSig.GetBinError(1)))+" $"
 
  labeldata = ("DATA     ") #+ (" %.0f"%h2data.Integral()).rjust(8)
  leg.AddEntry(h2data,labeldata,"p")
  if isStat:
    print " Stat: "+("DATA").rjust(10)+" & $ "+str(round(h2data.GetBinContent(1)))+" $" #+" +- "+str(h2data.GetBinError(1))
 

#########################################
  h2data.GetYaxis().SetTitle("Events")
  h2data.GetXaxis().SetTitle("")
  h2data.Draw()
  hs.Draw("same,hist")
  gr = myHist2TGraphError(hmctot)
  #gr.Draw("same,2")
  gr.Draw("e2SAME")
  #leg.AddEntry(gr,"Uncertainty","f")
  myAmcNLOHistSet(hmcAmcNLO)
  #hmcAmcNLO.Draw("histoSAME")
  myMG5HistSet(hmcMG5)
  hmcMG5.Draw("histoSAME")
  #leg3.AddEntry(hmcAmcNLO,"MC@NLO","l")
  leg3.AddEntry(hmcMG5,"Madgraph","l")
  leg3.AddEntry(hmcSig, label, "l")
  hmcSig.Draw("same")
  h2data.Draw("same")
#  h2data.Draw("sameaxis")


  leg.Draw()
  leg2.Draw()
  leg3.Draw()
  pad1.SetLogy()
  pt = addLegendLumi(lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode("ll")
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  pad1.Modified()
  c1.cd()
###########################################
  if log :  print "pad1 step"
  #pad2 = TPad("pad2", "",0,0,1,0.3)
  pad2 = myPad2(canvasname+"pad2")

  if log :  print "pad2 step1"
  pad2.Draw()
  pad2.cd()
  hdataAMC=hdata.Clone("hdataAMC")
  hdataMG5=hdata.Clone("hdataMG5")
  hdata.Divide(hmctot)
  hdataAMC.Divide(hmcAmcNLO)
  hdataMG5.Divide(hmcMG5)
  myAmcNLORatioSet(hdataAMC)
  myMG5RatioSet(hdataMG5)

  hratio = myRatio(hdata)
  hratio.GetXaxis().SetTitle(mon1['unit'])
  hratio.Draw()
  hratiosyst = myRatioSyst(hdata)
  hratiosyst.Draw("e2")
  hratio.Draw("e1SAME")
  #hdataAMC.Draw("histSAME")
  hdataMG5.Draw("histSAME")
  

  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  Weight2=weight.replace("CEN","")  
  output = "plots/eps/TH1_"+mon+"_"+step+"LL"+Weight2+".eps"
  output2 = "plots/png/TH1_"+mon+"_"+step+"LL"+Weight2+".png"
  c1.Print(output)
  c1.Print(output2)

  #f.Close()
  #c1.Close()
  if useReturn : return c1,pad1,pad2,hs,gr,h2data,hdataMC,leg,leg2
  else : c1.Close() 
    
############################################
############################################
############################################
############################################
############################################
############################################
def singleplotStackMMEE2(filename,mon,weight,step,mcsamples,datasamples,useReturn):
  f = TFile.Open(filename,"read")
  singleplotStackMMEE(f,mon,weight,step,mcsamples,datasamples,useReturn)
  f.Close()

def singleplotStackMMEE(f,mon1,weight,step,mcsamples,datasamples,useReturn):

  #dyest = drellYanEstimationRun(f,step[0:2])
  dyest = DYsf[step[0:2]]
  print "step : "+step+":"+str(dyest)
  #f = TFile.Open(filename,"read")
  mon = mon1["name"]
  canvasname = mon+step
  c1 = myCanvas(canvasname)
  #c1 = TCanvas( 'c1', '', 500, 500 )
  if log : print mon+step
  #c1.Divide(1,2)

   #Plot Pad
  pad1 = myPad1(canvasname+"pad1")
  #Ratio Pad
  pad2 = myPad2(canvasname+"pad2")
##############
  pad1.Draw()
  pad1.cd() 

  legx1 = 0.8
  wid=0.12
  legx2 = 0.67
  leg  = make_legend(legx1,0.64, legx1+wid,0.88)
  leg2 = make_legend(legx2,0.68, legx2+wid,0.88)
  leg3 = make_legend(legx1,0.54, legx1+wid,0.63)
 
  lumi = mainlumi

  hs = THStack("hs","")

  hmctotName = mcsamples[0]['name']+"/"+weight+"/h1_"+mcsamples[0]['name']+"_"+mon+"_mm_"+step+"_"+weight
  if log : print "hmcTotal: "+hmctotName
  hmctot = f.Get(hmctotName).Clone("hmctot")
  hmcmerge = f.Get(hmctotName).Clone("hmcmerge")
  hmcSig = f.Get(hmctotName).Clone("hmcSig")
  hmctot.Reset()
  hmcmerge.Reset()
  hmcSig.Reset()

  hmcAmcNLO = hmctot.Clone("hmcAmcNLO")
  hmcMG5   = hmctot.Clone("hmcMG5")
  hdata = hmctot.Clone("hdata")
  myMCHistSet(hmctot)
  myMCHistSet(hmcmerge)
  myDataHistSet(hdata)

  isStat = mon.find("Stat")>-1
  if isStat : 
    print "Stat: step: "+step

  for i,mc in enumerate(mcsamples):
    isMC = mc["ColorLabel"]['label'].find("DATA")==-1
    if not isMC: continue

    histnameSmm = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_mm_"+step+"_"+weight
    histnameSee = mc['name']+"/"+weight+"/"+"h1_"+mc['name']+"_"+mon+"_ee_"+step+"_"+weight
    #histnameSmm = "h1_"+mc['name']+"_"+mon+"_mm_"+step
    #histnameSee = "h1_"+mc['name']+"_"+mon+"_ee_"+step
    #histnameSem = "h1_"+mc['name']+"_"+mon+"_em_"+step
    #channel = step[2:4]
    h2ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h2ee = f.Get(histnameSee).Clone("h"+histnameSee)
    #h2em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h2ll) is not TH1D :
      continue


    h2ll.AddBinContent(h2ll.GetNbinsX(),h2ll.GetBinContent(h2ll.GetNbinsX()+1))
    h2ee.AddBinContent(h2ee.GetNbinsX(),h2ee.GetBinContent(h2ee.GetNbinsX()+1))
    #h2em.AddBinContent(h2em.GetNbinsX(),h2em.GetBinContent(h2em.GetNbinsX()+1))
    ###############
    isDY = mc['name'].find("DYJet")>-1
    if isDY and int(step[1:2])>1: 
        h2ee.Scale(dyest[0])
        h2ll.Scale(dyest[1])


    #if h2.Integral()>0 :  h2.Scale(mc['cx']/Ntot*lumi)
    h2ll.Add(h2ee)
    #h2ll.Add(h2em)

    if h2ll.Integral()>0 :  h2ll.Scale(mc['cx']*lumi)
    #if h2ll.Integral()>0 :  h2ll.Scale(lumi)

    ###############
    ci = TColor.GetColor(mc["ColorLabel"]['color']);
    h2ll.SetFillColor(ci)
    h2ll.SetLineColor(kBlack)

    isTTH = mc['name'].find("ttH")>-1
    isPowheg = mc['name'].find("POW")>-1
    isAmcNLO = mc['name'].find("AMC")>-1
    isMG5 = mc['name'].find("MG5")>-1
    if not isPowheg and not isTTH and not isMG5:
      hmcAmcNLO.Add(h2ll)
      if isStat and isAmcNLO:
        if h2ll.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)*10)/10)+" \pm "+str(round(h2ll.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)))+" \pm "+str(round(h2ll.GetBinError(1)))+" $"
      if isAmcNLO : continue
    if not isPowheg and not isTTH and not isAmcNLO:
      hmcMG5.Add(h2ll)
      if isStat and isMG5:
        if h2ll.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)*10)/10)+" \pm "+str(round(h2ll.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h2ll.GetBinContent(1)))+" \pm "+str(round(h2ll.GetBinError(1)))+" $"
      if isMG5 : continue

    if not isTTH and not isMG5 and not isAmcNLO:
      hmctot.Add(h2ll)

    hmcmerge.Add(h2ll)
    #hs.Add( h2ll )

    selEvet=h2ll.Integral() 
    selEnts=h2ll.GetEntries()
    if log : print "mc:"+mc['file']+":"+str(round(selEvet))+", "+str(selEnts)
    isSameNext=False
    if i<len(mcsamples)-1 : isSameNext= mc["ColorLabel"]['label'] is mcsamples[i+1]["ColorLabel"]["label"]
    if  (not isSameNext) and isPowheg:
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)
      label = ("%s"%mc["ColorLabel"]['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and not isTTH :
      h3=hmcmerge.Clone("h"+mc['name'])
      h3.SetFillColor(ci)
      h3.SetLineColor(kBlack)
      label = ("%s"%mc["ColorLabel"]['label'])# + (" %.0f"%(h3.Integral()) ).rjust(7)
      leg2.AddEntry(h3, label, "f")
      if isStat:
        if h3.GetBinContent(1)<100 : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)*10)/10)+" \pm "+str(round(h3.GetBinError(1)*10)/10)+" $"
        else                       : print " Stat: "+(mc['name']).rjust(10)+" & $"+str(round(h3.GetBinContent(1)))+" \pm "+str(round(h3.GetBinError(1)))+" $"
 
      hs.Add(h3)
      hmcmerge.Reset()
    elif not isSameNext and  isTTH : 
      h3=hmcmerge.Clone("h"+mc['name'])
      #h3.SetLineColor(kBlack)
      hmcSig.Add(h3)
      hmcSig.SetLineColor(ci)
      hmcSig.SetTitle(mc["ColorLabel"]['label'])
      #label = ("%s"%mc['label']) + (" %.0f"%(hmcSig.Integral()) ).rjust(7)
      #leg2.AddEntry(hmcSig, label, "l")
      hmcmerge.Reset()

  hdata.Reset()
  for i,mc in enumerate(datasamples):
    histnameSmm = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_mm_"+step+"_CEN"
    histnameSee = mc['name']+"/CEN/"+"h1_"+mc['name']+"_"+mon+"_ee_"+step+"_CEN"
    #histnameSmm = "h1_"+mc['name']+"_"+mon+"_mm_"+step[0:2]
    #histnameSee = "h1_"+mc['name']+"_"+mon+"_ee_"+step[0:2]
    #histnameSem = "h1_"+mc['name']+"_"+mon+"_em_"+step[0:2]
    #channel = step[2:4]
    h1ll = f.Get(histnameSmm).Clone("h"+histnameSmm)
    h1ee = f.Get(histnameSee).Clone("h"+histnameSee)
    #h1em = f.Get(histnameSem).Clone("h"+histnameSem)
    if type(h1ll) is not TH1D :
      continue
    h1ll.GetYaxis().SetTitle("Events")

    isMuMu = mc['name'].find("MuMu")==-1
    isElEl = mc['name'].find("ElEl")==-1
    #isMuEl = mc['name'].find("MuEl")==-1
    if not isMuMu :
      h1ee.Reset()
      #h1em.Reset()
    if not isElEl :
      h1ll.Reset()
      #h1em.Reset()
    #if not isMuEl :
    #  h1ee.Reset()
    #  h1ll.Reset()

    h1ll.AddBinContent(h1ll.GetNbinsX(),h1ll.GetBinContent(h1ll.GetNbinsX()+1))
    h1ee.AddBinContent(h1ee.GetNbinsX(),h1ee.GetBinContent(h1ee.GetNbinsX()+1))
    #h1em.AddBinContent(h1em.GetNbinsX(),h1em.GetBinContent(h1em.GetNbinsX()+1))
    h1ll.Add(h1ee)
    #h1ll.Add(h1em)

    selEvet=h1ll.Integral() 
    selEnts=h1ll.GetEntries()
 
    hdata.Add(h1ll)
    if log : print "data:"+mc['file']+": "+str(round(selEvet))+", "+str(selEnts)
    #if not (round(selEvet) == round(selEnts)) : return 
################################
  scale = hmctot.GetMaximum()
  minimum = 0.05

  h1data = hdata.Clone("h1data")
  h2data = myDataHistSet(h1data)

  maxY=0.
  for i in range(int(h1data.GetNbinsX()*0.7)+1, h1data.GetNbinsX()+2):
     if maxY<h1data.GetBinContent(i): maxY=h1data.GetBinContent(i)

  h2data.SetMaximum(maxY*10000)
  #if maxY is 0. : h2data.SetMaximum(scale*100)
  if maxY*10000 < scale*140 : h2data.SetMaximum(scale*140)

  #h2data.SetMaximum(scale*40)
  h2data.SetMinimum(minimum)
  #if log :  print "dddd"+str(type(hmctot))+("bbbb: %f"%hmctot.Integral())
  labeltot = ("MC Total") + (" %.0f"%hmctot.Integral()).rjust(8)
  #leg2.AddEntry(hmctot,labeltot,"")
  if isStat:
    if hmctot.GetBinContent(1)<100 : print " Stat: "+("MC Total").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)*10)/10)+" \pm "+str(round(hmctot.GetBinError(1)*10)/10)+" $"
    else                           : print " Stat: "+("MC Totlal").rjust(10)+" & $"+str(round(hmctot.GetBinContent(1)))+" \pm "+str(round(hmctot.GetBinError(1)))+" $"
 
  label = ("%s"%hmcSig.GetTitle()) #+ (" %.0f"%(hmcSig.Integral()) ).rjust(7)
  if isStat and (hmcSig.Integral()>0):
    if hmcSig.GetBinContent(1)<100 : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)*10)/10)+" \pm "+str(round(hmcSig.GetBinError(1)*10)/10)+" $"
    else                       : print " Stat: "+("tth").rjust(10)+" & $"+str(round(hmcSig.GetBinContent(1)))+" \pm "+str(round(hmcSig.GetBinError(1)))+" $"
 
  labeldata = ("DATA     ") #+ (" %.0f"%h2data.Integral()).rjust(8)
  leg.AddEntry(h2data,labeldata,"p")
  if isStat:
    print " Stat: "+("DATA").rjust(10)+" & $ "+str(round(h2data.GetBinContent(1)))+" $" #+" +- "+str(h2data.GetBinError(1))
 

#########################################
  h2data.GetYaxis().SetTitle("Events")
  h2data.GetXaxis().SetTitle("")
  h2data.Draw()
  hs.Draw("same,hist")
  gr = myHist2TGraphError(hmctot)
  #gr.Draw("same,2")
  gr.Draw("e2SAME")
  #leg.AddEntry(gr,"Uncertainty","f")
  myAmcNLOHistSet(hmcAmcNLO)
  #hmcAmcNLO.Draw("histoSAME")
  myMG5HistSet(hmcMG5)
  hmcMG5.Draw("histoSAME")
  #leg3.AddEntry(hmcAmcNLO,"MC@NLO","l")
  leg3.AddEntry(hmcMG5,"Madgraph","l")
  leg3.AddEntry(hmcSig, label, "l")
  hmcSig.Draw("same")
  h2data.Draw("same")
#  h2data.Draw("sameaxis")


  leg.Draw()
  leg2.Draw()
  leg3.Draw()
  pad1.SetLogy()
  pt = addLegendLumi(lumi)
  pt2 = addLegendCMS()
  pt3 = addDecayMode("#mu#mu/ee")
  pt.Draw()
  pt2.Draw()
  pt3.Draw()

  pad1.Modified()
  c1.cd()
###########################################
  if log :  print "pad1 step"
  #pad2 = TPad("pad2", "",0,0,1,0.3)
  pad2 = myPad2(canvasname+"pad2")

  if log :  print "pad2 step1"
  pad2.Draw()
  pad2.cd()
  hdataAMC=hdata.Clone("hdataAMC")
  hdataMG5=hdata.Clone("hdataMG5")
  hdata.Divide(hmctot)
  hdataAMC.Divide(hmcAmcNLO)
  hdataMG5.Divide(hmcMG5)
  myAmcNLORatioSet(hdataAMC)
  myMG5RatioSet(hdataMG5)

  hratio = myRatio(hdata)
  hratio.GetXaxis().SetTitle(mon1['unit'])
  hratio.Draw()
  hratiosyst = myRatioSyst(hdata)
  hratiosyst.Draw("e2")
  hratio.Draw("e1SAME")
  #hdataAMC.Draw("histSAME")
  hdataMG5.Draw("histSAME")
  

  pad2.Modified()
  c1.cd()
  c1.Modified()
  c1.cd()

  Weight2=weight.replace("CEN","")  
  output = "plots/eps/TH1_"+mon+"_"+step+"MMEE"+Weight2+".eps"
  output2 = "plots/png/TH1_"+mon+"_"+step+"MMEE"+Weight2+".png"
  c1.Print(output)
  c1.Print(output2)

  #f.Close()
  #c1.Close()
  if useReturn : return c1,pad1,pad2,hs,gr,h2data,hdataMC,leg,leg2
  else : c1.Close() 
   
