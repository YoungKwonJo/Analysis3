#!/bin/bash

#for i in {0..24}
for i in {0..2}
do
  for j in {0..6}
  do
    nohup python genTtBbStudy.py $i $j -b >& Q2_Weights$i_$j.log & 
  done
done

