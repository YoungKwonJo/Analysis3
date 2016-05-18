
def PrintSys2(data,data2):
  return PrintSys3(data,data2,True)

def PrintSys3(data,data2,isPrint):
  from pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
  sysRvs=getSys(data['rVS'],data2['rVS'])
  sysRfs=getSys(data['rFS'],data2['rFS'])
  sysTtbbEff=getSys(data['Eff']["ttbb"],data2['Eff']['ttbb'])
  sysTtjjEff=getSys(data['Eff']["ttjj"],data2['Eff']['ttjj'])

  sysTtbbAcc=getSys(data['Acc']["ttbb"],data2['Acc']['ttbb'])
  sysTtjjAcc=getSys(data['Acc']["ttjj"],data2['Acc']['ttjj'])


  sysRtjtFS=getSys(data['rTtjjTotal']['FS'],data2['rTtjjTotal']['FS'])
  sysRtjtVS=getSys(data['rTtjjTotal']['VS'],data2['rTtjjTotal']['VS'])
  sysRtjtS6=getSys(data['rTtjjTotal']['S6'],data2['rTtjjTotal']['S6'])
  if isPrint:
    #print "+++sys ttbb/ttjj in VS : "+str(roudV(sysRvs)*100)+" %"
    #print "+++sys ttbb/ttjj in FS : "+str(roudV(sysRfs)*100)+" %"
    #print "+++sys Ttjj/TotalFS : "+str(roudV(sysRtjtFS)*100)+" %"
    #print "+++sys Ttjj/TotalVS : "+str(roudV(sysRtjtVS)*100)+" %"
    #print "+++sys Ttjj/TotalS6 : "+str(roudV(sysRtjtS6)*100)+" %"
    #print "sys rFS : "+str(roudV(sysRfs)*100)+" %"
    print "sys ttbb Eff : "+str(roudV(sysTtbbEff)*100)+" %"
    print "sys ttjj Eff : "+str(roudV(sysTtjjEff)*100)+" %"
    print "sys ttbb Acc : "+str(roudV(sysTtbbAcc)*100)+" %"
    print "sys ttjj Acc : "+str(roudV(sysTtjjAcc)*100)+" %"


  return {"rFS":abs(sysRfs),"rVS":abs(sysRvs),"kFS":abs(sysRtjtFS),"kVS":abs(sysRtjtVS),"kS6":abs(sysRtjtS6),"Acc":{"ttbb":sysTtbbAcc,"ttjj":sysTtjjAcc },"Eff":{"ttbb":sysTtbbEff,"ttjj":sysTtjjEff}}

def compareSYS(data,data2):
  data3={}
  data3['rVS']=max(abs(data["rVS"]),abs(data2["rVS"]))
  data3['kFS']=max(abs(data["kFS"]),abs(data2["kFS"]))
  data3['kVS']=max(abs(data["kVS"]),abs(data2["kVS"]))
  data3['kS6']=max(abs(data["kS6"]),abs(data2["kS6"]))
  AccTTBB = max(abs(data["Acc"]["ttbb"]),abs(data2["Acc"]["ttbb"]))
  AccTTJJ = max(abs(data["Acc"]["ttjj"]),abs(data2["Acc"]["ttjj"]))
  EffTTBB = max(abs(data["Eff"]["ttbb"]),abs(data2["Eff"]["ttbb"]))
  EffTTJJ = max(abs(data["Eff"]["ttjj"]),abs(data2["Eff"]["ttjj"]))
  data3["Acc"]={"ttbb":AccTTBB,"ttjj":AccTTJJ}
  data3["Eff"]={"ttbb":EffTTBB,"ttjj":EffTTJJ}

  return data3

def printSumWeight(name,data, dataN):
  sumweight= data['semileptonic']+data['dileptonic']+data['hadroic']
  print name+" : "+str(sumweight)
  dataN[name]=sumweight

def main():
  from pdfAllRun import roudV,sumV,printV,getSys,PrintSys#,compareSYS
  from Q2scale import *

  print "> python Q2scaleRun2.py > resultQ2scaleSys.txt"
  print ""
  print 'POW'
  POW2=printV(POW,True)
  print ""
  print ""
  print "Down"
  dwPOWnom=printV(dwPOW['nom']['dwPOW'],False)
  dwnomSys=PrintSys2(POW2,dwPOWnom)
  dwPOWmax=compareSYS(dwnomSys,dwnomSys)
  print "+Central Sample"
  for i in range(1,4):
    print "++Q2_Dw"+str(i)
    dwPOW3=printV(POWsys['Q2_Dw'+str(i)],False)
    dwPOWsys=PrintSys2(POW2,dwPOW3)
    dwPOWmax=compareSYS(dwPOWmax,dwPOWsys)

  print ""
  print "+ME Down Sample"
  for i in range(1,4):
    print "++Q2_Dw"+str(i)
    dwPOW3=printV(dwPOW['Q2_Dw'+str(i)]['dwPOW'],False)
    dwPOWsys=PrintSys2(POW2,dwPOW3)
    dwPOWmax=compareSYS(dwPOWmax,dwPOWsys)

  print "dwPOWmax : "+str(dwPOWmax)

  print ""
  print "Up"
  upPOWnom=printV(upPOW['nom']['upPOW'],False)
  upnomSys=PrintSys2(POW2,upPOWnom)
  upPOWmax=compareSYS(upnomSys,upnomSys)
  print "+Central Sample"
  for i in range(1,4):
    print "++Q2_Up"+str(i)
    upPOW3=printV(POWsys['Q2_Up'+str(i)],False)
    upPOWsys=PrintSys2(POW2,upPOW3)
    upPOWmax=compareSYS(upPOWmax,upPOWsys)

  print ""
  print "+ME Up Sample"
  for i in range(1,4):
    print "++Q2_Up"+str(i)
    upPOW3=printV(upPOW['Q2_Up'+str(i)]['upPOW'],False)
    upPOWsys=PrintSys2(POW2,upPOW3)
    upPOWmax=compareSYS(upPOWmax,upPOWsys)

  print "upPOWmax : "+str(upPOWmax)

  print ""
  print "sysPOWmax:"
  print compareSYS(upPOWmax,dwPOWmax)
  
if __name__ == "__main__":
    test=main()

