

def main():
  from pdfAllRun import roudV,printV 
  from Q2scaleRun3 import getRttjjttbb,getSys,printSys,compareSYS,printAccEff,printV2

  from Q2scale import *
  from genFPSAllchannel import POWAcc,AMCAcc,MG5Acc 

  RFit = 0.0557405348697
  NttjjFit = 926.771624879
  lumi = 2318.278305882 

  #print "> python genMCsys.py > resultMCsys.txt"
  #print ""

  print 'POW'
  POW2=printV2(POW,POWAcc,False)
  POW3=getRttjjttbb(POW2,RFit,NttjjFit,lumi)
  print str(POW3)
  POW4={}
  POW4["data"]=POW2
  POW4["data2"]=POW3
  #maxSys=printSys(POW3,POW,RFit,NttjjFit,lumi)
 
  #print ""
  #print "AMC"
  AMCSys=printSys(POW3,AMC['nom']['AMC'],AMCAcc,RFit,NttjjFit,lumi)
  printAccEff("AMC",AMCSys,POW4)
  print AMCSys["data2"]

  #print ""
  #print "MG5"
  MG5Sys= printSys(POW3,MG5['nom']['MG5'],MG5Acc,RFit,NttjjFit,lumi)
  printAccEff("MG5",MG5Sys,POW4)
  print MG5Sys["data2"]

  #print ""
  #print "POHP"
  #POHPSys= printSys(POW3,POHP['nom']['POHP'],RFit,NttjjFit,lumi)
  #printAccEff("POW\_HERWIG++",POHPSys,POW4)


if __name__ == "__main__":
    test=main()

