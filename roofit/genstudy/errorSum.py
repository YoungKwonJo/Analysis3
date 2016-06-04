
def quardsum(aaa):
  from math import sqrt
  bbb=0.0
  for i in aaa:
    bbb+= i*i
  return sqrt(bbb)

Rsys= [ 0.40 , 2.58 , 18.64, 14.31, 9.74 , 0.41 , 1.55 , 9.95 , 0.20 , 0.08, 1.3 ]
ttjjsys=[0.07 ,7.37 ,4.65 ,1.31 ,9.83 ,0.01 ,3.5 ,0.02 ,1.97 ,1.61, 1.3, 2.7 ]
ttbbsys=[0.40,7.81,19.21,14.37,13.84,0.41,3.83,9.95,1.98,1.61, 2.7 ]

#Rsys= [0.37 , 2.52 , 18.8 , 14.5 , 9.76 , 3.21 , 1.58 , 10.06 , 0.10 , 8.81, 1.3]
#ttjjsys=[0.09 , 7.4  , 4.65 , 1.32 , 9.83 , 0.01 , 3.55  , 0.02 , 1.98 , 3.57 , 2.7] 
#ttbbsys=[0.38 , 7.81 , 19.36 , 14.56 , 13.85 , 3.21 , 3.87 , 10.06 , 1.98 , 9.51 , 2.7]
#ttjjsys=[0.09 , 7.4  , 4.65 , 1.32 , 9.83 , 0.01 , 3.55  , 0.02 , 1.98 ,1.3 , 2.7] 
#ttbbsys=[0.38 , 7.81 , 19.36 , 14.56 , 13.85 , 3.21 , 3.87 , 10.06 , 1.98 , 2.7]

RsysVS= [ 3.02 ,9.83  , 0.90 ]
ttjjsysVS=[ 6.20 , 9.91 , 1.41 ]
ttbbsysVS= [ 9.40 , 12.84 , 1.91]

RsysFS= [ 2.66 , 1.71 ,11.51 ]
ttjjsysFS= [  10.52 , 4.34 , 10.56  ]
ttbbsysFS= [ 13.45 , 5.72 , 13.26 ]

"""
Rsys= [0.37 , 2.52 , 18.8 , 14.5 , 9.76 , 3.21 , 4.64 , 10.06 , 0.10 , 8.81]
ttjjsys=[0.09 , 7.4  , 4.65 , 1.32 , 9.83 , 0.01 , 7.2  , 0.02 , 1.98 , 3.57 , 2.7]
ttbbsys=[0.38 , 7.81 , 19.36 , 14.56 , 13.85 , 3.21 , 8.57 , 10.06 , 1.98 , 9.51 , 2.7]

RsysVS= [ 3.02 ,9.83 ,1.90 , 0.90 ]
ttjjsysVS=[ 6.20 , 9.91 , 18.72 , 1.41 ]
ttbbsysVS= [ 9.40 , 12.84 , 16.46 , 1.91]

RsysFS= [ 2.66 , 1.71 ,11.51 ,1.65]
ttjjsysFS= [  10.52 , 4.34 , 10.56 , 51.44 ]
ttbbsysFS= [ 13.45 , 5.72 , 13.26 , 53.93]
"""

R = quardsum(Rsys) 
ttjj = quardsum(ttjjsys) 
ttbb = quardsum(ttbbsys) 

Rvs = quardsum(RsysVS) 
ttjjvs = quardsum(ttjjsysVS) 
ttbbvs = quardsum(ttbbsysVS) 

Rfs = quardsum(RsysFS) 
ttjjfs = quardsum(ttjjsysFS) 
ttbbfs = quardsum(ttbbsysFS) 

print "R:"+str(R)+", ttjj:"+str(ttjj)+", ttbb:"+str(ttbb)
print "Rvs:"+str(Rvs)+", ttjj:"+str(ttjjvs)+", ttbb:"+str(ttbbvs)
print "Rfs:"+str(Rfs)+", ttjj:"+str(ttjjfs)+", ttbb:"+str(ttbbfs)

RvsTot = quardsum([R,Rvs])
ttjjvsTot = quardsum([ttjj,ttjjvs])
ttbbvsTot = quardsum([ttbb,ttbbvs])

RfsTot = quardsum([R,Rfs])
ttjjfsTot = quardsum([ttjj,ttjjfs])
ttbbfsTot = quardsum([ttbb,ttbbfs])

print "RvsTot:"+str(RvsTot)+", ttjj:"+str(ttjjvsTot)+", ttbb:"+str(ttbbvsTot)
print "RfsTot:"+str(RfsTot)+", ttjj:"+str(ttjjfsTot)+", ttbb:"+str(ttbbfsTot)




