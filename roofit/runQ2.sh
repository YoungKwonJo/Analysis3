#!/bin/bash

#for i in {0..24}
for i in {0..2}
do
   nohup python genTtBbStudy.py $i -b >& Q2_Weights$i.log & 
done

