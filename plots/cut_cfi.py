

mm= "(channel==3)" 
ee= "(channel==2)"
em= "(channel==1)"

preselection = "(filtered==1)" 
#trigger   = "((tri==1)*(filtered==1))"
trigger   = "((tri==1)*(filtered==1))"

cut = [ "(step1==1)", "(step2==1)",  "(step3==1)", "(step4==1)","(step5==1)","(step6==1)" ]
mm_cuts ={
"channel": "mm",
"cut": [
   "(1)",
#   preselection,
   "("+mm+"&&"+trigger+")",
   "("+cut[0]+"&&"+mm+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
ee_cuts = {
"channel": "ee",
"cut": [
   "(1)",
#   preselection,
   "("+ee+"&&"+trigger+")",
   "("+cut[0]+"&&"+ee+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}
em_cuts = {
"channel": "em",
"cut":[
   "(1)", 
#   preselection,
   "("+em+"&&"+trigger+")",
   "("+cut[0]+"&&"+em+")", cut[1], cut[2], cut[3], cut[4], cut[5]
]
}

##########
import copy

mm_cutsQCD = copy.deepcopy(mm_cuts)
ee_cutsQCD = copy.deepcopy(ee_cuts)
em_cutsQCD = copy.deepcopy(em_cuts)

def cut_maker(cuts_,ii):
  cuts  = {}
  for i,cut in enumerate(cuts_["cut"]):
    if i==0 :
      cuts["S%d"%i]=cut
    else:
      cuts["S%d"%i]= cuts["S%d"%(i-1)] + " * " + cut

  cuts2  = {}
  cuts2["S%d"%ii] = cuts["S%d"%ii]
  #cutsN = {"channel":cuts_["channel"],"cut":cuts2}
  cutsN = {"channel":cuts_["channel"],"cut":cuts2}
  #print cutsN
  return cutsN


