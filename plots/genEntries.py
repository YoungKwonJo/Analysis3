from ROOT import *
from mcsample_cfi import *

def mAND(aaa,bbb):
  return "(" +aaa+ " && "+bbb+")"

def getDictionary(tree, name, name2, vvv, sel1, sel2, description):
  htemp = TH1D("htemp"+name+name2,"",1,-20,20)
  tree.Project("htemp"+name+name2,vvv,sel1)
  bbbb=description+" events,(sumweights): "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  selection1_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
###########
  htemp.Reset()
  tree.Project("htemp"+name+name2,vvv,sel2)
  print bbbb+", S6: "+str(int(htemp.GetEntries()))+", "+str(int(htemp.Integral()))
  selection2_={"events":htemp.GetEntries(),"integral":htemp.Integral()}
  return {"GEN":selection1_,"S6":selection2_, "eff1":selection2_["events"]/selection1_["events"], "eff2":selection2_["integral"]/selection1_["integral"]}  

def ntuple2entries(files,name):
  vvv = "1"#"(weight)/abs(weight)"
  #tt="(1)"
  tt="(weight/abs(weight))"
  #if name.find("aMC")>-1 :   tt ="(weight/abs(weight))"
  visible="(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)"
  ttjj = visible
  ttbb = mAND("(NbJets20>=4)",visible)
  ttb = mAND("(NbJets20==3)",visible)
  ttcc = mAND("((NcJets20>=2) && !(NbJets20>=3))",visible)
  ttlf = mAND("(!(NbJets20>=4) && !(NbJets20==3) && !(NcJets20>=2))",visible)

  #dileptonic ="(diLeptonicMuoMuo ==1 ||  diLeptonicMuoEle ==1 ||  diLeptonicEleEle ==1 ||  diLeptonicTauMuo ==1 ||  diLeptonicTauEle ==1 ||  diLeptonicTauTau ==1 )"
  dileptonic ="(allHadronic != 1 && semiLeptonic != 1)"

  fullphaseTTBB="("+dileptonic+" && NaddbJets20 >= 2)"
  fullphaseTTJJ="("+dileptonic+" && NaddJets20 >= 2)"
  old="""
  ttjj = "(partonInPhaseLep==1 && NgenJet>=4 )"
  ttbb = "("+ttjj+"&&"+"(genTtbarId%100>52))"
  ttb  = "("+ttjj+"&&"+"(genTtbarId%100>50 && genTtbarId%100<53))"
  ttcc = "("+ttjj+"&&"+"(genTtbarId%100>42 && genTtbarId%100<49))"
  ttc  = "("+ttjj+"&&"+"(genTtbarId%100>40 && genTtbarId%100<43))"
  ttlf = "("+ttjj+"&&"+"(genTtbarId%100 ==0))"
  """

  trigger = "((channel==3||(channel==2)||(channel==1)) && (tri==1)&&(filtered==1))"
  #S1 = trigger+"&&( (step1==1) &&((channel==3)&&(lep1_RelIso<0.15 && lep2_RelIso<0.15)) ||((channel==2)&&(lep1_RelIso<0.12 && lep2_RelIso<0.12)) ||((channel==1)&&(lep1_RelIso<0.12 && lep2_RelIso<0.15)) )"
  S1 = trigger+"&&( (step1==1) && ((channel==3) ||(channel==2) ||(channel==1)) )"
  S6 = "("+S1+"&&(step2==1)&&(step3==1)&&(step4==1)&&(step5==1))"

  chain = TChain("cattree/nom")
  for afile in files:
    f = TFile.Open(afile)
    if None == f: continue
    chain.Add(afile)
  tree = chain
  summary = {}

  summary['total']=getDictionary(tree, "total", "2", vvv, tt,          tt+"*"+S6,          "total ")
  summary['ttjj'] =getDictionary(tree, "ttjj",  "2", vvv, tt+"*"+ttjj, tt+"*"+ttjj+"*"+S6, "ttjj ")
  summary['ttbb'] =getDictionary(tree, "ttbb",  "2", vvv, tt+"*"+ttbb, tt+"*"+ttbb+"*"+S6, "ttbb ")
  summary['ttb']  =getDictionary(tree, "ttb",   "2", vvv, tt+"*"+ttb,  tt+"*"+ttb+"*"+S6,  "ttb ")
  summary['ttcc'] =getDictionary(tree, "ttcc",  "2", vvv, tt+"*"+ttcc, tt+"*"+ttcc+"*"+S6, "ttcc ")
  summary['ttlf'] =getDictionary(tree, "ttlf",  "2", vvv, tt+"*"+ttlf, tt+"*"+ttlf+"*"+S6, "ttlf ")

  summary["ratio"]={"events":summary["ttbb"]["GEN"]["events"]/summary["ttjj"]["GEN"]["events"],"integral":summary["ttbb"]["GEN"]["integral"]/summary["ttjj"]["GEN"]["integral"],"eventsS6":summary["ttbb"]["S6"]["events"]/summary["ttjj"]["S6"]["events"],"integralS6":summary["ttbb"]["S6"]["integral"]/summary["ttjj"]["S6"]["integral"]}
  
  #summary['fullphaseTTBB']=getDictionary(tree, "fullphaseTTBB", "2", vvv, tt+"*"+fullphaseTTBB, tt+"*"+fullphaseTTBB+"*"+S6, "fullphaseTTBB ")
  #summary['fullphaseTTJJ']=getDictionary(tree, "fullphaseTTJJ", "2", vvv, tt+"*"+fullphaseTTJJ, tt+"*"+fullphaseTTJJ+"*"+S6, "fullphaseTTJJ ")
  #summary["ratio2"]={"events":summary["fullphaseTTBB"]["GEN"]["events"]/summary["fullphaseTTJJ"]["GEN"]["events"],"integral":summary["fullphaseTTBB"]["GEN"]["integral"]/summary["fullphaseTTJJ"]["GEN"]["integral"],"eventsS6":summary["fullphaseTTBB"]["S6"]["events"]/summary["fullphaseTTJJ"]["S6"]["events"],"integralS6":summary["fullphaseTTBB"]["S6"]["integral"]/summary["fullphaseTTJJ"]["S6"]["integral"]}
  return summary


ttbarMG5 = "TTJets_MG5"
ttbarAMC = "TTJets_aMC"
ttbarPOW = "TT_powheg"
loc = "/store/user/youngjo/Cattools/v7-6-1v3/"
z="v2"#GenTop"

mg5=ntuple2entries(files(loc + ttbarMG5+z),ttbarMG5)
#amc=ntuple2entries(files(loc + ttbarAMC+z),ttbarAMC)
#pow=ntuple2entries(files(loc + ttbarPOW+z),ttbarPOW)

allsummary={}
allsummary["MG5"]=mg5
#allsummary["AMC"]=amc
#allsummary["POW"]=pow

print str(allsummary)

for j  in allsummary.keys():
  print j
  for i  in allsummary[j].keys():
    if i.find("ratio")==-1:
      print i+"  &  "+str(int(allsummary[j][i]["GEN"]["events"]))+"  &  "+str(int(allsummary[j][i]["S6"]["events"]))+" & "+str(round(allsummary[j][i]["eff1"]*100000)/1000)+"\%  \\\\ "
  print " &"+str(round(allsummary[j]["ratio"]["events"]*100000)/1000)+" \% &  "+str(round(allsummary[j]["ratio"]["eventsS6"]*100000)/1000)+" \% &  \\\\ "

for j  in allsummary.keys():
  print j
  for i  in allsummary[j].keys():
    if i.find("ratio")==-1:
      print i+"  &  "+str(int(allsummary[j][i]["GEN"]["integral"]))+"  &  "+str(int(allsummary[j][i]["S6"]["integral"]))+" & "+str(round(allsummary[j][i]["eff2"]*100000)/1000)+"\%  \\\\ "
  print " &"+str(round(allsummary[j]["ratio"]["integral"]*100000)/1000)+" \%  &  "+str(round(allsummary[j]["ratio"]["integralS6"]*100000)/1000)+" \% &  \\\\ "



