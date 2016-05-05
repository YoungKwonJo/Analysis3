

#Acceptance
#Efficiency
def roudV(val):
  if val > 100 :
    return int(round(val))
  elif val > 1 : 
    return round(val*100)/100
  else :
    nom=10000.
    if val>0.1    : nom=10000.
    elif val>0.01 : nom=100000.
    elif val>0.001: nom=1000000.
    else          : nom=100000000.

    return round(val*nom)/nom

def sumV(data,step,candi):
  sumV =0.
  if step == "": 
    for i in candi:  sumV +=data[i] 
  else         : 
    for i in candi:  sumV +=data[step][i]
  return sumV

def printV(data,isPrint):
  total = sumV(data,"",['dileptonic','semileptonic','hadroic'])
  if isPrint : print "total : "+str(total)
  if isPrint : print "dileptonic : "+str(data['dileptonic'])+", semileptonic : "+str(data['semileptonic'])+", hadroic : "+str(data['hadroic'])
  VS = ["ttbb","tt2b","ttb","ttcc","ttlf"]# "ttot"
  FS = ["ttbbF","ttbF","ttccF","ttlfF"]
  ttbb = data['S0']['ttbb']
  ttbbF = data['S0']['ttbbF']
  ttjj = sumV(data,'S0',VS)
  ttjjF = sumV(data,'S0',FS)
  ttbbAcc=ttbb/ttbbF
  ttjjAcc=ttjj/ttjjF
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

def getSys(a,b):
  return (a-b)/a

def PrintSys(data,data2):
  sysRvs=getSys(data['rVS'],data2['rVS'])
  sysRfs=getSys(data['rFS'],data2['rFS'])
  sysTtbbEff=getSys(data['Eff']["ttbb"],data2['Eff']['ttbb'])
  sysTtjjEff=getSys(data['Eff']["ttjj"],data2['Eff']['ttjj'])

  sysRtjtFS=getSys(data['rTtjjTotal']['FS'],data2['rTtjjTotal']['FS'])
  sysRtjtVS=getSys(data['rTtjjTotal']['VS'],data2['rTtjjTotal']['VS'])
  sysRtjtS6=getSys(data['rTtjjTotal']['S6'],data2['rTtjjTotal']['S6'])

  print "sys rVS : "+str(roudV(sysRvs)*100)+" %"
  print "sys rTtjjTotalFS : "+str(roudV(sysRtjtFS)*100)+" %"
  print "sys rTtjjTotalVS : "+str(roudV(sysRtjtVS)*100)+" %"
  print "sys rTtjjTotalS6 : "+str(roudV(sysRtjtS6)*100)+" %"
  #print "sys rFS : "+str(roudV(sysRfs)*100)+" %"
  #print "sys ttbb Eff : "+str(roudV(sysTtbbEff)*100)+" %"
  #print "sys ttjj Eff : "+str(roudV(sysTtjjEff)*100)+" %"

  return {"rVS":abs(sysRvs),"kFS":abs(sysRtjtFS),"kVS":abs(sysRtjtVS),"kS6":abs(sysRtjtS6)}

def compareSYS(data,data2):
  data3={}
  data3['rVS']=max(data["rVS"],data2["rVS"])
  data3['kFS']=max(data["kFS"],data2["kFS"])
  data3['kVS']=max(data["kVS"],data2["kVS"])
  data3['kS6']=max(data["kS6"],data2["kS6"])
  return data3


#['Q2_Dw3', 'nom', 'Q2_Dw1', 'Q2_Dw2', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']
#['dwPOW', 'POW', 'AMC', 'POHP', 'MG5', 'upPOW']
#['semileptonic', 'dileptonic', 'S0', 'S7', 'S6', 'etc', 'hadroic']
#{'ttbbF': 2838.0, 'ttbF': 4276.0, 'ttlfF': 62138.0, 'ttotF': 1874.0, 'ttccF': 3056.0, 'ttb': 4127.0, 'ttlf': 59498.0, 'ttbb': 2206.0, 'ttot': 6077.0, 'ttcc': 2659.0, 'tt2bF': 1905.0, 'tt2b': 1520.0}
from pdfAll import *

print 'POW'
POW2=printV(POW,True)
print ""
print "PDF"
POW0=PrintSys(POW2,POW2)
data31=compareSYS(POW0,POW0)
#for i in range(0,212):
for i in range(0,100):
  bbb= 'pdf_N'+str(i)
  pdfI = eval(bbb)
  aaa=printV(pdfI[bbb]['POW'],False)
  ccc=PrintSys(POW2,aaa)
  data31=compareSYS(data31,ccc)

print data31


