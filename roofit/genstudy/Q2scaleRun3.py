
from pdfAllRun import roudV,printV,sumV,roudV

def printV2(data,data2,isPrint):
  total = sumV(data,"",['dileptonic','semileptonic','hadroic'])
  if isPrint : print "total : "+str(total)
  if isPrint : print "dileptonic : "+str(data['dileptonic'])+", semileptonic : "+str(data['semileptonic'])+", hadroic : "+str(data['hadroic'])
  VS = ["ttbb","tt2b","ttb","ttcc","ttlf"]# "ttot"
  FS = ["ttbbF","tt2bF","ttbF","ttccF","ttlfF"]
  ttbb = data['S0']['ttbb']
  ttbbF = data2['data']['ttbbF']
  ttjj = sumV(data,'S0',VS)
  ttjjF = sumV(data2["data"],"",FS)
  ttbbAcc=data2["ttbb"]#ttbb/ttbbF
  ttjjAcc=data2["ttjj"] #ttjj/ttjjF
  rFS = ttbbF/ttjjF
  rVS = ttbb/ttjj
  rTtjjTotalFS=ttjjF/total
  rTtjjTotalVS=ttjj/total

  if isPrint : print "ratio ttjj/total FS: "+str(roudV(rTtjjTotalFS*100))+" %"
  if isPrint : print "ratio ttjj/total VS: "+str(roudV(rTtjjTotalVS*100))+" %"
  if isPrint : print "Acceptance(VS/FS) ttbb : "+str(roudV(ttbbAcc))+", ttjj : "+str(roudV(ttjjAcc))
  if isPrint : print "FS R(ttbb/ttjj) : "+str(roudV(rFS)*100)+" %"
  if isPrint : print "VS R(ttbb/ttjj) : "+str(roudV(rVS)*100)+" %"
  ttbbS6 = data['S6']['ttbb']
  ttjjS6 = sumV(data,"S6",["ttbb","tt2b","ttb","ttcc","ttlf"])
  ttbbEff= ttbbS6/ttbb
  ttjjEff= ttjjS6/ttjj
  rTtjjTotalS6=ttjjS6/total
  if isPrint : print "ratio ttjj/total S6: "+str(roudV(rTtjjTotalS6))+" %"
  if isPrint : print "efficiency S6/S0 in VS"
  if isPrint : print "ttbb : "+str(roudV(ttbbEff)*100)+" %"
  if isPrint : print "ttjj : "+str(roudV(ttjjEff)*100)+" %"

  return {"rFS":rFS,"rVS":rVS,"Acc":{"ttbb":ttbbAcc,"ttjj":ttjjAcc},"Eff":{"ttbb":ttbbEff,"ttjj":ttjjEff},"rTtjjTotal":{"FS":rTtjjTotalFS,"VS":rTtjjTotalVS,"S6":rTtjjTotalS6}}


def getRttjjttbb(sample,RFit,NttjjFit,lumi):
  Rvps = RFit*sample["Eff"]["ttjj"]/sample["Eff"]["ttbb"]
  Rfps = Rvps*sample["Acc"]["ttjj"]/sample["Acc"]["ttbb"]
  SigTTJJvps = NttjjFit/(sample["Eff"]["ttjj"]*lumi)
  SigTTJJfps = SigTTJJvps / sample["Acc"]["ttjj"]

  SigTTBBvps = Rvps*SigTTJJvps
  SigTTBBfps = SigTTBBvps/sample["Acc"]["ttbb"]

  return {"vps":{"R":Rvps, "Sigma":{"ttjj":SigTTJJvps ,"ttbb":SigTTBBvps } },"fps":{"R":Rfps, "Sigma":{"ttjj":SigTTJJfps ,"ttbb":SigTTBBfps } } }
  #return {"rFS":rFS,"rVS":rVS,"Acc":{"ttbb":ttbbAcc,"ttjj":ttjjAcc},"Eff":{"ttbb":ttbbEff,"ttjj":ttjjEff},"rTtjjTotal":{"FS":rTtjjTotalFS,"VS":rTtjjTotalVS,"S6":rTtjjTotalS6}}

def getSys(sample, sample2,key):
  R=(sample[key]["R"]-sample2[key]["R"])/sample[key]["R"]
  ttjj=(sample[key]["Sigma"]["ttjj"]-sample2[key]["Sigma"]["ttjj"])/sample[key]["Sigma"]["ttjj"]
  ttbb=(sample[key]["Sigma"]["ttbb"]-sample2[key]["Sigma"]["ttbb"])/sample[key]["Sigma"]["ttbb"]
  return {"R":R,"ttbb":ttbb,"ttjj":ttjj}

def printSys(POW3,sample,data2,RFit,NttjjFit,lumi):

  #sample2=printV(sample,False)
  sample2=printV2(sample,data2,False)
  sample3=getRttjjttbb(sample2,RFit,NttjjFit,lumi)
  vps=getSys(POW3,sample3,"vps")
  fps=getSys(POW3,sample3,"fps")

  #print "vps:"+str(vps)
  #print "fps:"+str(fps)
  return {"vpsSys":vps, "fpsSys":fps,"data":sample2,"data2":sample3}  

def compareSYS(data,data2):
  dataAll={}
  for x in ["vpsSys","fpsSys"]:
    data3={}
    for y in data[x].keys():
      data3[y]= max(abs(data[x][y]),abs(data2[x][y]))
    dataAll[x]=data3 
  return dataAll

def SysVal(Sys,CEN):
  return abs( (1./CEN)-(1./Sys))/(1./CEN) 
  #return abs( (CEN)-(Sys))/(CEN) 


def roudV2(val2):
  val=val2
  sign=1.
  if val2<0: 
    val=-val2
    sign=-1.
  if val > 100 :
    return int(round(val))*sign
  elif val > 1 : 
    return round(val*100)/100*sign
  else :
    nom=10000.
    if val>0.1    : nom=1000.
    elif val>0.01 : nom=10000.
    elif val>0.001: nom=100000.
    else          : nom=10000000.

    return round(val*nom)/nom*sign


def printAccEff(name,Sys,CEN):
  ttjjAcc=Sys["data"]["Acc"]["ttjj"]
  ttbbAcc=Sys["data"]["Acc"]["ttbb"]
  ttjjEff=Sys["data"]["Eff"]["ttjj"]
  ttbbEff=Sys["data"]["Eff"]["ttbb"]
  #Rvps= Sys["data2"]["vps"]["R"]
  #Rfps= Sys["data2"]["fps"]["R"]

  ttjjAccSys= SysVal(ttjjAcc, CEN["data"]["Acc"]["ttjj"])
  ttbbAccSys= SysVal(ttbbAcc, CEN["data"]["Acc"]["ttbb"])
  ttjjEffSys= SysVal(ttjjEff, CEN["data"]["Eff"]["ttjj"])
  ttbbEffSys= SysVal(ttbbEff, CEN["data"]["Eff"]["ttbb"])

  ttjjEffttbbEffSys = SysVal( ttjjEff/ttbbEff, CEN["data"]["Eff"]["ttjj"]/CEN["data"]["Eff"]["ttbb"])
  ttjjACCEffSys = SysVal( ttjjEff*ttjjAcc , CEN["data"]["Eff"]["ttjj"]*CEN["data"]["Acc"]["ttjj"])
  ttbbACCEffSys = SysVal( ttbbEff*ttbbAcc , CEN["data"]["Eff"]["ttbb"]*CEN["data"]["Acc"]["ttbb"])

  ttjjACCttbbACCSys = SysVal( (ttjjEff*ttjjAcc)/(ttbbEff*ttbbAcc), (CEN["data"]["Eff"]["ttjj"]*CEN["data"]["Acc"]["ttjj"])/(CEN["data"]["Eff"]["ttbb"]*CEN["data"]["Acc"]["ttbb"]) )
  #RvpsSys   = SysVal(Rvps, CEN["data2"]["vps"]["R"])
  #RfpsSys   = SysVal(Rfps, CEN["data2"]["fps"]["R"])

  #print name+" & "+str(roudV(ttjjAcc*100.))+" & "+str(roudV(ttbbAcc*100.))+" & "+str(roudV(ttjjEff*100))+" & "+str(roudV(ttbbEff*100))+" & "+str(roudV(Rvps))+" & "+str(roudV(Rfps))+" \\\\ "
  #print name+" & "+str(roudV(ttjjAcc*100.))+" & "+str(roudV(ttbbAcc*100.))+" & "+str(roudV(ttjjEff*100))+" & "+str(roudV(ttbbEff*100))+" & "+str(roudV(ttjjEff/ttbbEff))+" & "+str(roudV((ttjjEff*ttjjAcc)/(ttbbEff*ttbbAcc)))+" \\\\ "
  ss,ss2,ss3 = 30,16,16
  AccPrint= (name.ljust(ss))+" & "+(str(roudV(ttjjAcc*100.))+" ("+str(roudV2(ttjjAccSys*100))+")").ljust(ss2)+" & "+(str(roudV(ttbbAcc*100.))+" ("+str(roudV2(ttbbAccSys*100))+") ").ljust(ss2)
  EffPrint = "& "+(str(roudV(ttjjEff*100))+" ("+str(roudV2(ttjjEffSys*100))+")").ljust(ss3)+" & "+(str(roudV(ttbbEff*100))+" ("+str(roudV2(ttbbEffSys*100))+") ").ljust(ss3)
  Rprint = "& "+(str(roudV(ttjjEff/ttbbEff*100))+" ("+str(roudV2(ttjjEffttbbEffSys*100))+")").ljust(ss3)+" & "+(str(roudV((ttjjEff*ttjjAcc)/(ttbbEff*ttbbAcc)*100))+" ("+str(roudV2(ttjjACCttbbACCSys*100))+")").ljust(ss3)
  AccEffPrint ="& "+(str(roudV(ttjjEff*ttjjAcc*100))+" ("+str(roudV2(ttjjACCEffSys)*100)+") ").ljust(ss3)+" & "+(str(roudV(ttbbEff*ttbbAcc*100))+" ("+str(roudV2(ttbbACCEffSys)*100)+") ").ljust(ss3)
  print AccPrint+EffPrint+Rprint+AccEffPrint+" \\\\"


def main():
  from Q2scale import *
  from Q2scaleFPS_Run import dwPOW_Acc,POW_Acc,upPOW_Acc

  RFit = 0.0557405348697
  NttjjFit = 926.771624879
  lumi = 2318.278305882 

  #print "> python Q2scaleRun2.py > resultQ2scaleSys.txt"
  #print ""
  #print 'POW'
  POW2=printV2(POW,POW_Acc["nom"],False)
  POW3=getRttjjttbb(POW2,RFit,NttjjFit,lumi)
  print "POW"
  print POW3
  POW4={}
  POW4["data"]=POW2
  POW4["data2"]=POW3
  printAccEff("POW",POW4,POW4)


  MEs = {}
  MEs["nom"] = "muR=1 muF=1"
  MEs["Dw1"] = "muR=1 muF=0.5"
  MEs["Dw2"] = "muR=0.5 muF=1"
  MEs["Dw3"] = "muR=0.5 muF=0.5"

  MEs["Up1"] = "muR=1 muF=2"
  MEs["Up2"] = "muR=2 muF=1"
  MEs["Up3"] = "muR=2 muF=2"
  PSs = {}
  PSs["POW"] = "POW "
  PSs["dwPOW"]="$PS_{dw}$ "
  PSs["upPOW"]="$PS_{up}$ "


  maxSys=printSys(POW3,POW,POW_Acc["nom"],RFit,NttjjFit,lumi)
  #print "Down"
  #print str(POW3)
  #print "+Central Sample"
  for i in range(1,4):
    Sys=printSys(POW3,POWsys['Q2_Dw'+str(i)],POW_Acc['Q2_Dw'+str(i)],RFit,NttjjFit,lumi)
    printAccEff(PSs["POW"]+MEs["Dw"+str(i)],Sys,POW4)
    maxSys=compareSYS(maxSys,Sys)

  #print maxSys
  #print "+Central Sample"
  for i in range(1,4):
    #print "++Q2_Up"+str(i)
    Sys=printSys(POW3,POWsys['Q2_Up'+str(i)],upPOW_Acc['Q2_Up'+str(i)],RFit,NttjjFit,lumi)
    printAccEff(PSs["POW"]+MEs["Up"+str(i)],Sys,POW4)
    maxSys=compareSYS(maxSys,Sys)
    
  #print maxSys
  #print "+Down Sample, nom"
  #print dwPOW_Acc["nom"]

  dwSys=printSys(POW3,dwPOW['nom']['dwPOW'],dwPOW_Acc["nom"],RFit,NttjjFit,lumi)
  printAccEff(PSs["dwPOW"]+MEs["nom"],dwSys,POW4)

  #print ""
  #print "+ME Down Sample"
  for i in range(1,4):
    #print "++Q2_Dw"+str(i)
    Sys=printSys(POW3,dwPOW['Q2_Dw'+str(i)]['dwPOW'],dwPOW_Acc['Q2_Dw'+str(i)],RFit,NttjjFit,lumi)
    printAccEff(PSs["dwPOW"]+MEs["Dw"+str(i)],Sys,POW4)
    maxSys=compareSYS(maxSys,Sys)
 
  #print maxSys

  #print maxSys
  #print ""
  #print "Up"

  upSys=printSys(POW3,upPOW['nom']['upPOW'],upPOW_Acc['nom'],RFit,NttjjFit,lumi)
  maxSys=compareSYS(maxSys,upSys)
  printAccEff(PSs["upPOW"]+MEs["nom"],upSys,POW4)

  #print ""
  #print "+ME Up Sample"
  for i in range(1,4):
    #print "++Q2_Up"+str(i)
    Sys=printSys(POW3,upPOW['Q2_Up'+str(i)]['upPOW'],upPOW_Acc['Q2_Up'+str(i)],RFit,NttjjFit,lumi)
    printAccEff(PSs["upPOW"]+MEs["Up"+str(i)],Sys,POW4)
    maxSys=compareSYS(maxSys,Sys)

  print maxSys


if __name__ == "__main__":
    test=main()

