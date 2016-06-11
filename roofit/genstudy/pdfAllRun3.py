
def sumSYS(data,data2):
  import math
  dataAll={}
  for x in data.keys():
    data3={}
    for y in data[x].keys():
      data3[y]= math.sqrt(( data[x][y])*(data[x][y]) + (data2[x][y]*data2[x][y]) )
    dataAll[x]=data3 
  return dataAll



def main():
  from pdfAll import *
  from pdfAllRun import roudV,printV 
  from Q2scaleRun3 import getRttjjttbb,getSys,printSys,compareSYS

  RFit = 0.0557405348697
  NttjjFit = 926.771624879
  lumi = 2318.278305882 

  #print "> python Q2scaleRun2.py > resultQ2scaleSys.txt"
  #print ""
  print 'POW'
  POW2=printV(POW,False)
  POW3=getRttjjttbb(POW2,RFit,NttjjFit,lumi)
  print str(POW3)
  maxSys=printSys(POW3,POW,RFit,NttjjFit,lumi)
 
  print ""
  print "PDF"

  for i in range(0,100):
    bbb= 'pdf_N'+str(i)
    print "+"+str(bbb)
    pdfI = eval(bbb)
    Sys=printSys(POW3,pdfI[bbb]['POW'],RFit,NttjjFit,lumi)
    maxSys=compareSYS(maxSys,Sys)

  print maxSys


if __name__ == "__main__":
    test=main()

