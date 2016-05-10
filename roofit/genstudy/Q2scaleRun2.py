
def PrintSys2(data,data2):
  return PrintSys3(data,data2,True)

def PrintSys3(data,data2,isPrint):
  from pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
  sysRvs=getSys(data['rVS'],data2['rVS'])
  sysRfs=getSys(data['rFS'],data2['rFS'])
  sysTtbbEff=getSys(data['Eff']["ttbb"],data2['Eff']['ttbb'])
  sysTtjjEff=getSys(data['Eff']["ttjj"],data2['Eff']['ttjj'])

  sysRtjtFS=getSys(data['rTtjjTotal']['FS'],data2['rTtjjTotal']['FS'])
  sysRtjtVS=getSys(data['rTtjjTotal']['VS'],data2['rTtjjTotal']['VS'])
  sysRtjtS6=getSys(data['rTtjjTotal']['S6'],data2['rTtjjTotal']['S6'])
  if isPrint:
    print "++sys rVS : "+str(roudV(sysRvs)*100)+" %"
    print "++sys rFS : "+str(roudV(sysRfs)*100)+" %"
    print "++sys rTtjjTotalFS : "+str(roudV(sysRtjtFS)*100)+" %"
    print "++sys rTtjjTotalVS : "+str(roudV(sysRtjtVS)*100)+" %"
    print "++sys rTtjjTotalS6 : "+str(roudV(sysRtjtS6)*100)+" %"
    #print "sys rFS : "+str(roudV(sysRfs)*100)+" %"
    #print "sys ttbb Eff : "+str(roudV(sysTtbbEff)*100)+" %"
    #print "sys ttjj Eff : "+str(roudV(sysTtjjEff)*100)+" %"

  return {"rFS":abs(sysRfs),"rVS":abs(sysRvs),"kFS":abs(sysRtjtFS),"kVS":abs(sysRtjtVS),"kS6":abs(sysRtjtS6)}


def main():
  from pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
  from Q2scale import *
  print 'POW'
  POW2=printV(POW,True)
  print ""
  print ""
  print "Down"
  #dwPOWnom=printV(dwPOW['nom']['dwPOW'],False)
  nomSys=PrintSys3(POW2,POW2,False)
  dwPOWmax=compareSYS(nomSys,nomSys)
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
#  upPOWnom=printV(upPOW['nom']['upPOW'],False)
#  upPOWnomSys=PrintSys2(POW2,upPOWnom)
  upPOWmax=compareSYS(nomSys,nomSys)
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

