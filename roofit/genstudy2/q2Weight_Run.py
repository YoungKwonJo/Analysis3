from q2Weight2 import POW,dwPOW,upPOW,AMC,MG5,POHP
from ROOT import TH1D

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

def getNumbers(aaa,key,key2):
  ttbbFS = aaa["S0"]["ttbbF"]
  ttjjFS = aaa["S0"]["ttbbF"]+aaa["S0"]["ttbF"]+aaa["S0"]["tt2bF"]+aaa["S0"]["ttccF"]+aaa["S0"]["ttlfF"]
  ttbbVS = aaa["S0"]["ttbb"]
  ttjjVS = aaa["S0"]["ttbb"]+aaa["S0"]["ttb"]+aaa["S0"]["tt2b"]+aaa["S0"]["ttcc"]+aaa["S0"]["ttlf"]

  ttbbS6 = aaa["S6"]["ttbb"]
  ttjjS6 = aaa["S6"]["ttbb"]+aaa["S6"]["ttb"]+aaa["S6"]["tt2b"]+aaa["S6"]["ttcc"]+aaa["S6"]["ttlf"]

  total=aaa["dileptonicP1"]+aaa["dileptonicP1not"]
  llratio = aaa["dileptonicP1"]/total

  ttbarCX=831.76
  ttjjFSCX = ttbarCX/llratio*ttjjFS/total
  ttbbFSCX = ttbarCX/llratio*ttbbFS/total
  ttjjVSCX = ttbarCX*ttjjVS/total
  ttbbVSCX = ttbarCX*ttbbVS/total

  output = {"key":key,"key2":key2,"ttbbFS": ttbbFS, "ttjjFS":ttjjFS, "ttbbVS":ttbbVS, "ttjjVS":ttjjVS, "llratio":llratio,"ttjjAcc": ttjjVS/ttjjFS*llratio, "ttbbAcc":ttbbVS/ttbbFS*llratio,"total":total, "ttbbS6":ttbbS6, "ttjjS6":ttjjS6, "ttbbEff":ttbbS6/ttbbVS, "ttjjEff":ttjjS6/ttjjVS, "ttjjFSCX":ttjjFSCX,"ttbbFSCX":ttbbFSCX,"ttjjVSCX":ttjjVSCX,"ttbbVSCX":ttbbVSCX }
  return output
  #return ttbbFS/llratio,ttjjFS/llratio,ttbbVS,ttjjVS,llratio

def roudV(val1):
  val =abs(val1)
  if val > 100 :
    return int(round(val))
  elif val > 10 :
    return int(round(val))
  elif val > 1 :
    return round(val*10)/10
  else :
    nom=10.
    if val>0.1    : nom=100.
    elif val>0.01 : nom=1000.
    else          : nom=10000.
#    elif val>0.001: nom=1000000.
#    elif val>0.0001: nom=10000000.
#    else          : nom=1000000000.

    return round(val*nom)/nom

def printARow(bbb):
  print bbb["key"]+" & "+str(roudV(bbb["ttjjAcc"]))+" & "+str(roudV(bbb["ttbbAcc"]))+" \\\\ "

def getSys(a,b):
  return abs(1/a-1/b)/(1/a)
  #return abs(a-b)/a

def printARow2(bbb,aaa):
  ttjjAccSys=getSys(aaa["ttjjAcc"],bbb["ttjjAcc"])
  ttbbAccSys=getSys(aaa["ttbbAcc"],bbb["ttbbAcc"])

  ttjjEffSys=getSys(aaa["ttjjEff"],bbb["ttjjEff"])
  ttbbEffSys=getSys(aaa["ttbbEff"],bbb["ttbbEff"])

  MEs = {}
  MEs["nom"] = "muR=1 muF=1"
  MEs["weight"] = "muR=1 muF=1"
  MEs["Q2_Dw1"] = "muR=1 muF=0.5"
  MEs["Q2_Dw2"] = "muR=0.5 muF=1"
  MEs["Q2_Dw3"] = "muR=0.5 muF=0.5"
  MEs["Q2_Up1"] = "muR=1 muF=2"
  MEs["Q2_Up2"] = "muR=2 muF=1"
  MEs["Q2_Up3"] = "muR=2 muF=2"
  tot={}
  tot["POW"] =97994442.0
  tot["dwPOW"]=9932876.0
  tot["upPOW"]=9919776.0
  tot["AMC"] =12771412.0
  tot["MG5"] =10215131.0
  tot["POHP"]=19383463.0 

  
  label={}
  label["POW"] ="POWHEG"
  label["dwPOW"]="$PS_{dw}$"
  label["upPOW"]="$PS_{up}$"
  label["AMC"] ="aMC@NLO"
  label["MG5"] ="Madgraph"
  label["POHP"]="POW\\_H++"
  

  total1 = tot[bbb["key2"]]
  total2 = bbb["total"]
  totalCorr = total1/total2

  from math import sqrt
  ttjjAcc = bbb["ttjjAcc"]
  ttbbAcc = bbb["ttbbAcc"]
  ttjjEff = bbb["ttjjEff"]
  ttbbEff = bbb["ttbbEff"]

  ttjjFS = bbb["ttjjFS"]
  ttjjVS = bbb["ttjjVS"]
  ttbbFS = bbb["ttbbFS"]
  ttbbVS = bbb["ttbbVS"]
  ttjjS6 = bbb["ttjjS6"]
  ttbbS6 = bbb["ttbbS6"]

  llratio = bbb["llratio"] #sqrt(total1)/sqrt(bbb["llratio"]*total1)*sqrt(bbb["llratio"])
  statAcc_ttjj = getError(ttjjVS*totalCorr, ttjjFS*totalCorr)#*statAcc2
  statAcc_ttbb = getError(ttbbVS*totalCorr, ttbbFS*totalCorr)#*statAcc2
  
  statEff_ttjj = getError(ttjjS6*totalCorr, ttjjVS*totalCorr)
  statEff_ttbb = getError(ttbbS6*totalCorr, ttbbVS*totalCorr)


  """
  PSs = {}
  PSs["POW"] = "POW "
  PSs["dwPOW"]="$PS_{dw}$ "
  PSs["upPOW"]="$PS_{up}$ "
  """
  bbb["statAcc_ttjj"]=statAcc_ttjj/ttjjAcc
  bbb["statAcc_ttbb"]=statAcc_ttbb/ttbbAcc
  bbb["statEff_ttjj"]=statEff_ttjj/ttjjEff
  bbb["statEff_ttbb"]=statEff_ttbb/ttbbEff

  bbb["sysAcc_ttjj"]=ttjjAccSys
  bbb["sysAcc_ttbb"]=ttbbAccSys
  bbb["sysEff_ttjj"]=ttjjEffSys
  bbb["sysEff_ttbb"]=ttbbEffSys

  nn=40
  ccc= label[bbb["key2"]].ljust(10)
  ccc+=(" & "+MEs[bbb["key"]]).ljust(25)
  ccc+=(" & "+str(roudV(ttjjAcc))+" $\pm$ ("+str(roudV(statAcc_ttjj*100./ttjjAcc))+" \\%) $\pm$ ("+str(roudV(ttjjAccSys*100.))+" \\%) ").ljust(nn)
  ccc+=(" & "+str(roudV(ttbbAcc))+" $\pm$ ("+str(roudV(statAcc_ttbb*100./ttbbAcc))+" \\%) $\pm$ ("+str(roudV(ttbbAccSys*100.))+" \\%) ").ljust(nn)
  ccc+=(" & "+str(roudV(ttjjEff))+" $\pm$ ("+str(roudV(statEff_ttjj*100./ttjjEff))+" \\%) $\pm$ ("+str(roudV(ttjjEffSys*100.))+" \\%) ").ljust(nn)
  ccc+=(" & "+str(roudV(ttbbEff))+" $\pm$ ("+str(roudV(statEff_ttbb*100./ttbbEff))+" \\%) $\pm$ ("+str(roudV(ttbbEffSys*100.))+" \\%) ").ljust(nn)
  #ccc+=(" & ")+str(bbb["total"] ).ljust(20)
  ccc+=" \\\\ "
  #print ccc

def getOutputAll(aaa):
  outputAll = {}
  for key in aaa.keys():
    key2=aaa[key][key].keys()[0]
    bbb=aaa[key][key][key2]
    outputAll[key]=getNumbers(bbb,key,key2)
  return outputAll


POW2 = getOutputAll(POW)
dwPOW2 = getOutputAll(dwPOW)
upPOW2 = getOutputAll(upPOW)
AMC2 = getOutputAll(AMC)
MG52 = getOutputAll(MG5)
POHP2 = getOutputAll(POHP)

for key in sorted(POW2.keys()):
  printARow2( POW2[key], POW2["nom"])
for key in sorted(dwPOW2.keys()):
  printARow2( dwPOW2[key], POW2["nom"])
for key in sorted(upPOW2.keys()):
  printARow2( upPOW2[key], POW2["nom"])
for key in sorted(AMC2.keys()):
  printARow2( AMC2[key], POW2["nom"])
for key in sorted(MG52.keys()):
  printARow2( MG52[key], POW2["nom"])
for key in sorted(POHP2.keys()):
  printARow2( POHP2[key], POW2["nom"])

print "POW="+str(POW2)
print "dwPOW="+str(dwPOW2)
print "upPOW="+str(upPOW2)
print "AMC="+str(AMC2)
print "MG5="+str(MG52)
print "POHP="+str(POHP2)













