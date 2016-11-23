"""
This was the model used for getting the best predictions
during the contest.
Linear regression with L2 regularization, known as Lasso
Regression has been used here.
The value of the regularization parameter( alpha ) was varied
for generating the inputs.
Best score was achieved with alpha = 0.1
"""

import pandas as pd
import numpy as np

trd = pd.read_csv('trainingdata.csv', index_col = 0)
td = pd.read_csv('testinput.csv', index_col = 0)

x1 = pd.read_csv('buyvtrain.csv', index_col = 0)
x2 = pd.read_csv('sellvtrain.csv', index_col = 0)
x1 = x1.ix[:, 1:].as_matrix()
x2 = x2.ix[:, 1:].as_matrix()

y1 = trd.ix[:, -2].as_matrix()
y2 = trd.ix[:, -1].as_matrix()

X1 = pd.read_csv('buyvtestinput.csv', index_col = 0)
X2 = pd.read_csv('sellvtestinput.csv', index_col = 0)
X1 = X1.ix[:, 1:].as_matrix()
X2 = X2.ix[:, 1:].as_matrix()

from sklearn import linear_model

regBuy = linear_model.Ridge(alpha = 0.1)
regBuy.fit(x1,y1)
regSell =  linear_model.Ridge(alpha = 0.1)
regSell.fit(x2,y2)

buyPredictions = regBuy.predict(X1)
sellPredictions = regSell.predict(X2)

# rouding off predicted transactions

buyPredictions[buyPredictions<5000] = 0
sellPredictions[sellPredictions<5000] = 0

buyPredictions[(buyPredictions>=5000) & (sellPredictions<=7500)] = 5000
sellPredictions[(sellPredictions>=5000) & (sellPredictions<=7500)] = 5000

# will try this after testing the model learnt through k best features
buyPredictions[(buyPredictions>7500) & (sellPredictions<10000)] = 10000
sellPredictions[(sellPredictions>7500) & (sellPredictions<10000)] = 10000

for i in range(len(buyPredictions)):
	if buyPredictions[i]%10000 > 5000:
		buyPredictions[i] = (int(buyPredictions[i])/10000)*10000 + 10000
	else:
		buyPredictions[i] = (int(buyPredictions[i])/10000)*10000

for i in range(len(sellPredictions)):
	if sellPredictions[i]%10000 > 5000:
		sellPredictions[i] = (int(sellPredictions[i])/10000)*10000 + 10000
	else:
		sellPredictions[i] = (int(sellPredictions[i])/10000)*10000

output = pd.DataFrame()
output['isin'] = pd.Series(td['isin'].values)
output['buyvolume'] = pd.Series(buyPredictions)
output['sellvolume'] = pd.Series(sellPredictions)

output.to_csv('output.csv', index = False)