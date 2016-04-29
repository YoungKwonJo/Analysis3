from ROOT import *
import copy
from array import array
from math import sqrt

log = False
#log = True
#aMC=["AMCttbb","AMCttb","AMCttc","AMCttcc","AMCttlf","AMCttot","TTWlNu","TTWqq","TTZll","TTZqq","DYJets","DYJets10","WJets"]

######################
def h1_maker(tree, mon, cut):
  h1 =  TH1D( mon['name'], mon['title'], mon['xbin_set'][0],mon['xbin_set'][1],mon['xbin_set'][2])
  h1.GetXaxis().SetTitle(mon['x_name'])
  h1.GetYaxis().SetTitle(mon['y_name'])
  h1.Sumw2()
  tree.Project(mon['name'],mon['var'],cut)
  if mon['name'].find("Stat")>-1:
    print " Stat: "+mon['name']+" = "+str(h1.GetBinContent(1))+" +- "+str(h1.GetBinError(1)) 
  return h1  

def h1_set(name,monitor,cutname):
  mon = {  "name" : "h1_"+name+"_"+monitor['name']+"_"+cutname, "title" : name+" "+monitor['var'],
           "var" : monitor['var'],            "xbin_set" : monitor['xbin_set'],
           "x_name": monitor['unit'], "y_name": "Entries"
        }
  return mon

######################
def h2_maker(tree, mon, cut):
  h2 =  TH2F( mon['name'], mon['title'], mon['xbin_set'][0],mon['xbin_set'][1],mon['xbin_set'][2], mon['ybin_set'][0],mon['ybin_set'][1],mon['ybin_set'][2])
  h2.GetXaxis().SetTitle(mon['x_name'])
  h2.GetYaxis().SetTitle(mon['y_name'])
  h2.Sumw2()
  tree.Project(mon['name'],mon['var'],cut)
  return h2  

def h2_set(name,monitor,monitor2,cutname):
  mon = {  "name" : "h2_"+name+"_"+monitor['name']+"_"+monitor2['name']+"_"+cutname, "title" : name+" "+monitor['var']+" vs "+monitor2['var'],
           "var" : monitor2['var']+":"+monitor['var'],         
           "xbin_set" : monitor['xbin_set'], "ybin_set" : monitor2['xbin_set'],
           "x_name": monitor['unit'], "y_name": monitor2['unit']
        }
  return mon

######################
######################
def h_all_maker(tree2,mc, monitors, cuts, eventweight,Ntot,hN_maker):
  hh = {}
  h=[]
  aWeight=eventweight["name"]
  for cutname in cuts["cut"]:
    for i,ii in enumerate(monitors):
      mon = h1_set(mc['name'],monitors[i],cuts["channel"]+"_"+cutname+"_"+aWeight)
      if hN_maker is h2_maker : 
        if i+1 < len(monitors) and len(monitors) > 1 : mon = h2_set(mc['name'],monitors[i],monitors[i+1],cuts["channel"]+"_"+cutname+"_"+aWeight)
        else  : continue
      cut = "("+cuts["cut"][cutname]+" * "+mc['selection'] +")*("+eventweight["var"]+"/"+str(Ntot)+")"

      h2 = hN_maker(tree2,mon,cut)
      h.append(copy.deepcopy(h2))

      #making shape for dy estimation
      if monitors[i]['name'].find("ZMass")>-1 and ((mc['name'].find("DYJets")>-1) or (mc['name'].find("Mu")>-1) or (mc['name'].find("El")>-1)) and aWeight is "CEN" :
        incut = "((ll_m > 76) * (ll_m < 106))"
        outcut ="(!((ll_m > 76) * (ll_m < 106)))"
        monIN = h1_set(mc['name'],monitors[i], cuts["channel"]+"_"+cutname+"_in")
        monOUT = h1_set(mc['name'],monitors[i],cuts["channel"]+"_"+cutname+"_out")
        newCut = cuts["cut"][cutname].replace("* (step2==1)","")
        cutIN = "("+newCut+" * "+incut+" * "+mc['selection'] +")*("+eventweight["var"]+"/"+str(Ntot)+")"
        cutOUT = "("+newCut+" * "+outcut+" * "+mc['selection'] +")*("+eventweight["var"]+"/"+str(Ntot)+")"
        if(cutname.find("S0")>-1 or cutname.find("S1")>-1 ):
          continue
        else :
          h1 = h1_maker(tree2,monIN,cutIN)
          h.append(copy.deepcopy(h1))
          h2 = h1_maker(tree2,monOUT,cutOUT)
          h.append(copy.deepcopy(h2))
          print "  "+mc['name']+" \n "+newCut+" \n "+monIN["name"]+" , "+monOUT["name"]

  hh[eventweight["name"]]=copy.deepcopy(h)

  return hh


####################
####################
####################


def ntuple2hist(json,cuts,mcweight,mon,hN_maker):
  h = {}
  mcsamples = json['mcsamples']
  #mceventweight = json[mcweight]
  mceventweight = json['mceventweight']
  #monitors=json['monitors']
  monitors=json[mon]
  datasamples = json['datasamples']
  aWeight=mceventweight["name"]
  nom2 = "cattree/nom2"
  if   aWeight.find("JER_Up")>-1:    nom2 = "cattree/nomJER_up"
  elif aWeight.find("JER_NOM")>-1:   nom2 = "cattree/nomJER_n"
  elif aWeight.find("JER_Down")>-1:  nom2 = "cattree/nomJER_dw"
  elif aWeight.find("JES_Up")>-1:    nom2 = "cattree/nomJES_up"
  elif aWeight.find("JES_Down")>-1:  nom2 = "cattree/nomJES_dw"
  elif aWeight.find("Mu_Up")>-1:    nom2 = "cattree/nomMu_up"
  elif aWeight.find("Mu_Down")>-1:  nom2 = "cattree/nomMu_dw"
  elif aWeight.find("El_Up")>-1:    nom2 = "cattree/nomEl_up"
  elif aWeight.find("El_Down")>-1:  nom2 = "cattree/nomEl_up"
  else :                            nom2 = "cattree/nom2"

  for i,mc in enumerate(mcsamples):
    #chain = TChain("cattree/nom")
    chain2 = TChain(nom2)
    for afile in mcsamples[i]['file']:
      f = TFile.Open(afile)
      if None == f: continue
      #chain.Add(afile)
      chain2.Add(afile)
    #tree = chain
    tree2 = chain2

    #htemp = TH1D("htemp"+mcsamples[i]['name'],"",1,-2,2)
    #tree.Project("htemp"+mcsamples[i]['name'],"1","weight")#/abs(weight)")
    #Ntot = htemp.GetBinContent(1)
    Ntot = mc["sumWeight"]
    h[mcsamples[i]['name']]=h_all_maker(tree2,mcsamples[i],monitors,cuts,mceventweight,Ntot,hN_maker)
    #f.Close()

  if nom2 in ["cattree/nom2","cattree/nomJES_up","cattree/nomJES_dw"]:
    for i,mc in enumerate(datasamples):
      #chain = TChain("cattree/nom")
      chain2 = TChain(nom2)
      for afile in datasamples[i]['file']:
        f = TFile.Open(afile)
        if None == f: continue
        #chain.Add(afile)
        chain2.Add(afile)
      #tree = chain
      tree2 = chain2
    
      Ntot = 1 #htot.GetBinContent(1)
      dataweight = {"name":"CEN","var":"(1)"}
      if mceventweight["name"].find("JES_Up")>-1   : dataweight = {"name":"JES_Up","var":"(1)"}
      if mceventweight["name"].find("JES_Down")>-1 : dataweight = {"name":"JES_Down","var":"(1)"}
    
      if mceventweight["name"].find("JES")>-1 or mceventweight["name"].find("CEN")>-1:
        h[datasamples[i]['name']]=h_all_maker(tree2,datasamples[i],monitors,cuts,dataweight,1,hN_maker)
    #f.Close()

  return h


#########################################
#########################################

def makeoutput(outputname, h):
  #fout = TFile("root/"+outputname,"RECREATE")
  fout = TFile(""+outputname,"RECREATE")
  for a in h.keys():
    dirA = fout.mkdir(a)
    dirA.cd()
    for b in h[a].keys():
      dirB = dirA.mkdir(b)
      dirB.cd()
      for c in h[a][b]:
        c.Write()
  fout.Write()
  fout.Close()

#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
def makehist(json):
  cuts_  = json['cuts']  
  h={}
  if len(json['monitors'])>0 :
    #h = ntuple2hist(json,cuts_,"mceventweight","monitors",h1_maker)
    h = ntuple2hist(json,cuts_,"monitors",h1_maker)
  if len(json['monitors2'])>0 :
    #h = ntuple2hist(json,cuts_,"mceventweight","monitors2",h2_maker)
    h = ntuple2hist(json,cuts_,"monitors2",h2_maker)
  makeoutput(json['output'],h)

###################################################
###################################################

