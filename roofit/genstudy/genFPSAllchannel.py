AMC={'nom': {'AMC': {'hadroic': 17120975.0, 'S0': {'ttbbF': 305973.0, 'ttbb': 4990.0, 'ttbF': 739170.0, 'ttlfF': 17442407.0, 'ttotF': 19154086.0, 'ttccF': 664012.0, 'ttcc': 9459.0, 'tt2bF': 188888.0, 'tt2b': 3389.0, 'ttb': 15535.0, 'ttlf': 331797.0, 'ttot': 38110606.0}, 'semileptonic': 17088723.0, 'dileptonic': 4266078.0, 'etc': 0.0}}, 'weight': {'AMC': {'hadroic': 5683353.0, 'S0': {'ttbbF': 71857.0, 'ttbb': 1154.0, 'ttbF': 168966.0, 'ttlfF': 4554827.0, 'ttotF': 7777702.0, 'ttccF': 159378.0, 'ttcc': 2157.0, 'tt2bF': 44514.0, 'tt2b': 735.0, 'ttb': 3331.0, 'ttlf': 81261.0, 'ttot': 12682774.0}, 'semileptonic': 5670255.0, 'dileptonic': 1417804.0, 'etc': 0.0}}}
MG5={'nom': {'MG5': {'hadroic': 4542315.0, 'S0': {'ttbbF': 56158.0, 'ttbb': 947.0, 'ttbF': 134621.0, 'ttlfF': 3438782.0, 'ttotF': 6425897.0, 'ttccF': 122769.0, 'ttcc': 1881.0, 'tt2bF': 41247.0, 'tt2b': 787.0, 'ttb': 2969.0, 'ttlf': 66280.0, 'ttot': 10142267.0}, 'semileptonic': 4538129.0, 'dileptonic': 1134687.0, 'etc': 0.0}}, 'weight': {'MG5': {'hadroic': 4542315.0, 'S0': {'ttbbF': 56158.0, 'ttbb': 947.0, 'ttbF': 134621.0, 'ttlfF': 3438782.0, 'ttotF': 6425897.0, 'ttccF': 122769.0, 'ttcc': 1881.0, 'tt2bF': 41247.0, 'tt2b': 787.0, 'ttb': 2969.0, 'ttlf': 66280.0, 'ttot': 10142267.0}, 'semileptonic': 4538129.0, 'dileptonic': 1134687.0, 'etc': 0.0}}}
POW={'nom': {'POW': {'hadroic': 44779958.0, 'S0': {'ttbbF': 510842.0, 'ttbb': 8194.0, 'ttbF': 1203720.0, 'ttlfF': 30803478.0, 'ttotF': 64061622.0, 'ttccF': 1090577.0, 'ttcc': 15362.0, 'tt2bF': 364732.0, 'tt2b': 6393.0, 'ttb': 24712.0, 'ttlf': 546363.0, 'ttot': 97393418.0}, 'semileptonic': 42929174.0, 'dileptonic': 10285310.0, 'etc': 0.0}}, 'weight': {'POW': {'hadroic': 44779958.0, 'S0': {'ttbbF': 510842.0, 'ttbb': 8194.0, 'ttbF': 1203720.0, 'ttlfF': 30803478.0, 'ttotF': 64061622.0, 'ttccF': 1090577.0, 'ttcc': 15362.0, 'tt2bF': 364732.0, 'tt2b': 6393.0, 'ttb': 24712.0, 'ttlf': 546363.0, 'ttot': 97393418.0}, 'semileptonic': 42929174.0, 'dileptonic': 10285310.0, 'etc': 0.0}}}

POW2= POW["weight"]["POW"]["S0"]
AMC2= AMC["weight"]["AMC"]["S0"]
MG52= MG5["nom"]["MG5"]["S0"]

def addttjj(Sample):
  ttjjF=Sample["ttbbF"]+Sample["ttbF"]+ Sample["tt2bF"]+Sample["ttccF"]+Sample["ttlfF"]
  ttjj=Sample["ttbb"]+Sample["ttb"]+ Sample["tt2b"]+Sample["ttcc"]+Sample["ttlf"]
  Sample["ttjjF"]=ttjjF
  Sample["ttjj"]=ttjj

addttjj(POW2)
addttjj(MG52)
addttjj(AMC2)

###########
POW_ttbbAcc = POW2["ttbb"]/POW2["ttbbF"]
POW_ttjjAcc = POW2["ttjj"]/POW2["ttjjF"]

print "POW & "+str(POW_ttbbAcc)+" & "+str(POW_ttjjAcc)
MG5_ttbbAcc = MG52["ttbb"]/MG52["ttbbF"]
MG5_ttjjAcc = MG52["ttjj"]/MG52["ttjjF"]
print "MG5 & "+str(MG5_ttbbAcc)+" & "+str(MG5_ttjjAcc)

AMC_ttbbAcc = AMC2["ttbb"]/AMC2["ttbbF"]
AMC_ttjjAcc = AMC2["ttjj"]/AMC2["ttjjF"]
print "AMC & "+str(AMC_ttbbAcc)+" & "+str(AMC_ttjjAcc)

POWAcc={"ttbb":POW_ttbbAcc,"ttjj":POW_ttjjAcc,"data":POW2 }
AMCAcc={"ttbb":AMC_ttbbAcc,"ttjj":AMC_ttjjAcc,"data":AMC2 }
MG5Acc={"ttbb":MG5_ttbbAcc,"ttjj":MG5_ttjjAcc,"data":MG52 }



