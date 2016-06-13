#!/bin/bash

#for i in {0..24}
for i in {0..212}
do
   echo "pdf $i "
   if [ $((${i}%10)) -eq 9 ]
   then   nohup python genTtBbStudyPDF.py $i -b >& pdfWeights$i.log 
   else   nohup python genTtBbStudyPDF.py $i -b >& pdfWeights$i.log &
   fi

done

