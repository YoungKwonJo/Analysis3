  #['Stat', 'nGoodPV', 'MET', 'ZMass',            # 0-3
  # 'nBJet30L', 'nBJet30M', 'NJet30', 'nBJet30T', # 4-7
  # 'lep1Pt', 'lep2Pt', 'lep1Eta', 'lep2Eta',     # 8-11
  # 'lep1Phi', 'lep2Phi', 'lep1Iso', 'lep2Iso'    #12-15
  # 'jet1Pt', 'jet2Pt', 'jet3Pt', 'jet4Pt',       #16-19
  # 'jet1Eta', 'jet2Eta', 'jet3Eta', 'jet4Eta',   #20-23
  # 'jet1Phi', 'jet2Phi', 'jet3Phi', 'jet4Phi',   #24-27
  # 'jet1CSV', 'jet2CSV', 'jet3CSV', 'jet4CSV']   #28-31

for i in {1..7}
do
    python makeCanvasAN.py S2 $i -b
    python makeCanvasAN.py S3 $i -b
    python makeCanvasAN.py S4 $i -b
    python makeCanvasAN.py S5 $i -b
    python makeCanvasAN.py S6 $i -b
done 

for i in {8..15}
do
    python makeCanvasAN.py S2 $i -b
    python makeCanvasAN.py S3 $i -b
done 

for i in {16..31}
do
    python makeCanvasAN.py S4 $i -b
    python makeCanvasAN.py S5 $i -b
    python makeCanvasAN.py S6 $i -b
done 

