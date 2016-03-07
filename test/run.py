import os
from monitors_cfi import *

for i in range(0,len(monitors)+1): 
#for i in range(0,1): 
  ddd = "nohup python ntuple2hist.py " + ("%d"%i) + " >& log/log" + ("%d"%i) + ".txt  & "
  os.system(ddd)


