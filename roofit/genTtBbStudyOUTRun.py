
from genTtBbStudyOUT import result

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
  if isPrint : print "Acceptance(VS/FS) ttbb : "+str(roudV(ttbbAcc))+", ttjj : "+str(roudV(ttjjAcc))
  if isPrint : print "FS R(ttbb/ttjj) : "+str(roudV(rFS)*100)+" %"
  if isPrint : print "VS R(ttbb/ttjj) : "+str(roudV(rVS)*100)+" %"
  ttbbS6 = data['S6']['ttbb']
  ttjjS6 = sumV(data,"S6",["ttbb","tt2b","ttb","ttcc","ttlf"])
  ttbbEff= ttbbS6/ttbb
  ttjjEff= ttjjS6/ttjj
  if isPrint : print "efficiency S6/S0 in VS"
  if isPrint : print "ttbb : "+str(roudV(ttbbEff)*100)+" %"
  if isPrint : print "ttjj : "+str(roudV(ttjjEff)*100)+" %"

  return {"rFS":rFS,"rVS":rVS,"Acc":{"ttbb":ttbbAcc,"ttjj":ttjjAcc},"Eff":{"ttbb":ttbbEff,"ttjj":ttjjEff}}

def PrintSys(data,data2):
  sysRvs=(data['rVS']-data2['rVS'])/data['rVS']
  sysRfs=(data['rFS']-data2['rFS'])/data['rFS']
  sysTtbbEff=(data['Eff']["ttbb"]-data2['Eff']['ttbb'])/data['Eff']["ttbb"]
  sysTtjjEff=(data['Eff']["ttjj"]-data2['Eff']['ttjj'])/data['Eff']["ttjj"]

  print "sys rVS : "+str(roudV(sysRvs)*100)+" %"
  print "sys rFS : "+str(roudV(sysRfs)*100)+" %"
  #print "sys ttbb Eff : "+str(roudV(sysTtbbEff)*100)+" %"
  #print "sys ttjj Eff : "+str(roudV(sysTtjjEff)*100)+" %"

  

#['Q2_Dw3', 'nom', 'Q2_Dw1', 'Q2_Dw2', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']
#['dwPOW', 'POW', 'AMC', 'POHP', 'MG5', 'upPOW']
#['semileptonic', 'dileptonic', 'S0', 'S7', 'S6', 'etc', 'hadroic']
#{'ttbbF': 2838.0, 'ttbF': 4276.0, 'ttlfF': 62138.0, 'ttotF': 1874.0, 'ttccF': 3056.0, 'ttb': 4127.0, 'ttlf': 59498.0, 'ttbb': 2206.0, 'ttot': 6077.0, 'ttcc': 2659.0, 'tt2bF': 1905.0, 'tt2b': 1520.0}

print 'POW'
POW=printV(result['nom']['POW'],True)
print ""
print "AMC"
AMC=printV(result['nom']['AMC'],True)
PrintSys(POW,AMC)
print ""
print "MG5"
MG5=printV(result['nom']['MG5'],True)
PrintSys(POW,MG5)
print ""
print "Down"
dwPOWnom=printV(result['nom']['dwPOW'],False)
PrintSys(POW,dwPOWnom)
dwPOW3=printV(result['Q2_Dw3']['dwPOW'],False)
PrintSys(POW,dwPOW3)
dwPOW2=printV(result['Q2_Dw2']['dwPOW'],False)
PrintSys(POW,dwPOW2)
dwPOW1=printV(result['Q2_Dw2']['dwPOW'],False)
PrintSys(POW,dwPOW1)

print ""
print "Up"
upPOWnom=printV(result['nom']['upPOW'],False)
PrintSys(POW,upPOWnom)
upPOW3=printV(result['Q2_Up3']['upPOW'],False)
PrintSys(POW,upPOW3)
upPOW2=printV(result['Q2_Up2']['upPOW'],False)
PrintSys(POW,upPOW2)
upPOW1=printV(result['Q2_Up1']['upPOW'],False)
PrintSys(POW,upPOW1)


