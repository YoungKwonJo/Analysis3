

#Acceptance
#Efficiency
#['Q2_Dw3', 'nom', 'Q2_Dw1', 'Q2_Dw2', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']
#['dwPOW', 'POW', 'AMC', 'POHP', 'MG5', 'upPOW']
#['semileptonic', 'dileptonic', 'S0', 'S7', 'S6', 'etc', 'hadroic']
#{'ttbbF': 2838.0, 'ttbF': 4276.0, 'ttlfF': 62138.0, 'ttotF': 1874.0, 'ttccF': 3056.0, 'ttb': 4127.0, 'ttlf': 59498.0, 'ttbb': 2206.0, 'ttot': 6077.0, 'ttcc': 2659.0, 'tt2bF': 1905.0, 'tt2b': 1520.0}
from pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
from Q2scale import *

print 'POW'
POW2=printV(POW,True)
print ""
print "AMC"
AMC2=printV(AMC['nom']['AMC'],True)
PrintSys(POW2,AMC2)
print ""
print "MG5"
MG52=printV(MG5['nom']['MG5'],True)
PrintSys(POW2,MG52)

print ""
print "POHP"
POHP2=printV(POHP['nom']['POHP'],True)
PrintSys(POW2,POHP2)


print ""
print "Down"
dwPOWnom=printV(dwPOW['nom']['dwPOW'],False)
dwPOWnomSys=PrintSys(POW2,dwPOWnom)
dwPOWmax=compareSYS(dwPOWnomSys,dwPOWnomSys)
for i in range(1,4):
  dwPOW3=printV(dwPOW['Q2_Dw3']['dwPOW'],False)
  dwPOWsys=PrintSys(POW2,dwPOW3)
  dwPOWmax=compareSYS(dwPOWmax,dwPOWsys)

#dwPOW2=printV(dwPOW['Q2_Dw2']['dwPOW'],False)
#PrintSys(POW2,dwPOW2)
#dwPOW1=printV(dwPOW['Q2_Dw1']['dwPOW'],False)
#PrintSys(POW2,dwPOW1)
print dwPOWmax

print ""
print "Up"
upPOWnom=printV(upPOW['nom']['upPOW'],False)
upPOWnomSys=PrintSys(POW2,upPOWnom)
upPOWmax=compareSYS(upPOWnomSys,upPOWnomSys)
for i in range(1,4):
  upPOW3=printV(upPOW['Q2_Up3']['upPOW'],False)
  upPOWsys=PrintSys(POW2,upPOW3)
  upPOWmax=compareSYS(upPOWmax,upPOWsys)

#upPOW2=printV(upPOW['Q2_Up2']['upPOW'],False)
#PrintSys(POW2,upPOW2)
#upPOW1=printV(upPOW['Q2_Up1']['upPOW'],False)
#PrintSys(POW2,upPOW1)

print upPOWmax

print "total:"
print compareSYS(upPOWmax,dwPOWmax)

