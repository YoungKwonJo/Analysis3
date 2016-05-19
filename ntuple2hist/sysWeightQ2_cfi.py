
baseWeight2 = "puweight*mueffweight*eleffweight*tri*csvweights[0]"
#baseWeight2 = "weight*puweight*lepweight*csvweights[0]"
#scaleweight = []
aaaaaaaa="""
  ,"Q2_Up1":"scaleWeightsUp[0]"
  ,"Q2_Up2":"scaleWeightsUp[1]"
  ,"Q2_Up3":"scaleWeightsUp[2]"
  ,"Q2_Dw1":"scaleWeightsDown[0]"
  ,"Q2_Dw2":"scaleWeightsDown[1]"
  ,"Q2_Dw3":"scaleWeightsDown[2]"
"""
scaleweight=[
{"name":"Q2_Up1",       "var": "("+baseWeight2+"*scaleWeightsUp[0])"},
{"name":"Q2_Up2",       "var": "("+baseWeight2+"*scaleWeightsUp[1])"},
{"name":"Q2_Up3",       "var": "("+baseWeight2+"*scaleWeightsUp[2])"},
{"name":"Q2_Dw1",       "var": "("+baseWeight2+"*scaleWeightsDown[0])"},
{"name":"Q2_Dw2",       "var": "("+baseWeight2+"*scaleWeightsDown[1])"},
{"name":"Q2_Dw3",       "var": "("+baseWeight2+"*scaleWeightsDown[2])"}
]

#pdfweight=[]
for i in range(0,212):
  pdf = {"name":"pdf_N"+str(i), "var": "("+baseWeight2+"*pdfWeights["+str(i)+"])" }
  scaleweight.append(pdf)

#219
monitors = [
  { "name":"Stat",         "unit":"Stat ",                         "var":"met",       "xbin_set":[1,0,10000]  },

  { "name":"jet3CSV",     "unit":"CSVv2 of 3rd leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[2]]",   "xbin_set":[10,0,1]     },
  { "name":"jet4CSV",     "unit":"CSVv2 of 4th leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[3]]",   "xbin_set":[10,0,1]     },
]
monitors2d = [
  { "name":"jet3CSV",     "unit":"CSV2 of 3rd leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[2]]",   "xbin_set":[10,0,1]     },
  { "name":"jet4CSV",     "unit":"CSV2 of 4th leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[3]]",   "xbin_set":[10,0,1]     },
]


