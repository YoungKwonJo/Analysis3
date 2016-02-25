from ROOT import *
import copy
from array import array
from math import sqrt

################
from loadHistograms import lumi,loc 

###################################################

DYsf = {
"kMM":0.600490703126,
"kEE":0.416326179071,
# "kMM" : 0.600653370713,
# "kEE" : 0.416213430557,
  # EE MM
"S2":(1.0,1.0),
"S3":(0.935392718148,0.893447803495),
"S4":(1.00991020557,0.923236455098),
"S5":(1.17276976842,0.864208578682),
"S6":(1.17276976842,0.864208578682),
"S7":(1.17276976842,0.864208578682)
#"S3":(0.947060873954,0.862619078979),
#"S4":(1.01894001698,0.888697458327),
#"S5":(1.14618572215,0.844371813284),
#"S6":(1.14618572215,0.844371813284)
}
"""
#DATE : 2016.02.24. v7-6-3 
    kMM=0.600490703126
    kEE=0.416326179071
    step : S3
Rout/in MM: 0.0943465891907, EE:0.0870808099669
SF MM: 0.893447803495, EE:0.935392718148
"S3":(0.935392718148,0.893447803495)
    kMM=0.600490703126
    kEE=0.416326179071
    step : S4
Rout/in MM: 0.106339424998, EE:0.0973279293949
SF MM: 0.923236455098, EE:1.00991020557
"S4":(1.00991020557,0.923236455098)
    kMM=0.600490703126
    kEE=0.416326179071
    step : S5
Rout/in MM: 0.102812784359, EE:0.110635521683
SF MM: 0.864208578682, EE:1.17276976842
"S5":(1.17276976842,0.864208578682)
################
#DATE : 2016.02.15 
    kMM=0.596276082525
    kEE=0.419268871127
    step : S3
Rout/in MM: 0.0937115897632, EE:0.0892321694339
SF MM: 0.862619078979, EE:0.947060873954
"S3":(0.947060873954,0.862619078979)
    step : S4
Rout/in MM: 0.10576383469, EE:0.0985434656777
SF MM: 0.888697458327, EE:1.01894001698
"S4":(1.01894001698,0.888697458327)
    step : S5
Rout/in MM: 0.112281452718, EE:0.103372481597
SF MM: 0.844371813284, EE:1.14618572215
"S5":(1.14618572215,0.844371813284)
"""


def drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out,
                       rd_ee_in, rd_mm_in, rd_em_in,kMM,kEE,step):    

    print "    kMM="+str(kMM)
    print "    kEE="+str(kEE)

    rMC_mm = mc_mm_out/mc_mm_in
    rMC_ee = mc_ee_out/mc_ee_in
    print "    step : "+step
    print "Rout/in MM: "+str(rMC_mm)+", EE:"+str(rMC_ee)
    nOutEst_mm = rMC_mm*(rd_mm_in - rd_em_in*kMM)
    nOutEst_ee = rMC_ee*(rd_ee_in - rd_em_in*kEE)
    print "SF MM: "+str(nOutEst_mm/mc_mm_out)+", EE:"+str(nOutEst_ee/mc_ee_out)

    print "\""+step+"\":("+str(nOutEst_ee/mc_ee_out)+","+str(nOutEst_mm/mc_mm_out)+")"
    return nOutEst_ee/mc_ee_out,nOutEst_mm/mc_mm_out

#####################
def drellYanEstimationRun(f,step, mcsamples, datas):
 
  step=step.replace("mm_","")
  step=step.replace("ee_","")
  step=step.replace("em_","")
  #mcs = ["DYJets","DYJets10"]
  #mcxs = [6025.2,18610.0]
  #datas = ["1","2"]

  hrdeein_s2 = TH1D("rd_ee_in_s2","",60,0,300)
  hrdmmin_s2 = TH1D("rd_mm_in_s2","",60,0,300)

  hmceein = TH1D("mc_ee_in","",60,0,300)
  hmcmmin = TH1D("mc_mm_in","",60,0,300)
  hmcemin = TH1D("mc_em_in","",60,0,300)

  hmceeout = TH1D("mc_ee_out","",60,0,300)
  hmcmmout = TH1D("mc_mm_out","",60,0,300)

  hrdeein = TH1D("rd_ee_in","",60,0,300)
  hrdmmin = TH1D("rd_mm_in","",60,0,300)
  hrdemin = TH1D("rd_em_in","",60,0,300)


  for i,mc in enumerate(mcsamples) :
    name = mc["name"]
    cx = mc["cx"]
    inee =  name+"/CEN/"+"/h1_"+name+"_ZMass_ee_"+step+"_in"
    h1=f.Get(inee).Clone("hhhh_ee_"+name) 
    h1.Scale(lumi*cx)
    hmceein.Add(h1)

    inmm = name+"/CEN/"+"/h1_"+name+"_ZMass_mm_"+step+"_in"
    h2=f.Get(inmm).Clone("hhhh_mm_"+name) 
    h2.Scale(lumi*cx)
    hmcmmin.Add(h2)

    inem = name+"/CEN/"+"/h1_"+name+"_ZMass_em_"+step+"_in"
    h3=f.Get(inem).Clone("hhhh_em_"+name) 
    h3.Scale(lumi*cx)
    hmcemin.Add(h3)

    outee = name+"/CEN/"+"/h1_"+name+"_ZMass_ee_"+step+"_out"
    h11=f.Get(outee).Clone("hhhh_ee_"+name) 
    h11.Scale(lumi*cx)
    hmceeout.Add(h11)

    outmm = name+"/CEN/"+"/h1_"+name+"_ZMass_mm_"+step+"_out"
    h22=f.Get(outmm).Clone("hhhh_mm_"+name) 
    h22.Scale(lumi*cx)
    hmcmmout.Add(h22)

  for data in datas :
    eein = "ElEl"+data+"/CEN/"+"/h1_ElEl"+data+"_ZMass_ee_"+step+"_in"
    h1=f.Get(eein).Clone("hhhh_rd_ee"+data)
    hrdeein.Add(h1)

    mmin = "MuMu"+data+"/CEN/"+"/h1_MuMu"+data+"_ZMass_mm_"+step+"_in"
    h2=f.Get(mmin).Clone("hhhh_rd_mm"+data)
    hrdmmin.Add(h2)

    emin = "MuEl"+data+"/CEN/"+"/h1_MuEl"+data+"_ZMass_em_"+step+"_in"
    h3=f.Get(emin).Clone("hhhh_rd_em"+data)
    hrdemin.Add(h3)

    eein2 = "ElEl"+data+"/CEN/"+"/h1_ElEl"+data+"_ZMass_ee_S2_in"
    h12=f.Get(eein2).Clone("hhhh_rd_ee_s2"+data)
    hrdeein_s2.Add(h12)

    mmin2 = "MuMu"+data+"/CEN/"+"/h1_MuMu"+data+"_ZMass_mm_S2_in"
    h22=f.Get(mmin2).Clone("hhhh_rd_mm_s2"+data)
    hrdmmin_s2.Add(h22)


  mc_ee_in   = hmceein.Integral()
  mc_ee_out  = hmceeout.Integral()
  mc_mm_in   = hmcmmin.Integral()
  mc_mm_out  = hmcmmout.Integral()
  rd_ee_in   = hrdeein.Integral()
  rd_mm_in   = hrdmmin.Integral()
  rd_em_in   = hrdemin.Integral()
  rd_ee_in_s2   = hrdeein_s2.Integral()
  rd_mm_in_s2   = hrdmmin_s2.Integral()
  kMM = sqrt(rd_mm_in_s2/rd_ee_in_s2)/2.
  kEE = sqrt(rd_ee_in_s2/rd_mm_in_s2)/2.
 
  return drellYanEstimation(mc_ee_in, mc_ee_out, mc_mm_in, mc_mm_out, rd_ee_in, rd_mm_in, rd_em_in,kMM,kEE,step)
 
def main():
  from mcsample_cfi import mcsamples2
  filename="hist_CEN.root"
  f = TFile.Open(loc+filename,"read")

  drellYanEstimationRun(f,"S3",mcsamples2,["1","2"])
  drellYanEstimationRun(f,"S4",mcsamples2,["1","2"])
  drellYanEstimationRun(f,"S5",mcsamples2,["1","2"])

  return False

if __name__ == "__main__":
  test=main()

