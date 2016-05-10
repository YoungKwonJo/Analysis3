

def main():
  from pdfAllRun import roudV,sumV,printV,getSys,PrintSys,compareSYS
  from Q2scale import *
  print "> python genMCsys.py > resultMCsys.txt"
  print ""

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


if __name__ == "__main__":
    test=main()

