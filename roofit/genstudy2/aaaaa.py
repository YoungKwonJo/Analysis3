from bbbbb import POW,dwPOW,upPOW,AMC,MG5,POHP

def printAcc(aaa,ss):
  a=round(aaa["ttbbAcc"]     *10000.)/100.
  b=round(aaa["sysAcc_ttbb"] *10000.)/100.
  c=round(aaa["ttjjAcc"]     *10000.)/100.
  d=round(aaa["sysAcc_ttjj"] *10000.)/100.

  bbb= ss+"     & "+str(a)+"  & "+str(b)+"      & "+str(c)+" & "+str(d)+" \\\\"
  return b,d,bbb

def printEff(aaa,ss):
  a=round(aaa["ttbbEff"]     *10000.)/100.
  b=round(aaa["sysEff_ttbb"] *10000.)/100.
  c=round(aaa["ttjjEff"]     *10000.)/100.
  d=round(aaa["sysEff_ttjj"] *10000.)/100.

  bbb= ss+"     & "+str(a)+"  & "+str(b)+"      & "+str(c)+" & "+str(d)+" \\\\"
  return b,d,bbb



print "sample & $Acc._{\\ttbb}$ [\\%] & $Sys_{\\ttbb}^{Acc.}$ [\\%] &  $Acc._{\\ttjj}$ [\\%] & $Sys_{\\ttjj}^{Acc.}$ [\\%] \\\\"
print "\\hline"
bb,dd=0.,0.
for ss in ['nom','Q2_Dw3', 'Q2_Dw2', 'Q2_Dw1', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']:
  b,d,bbb=printAcc(POW[ss],ss)
  #print bbb
  print bbb.replace("_","\\_")
  if abs(b)>bb: bb=abs(b)
  if abs(d)>dd: dd=abs(d)

print "\\hline"
print "Sys        &       & "+str(bb)+"   &      & "+str(dd)+" \\\\"
print "\\hline\\hline"


b_dw,d_dw,dw_bbb=printAcc(dwPOW['nom'],'nom')
print dw_bbb

b_up,d_up,up_bbb=printAcc(upPOW['nom'],'nom')
print up_bbb

b_sys,d_sys=0.,0.
if abs(b_dw)>abs(b_up): b_sys=abs(b_dw)
if abs(b_up)>abs(b_up): b_sys=abs(b_up)

print "\\hline"
print "Sys        &       & "+str(b_sys)+"   &      & "+str(d_sys)+" \\\\"
print "\\hline\\hline"
    

print ""
print ""

print "sample & $Eff._{\\ttbb}$ [\\%] & $Sys_{\\ttbb}^{Eff.}$ [\\%] &  $Eff._{\\ttjj}$ [\\%] & $Sys_{\\ttjj}^{Eff.}$ [\\%] \\\\"
bbef,ddef=0.,0.
for ss in ['nom','Q2_Dw3', 'Q2_Dw2', 'Q2_Dw1', 'Q2_Up3', 'Q2_Up2', 'Q2_Up1']:
  b,d,bbb=printEff(POW[ss],ss)
  print bbb.replace("_","\\_")
  if abs(b)>bbef: bbef=abs(b)
  if abs(d)>ddef: ddef=abs(d)

print "\\hline"
print "Sys        &       & "+str(bbef)+"   &      & "+str(ddef)+" \\\\"
print "\\hline\\hline"

b_dwef,d_dwef,dw_bbbef=printEff(dwPOW['nom'],'nom')
print dw_bbbef

b_upef,d_upef,up_bbbef=printEff(upPOW['nom'],'nom')
print up_bbbef

bef_sys,def_sys=0.,0.
if abs(b_dwef)>abs(b_upef): bef_sys=abs(b_dwef)
if abs(b_upef)>abs(b_upef): bef_sys=abs(b_upef)


print "\\hline"
print "Sys        &       & "+str(bef_sys)+"   &      & "+str(def_sys)+" \\\\"
print "\\hline\\hline"



