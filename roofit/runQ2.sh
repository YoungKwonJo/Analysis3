#!/bin/bash

#for i in {0..24}
for i in {0..5}
do
  for j in {0..6}
  do
    nohup python genTtBbStudy.py $i $j -b >& Q2_Weights${i}_${j}.log & 
  done
done

