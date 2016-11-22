-----------------------------------------
List of files and their responsibilities:
-----------------------------------------

generateStaticCsv.py		
_______________________
Will produce a csv file staticdata.csv using the static bond characteristics data in the given ML_Bond_metadata.csv file. This will be further used to generate training data for the model.

generateTrainingData.py
_______________________
Will produce a csv file trainingdata.csv using staticdata.csv and the bond liquidity history data in the given dataset.csv file. This will be passed to the feature selection algorithm.

generatetest.py				
_______________________
Will produce a csv file testinput.csv ( and a file testinputtmp.csv, to be ignored) using staticdata.csv and dataset.csv which will be passed to the feature selection algorithm.

selectbest.py				
_______________________
Will use training data in the file trainingdata.csv to generate reduced training data after applying a feature selection algorithm and the training data will be written in buyvtrain.csv & sellvtrain.csv. Will use test input data in the file testinput.csv to generate test input with selected features and this will be written to the files buyvtestinput.csv and sellvtestinput.csv.

modelridgea01moredata.py
_______________________
Will apply the regression model to training input files buyvtrain.csv and sellvtrain.csv and then predict the output on buvtestinput.csv and sellvtestinput.csv.
The output will be written to the file output.csv.



-----------
How to run?
-----------
1. Change directory to current.
2. run python generateStaticData.py
3. run python generateTrainingData.py
4. run python generateTest.py
5. run python selectbest.py
6. run modelridgea01moredata.py
