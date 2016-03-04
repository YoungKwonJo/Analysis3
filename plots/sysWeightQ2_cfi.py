
baseWeight2 = "weight*puweight*lepweight*csvweights2[0]"
scaleweight=[
{"name":"Q2_N1",       "var": "("+baseWeight2+"*scaleWeights[1])"},
{"name":"Q2_N2",       "var": "("+baseWeight2+"*scaleWeights[2])"},
{"name":"Q2_N3",       "var": "("+baseWeight2+"*scaleWeights[3])"},
{"name":"Q2_N4",       "var": "("+baseWeight2+"*scaleWeights[4])"},
{"name":"Q2_N5",       "var": "("+baseWeight2+"*scaleWeights[5])"},
{"name":"Q2_N6",       "var": "("+baseWeight2+"*scaleWeights[6])"},
{"name":"Q2_N7",       "var": "("+baseWeight2+"*scaleWeights[7])"},
]

#pdfweight=[]
for i in range(0,212):
  pdf = {"name":"pdf_N"+str(i), "var": "("+baseWeight2+"*pdfWeights["+str(i)+"])" }
  scaleweight.append(pdf)

#219
monitors = [
  { "name":"Stat",         "unit":"Stat ",                         "var":"met",       "xbin_set":[1,0,10000]  },

  { "name":"jet3CSV",     "unit":"CSVv2 of 3rd leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[2]]",   "xbin_set":[20,0,1]     },
  { "name":"jet4CSV",     "unit":"CSVv2 of 4th leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[3]]",   "xbin_set":[20,0,1]     },
]
monitors2d = [
  { "name":"jet3CSV",     "unit":"CSV2 of 3rd leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[2]]",   "xbin_set":[20,0,1]     },
  { "name":"jet4CSV",     "unit":"CSV2 of 4th leading Jet ",     "var":"jets_bDiscriminatorCSV[csvd_jetid[3]]",   "xbin_set":[20,0,1]     },
]


