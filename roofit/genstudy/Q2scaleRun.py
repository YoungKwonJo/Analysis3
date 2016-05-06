

def main():
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

  print upPOWmax

  print "total:"
  print compareSYS(upPOWmax,dwPOWmax)

if __name__ == "__main__":
    test=main()

