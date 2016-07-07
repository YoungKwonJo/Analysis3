from ROOT import *
import copy

def makeoutput(h):
  fout = TFile("output.root","RECREATE")
  for c in h:
    c.Write()
  fout.Write()
  fout.Close()
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
  mon = {  "name" : "h1_"+name+"_"+monitor['name']+"_"+cutname, "title" : name+", "+monitor['exp'],
           "var" : monitor['var'],            "xbin_set" : monitor['xbin_set'],
           "x_name": monitor['unit'], "y_name": "Entries"
        }
  return mon

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


def getList(loc,ls):
  ls2 = []
  for l1 in ls:
    ls2.append(loc+"cattree_"+l1+".root")
  return ls2
#######################
ES = "(((channel==3)||(channel==2)||(channel==1))&& (tri>0)&&(filtered==1))&&((step1==1)&&(step2==1)&&(step3==1)&&(step4==1)&(step5==1))"
ttjjVis = "(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4)  "
ttbbVis = "(NJets20>=4 && NbJets20>=2 && lepton1_pt>20 && lepton2_pt>20 && abs(lepton1_eta)<2.4 && abs(lepton2_eta)<2.4) && (NbJets20>=4) "
mons=[
    { "name":"jet1_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[0]]",  "xbin_set":[50,0,5], "exp":"1st jet CSV order" },
    { "name":"jet2_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[1]]",  "xbin_set":[50,0,5], "exp":"2nd jet CSV order" },
    { "name":"jet3_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[2]]",  "xbin_set":[50,0,5], "exp":"3rd jet CSV order" },
    { "name":"jet4_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[3]]",  "xbin_set":[50,0,5], "exp":"4th jet CSV order" },
]
mon2ds=[
    { "name":"jet1_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[0]]<0.5",  "xbin_set":[2,0,2], "exp":"DR<0.5 in 1st jet" },
    { "name":"jet2_DRbTjet",         "unit":"",  "var":"jets_drbjetFromT[csvd_jetid[1]]<0.5",  "xbin_set":[2,0,2], "exp":"DR<0.5 in 2nd jet" },
    ]
cut_ttjj = ES+" && "+ttjjVis
cut_ttbb = ES+" && "+ttbbVis
cuts ={"ttjj": cut_ttjj, "ttbb": cut_ttbb }

loc="/xrootd//store/user/youngjo/Cattools/v7-6-6v1/test_ttbar_powheg/"
######ls /xrootd//store/user/youngjo/Cattools/v7-6-6v1/test_ttbar_powheg | sed 's/cattree_/"/g' | sed 's/.root/",/g'
ls=[ "000", "001", "002", "003", "004", "006", "007", "008", "009", "010", "011", "012", "013", "014", "016", "017", "018", "019", "021", "023", "024", "025", "026", "027", "028", "032", "033", "035", "036", "038", "039", "040", "042", "043", "044", "045", "046", "047", "048", "049"  ]
#loc="/Users/youngkwonjo/Documents/CMS/Analysis/20160604_ttbb_765/hist_20160604/temp/"
#ls=["049"]
filelist=getList(loc,ls)
#filelist =[loc+"cattree_049.root"]

nom2 = "cattree/nom2"
chain = TChain(nom2)
for afile in filelist:
  f = TFile.Open(afile)
  chain.Add(afile)

tree = chain
h = []
for cut in cuts.keys():
  for i,ii in enumerate(mons):
    mon = h1_set(cut,mons[i],"")
    h1 = h1_maker(tree,mon,cuts[cut])
    h.append(copy.deepcopy(h1))
  for i,ii in enumerate(mon2ds):
    if i+1 < len(mon2ds) and len(mon2ds) > 1 :
      mon = h2_set(cut,mon2ds[i],mon2ds[i+1],"")
      h1 = h2_maker(tree,mon,cuts[cut])
      h.append(copy.deepcopy(h1))
 
makeoutput(h)

#root -l output.root
#jet1_ttjj=h1_ttjj_jet1_DRbjetFromTop_S5->Integral(1,5)/h1_ttjj_jet1_DRbjetFromTop_S5->Integral(1,51)
#jet2_ttjj=h1_ttjj_jet2_DRbjetFromTop_S5->Integral(1,5)/h1_ttjj_jet2_DRbjetFromTop_S5->Integral(1,51)
#jet1_ttbb=h1_ttbb_jet1_DRbjetFromTop_S5->Integral(1,5)/h1_ttbb_jet1_DRbjetFromTop_S5->Integral(1,51)
#jet2_ttbb=h1_ttbb_jet2_DRbjetFromTop_S5->Integral(1,5)/h1_ttbb_jet2_DRbjetFromTop_S5->Integral(1,51)


