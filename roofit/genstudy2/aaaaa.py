from bbbbb import POW,dwPOW,upPOW,AMC,MG5,POHP

def printAcc(aaa):
  a=round(aaa["ttbbAcc"]     *10000.)/100.
  b=round(aaa["sysAcc_ttbb"] *10000.)/100.
  c=round(aaa["ttjjAcc"]     *10000.)/100.
  d=round(aaa["sysAcc_ttjj"] *10000.)/100.

  bbb= ss+"     & "+str(a)+"  & "+str(b)+"      & "+str(c)+" & "+str(d)+" \\\\"
  return b,d,bbb

def printEff(aaa):
  a=round(aaa["ttbbEff"]     *10000.)/100.
  b=round(aaa["sysEff_ttbb"] *10000.)/100.
  c=round(aaa["ttjjEff"]     *10000.)/100.
  d=round(aaa["sysEff_ttjj"] *10000.)/100.

  bbb= ss+"     & "+str(a)+"  & "+str(b)+"      & "+str(c)+" & "+str(d)+" \\\\"
  return b,d,bbb



print "sample & Acc._{\\ttbb} [\\%] & Sys_{\\ttbb}^{Acc.} [\\%] &  Acc._{\\ttjj} [\\%] & Sys_{\\ttjj}^{Acc.} [\\%] \\\\"
bb,dd=0.,0.
for ss in ['Q2_Dw3', 'nom', 'Q2_Dw1', 'Q2_Dw2', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']:
  b,d,bbb=printAcc(POW[ss])
  print bbb
  if abs(b)>bb: bb=abs(b)
  if abs(d)>dd: dd=abs(d)


print bb
print dd

b_dw,d_dw,dw_bbb=printAcc(dwPOW['nom'])
print dw_bbb

b_up,d_up,up_bbb=printAcc(upPOW['nom'])
print up_bbb

print ""
print ""

print "sample & Eff._{\\ttbb} [\\%] & Sys_{\\ttbb}^{Eff.} [\\%] &  Eff._{\\ttjj} [\\%] & Sys_{\\ttjj}^{Eff.} [\\%] \\\\"
bbef,ddef=0.,0.
for ss in ['Q2_Dw3', 'nom', 'Q2_Dw1', 'Q2_Dw2', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']:
  b,d,bbb=printEff(POW[ss])
  print bbb
  if abs(b)>bbef: bbef=abs(b)
  if abs(d)>ddef: ddef=abs(d)


print bbef
print ddef

b_dwef,d_dwef,dw_bbbef=printEff(dwPOW['nom'])
print dw_bbbef

b_upef,d_upef,up_bbbef=printEff(upPOW['nom'])
print up_bbbef



