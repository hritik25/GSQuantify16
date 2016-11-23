from sklearn.feature_selection import f_regression	
import pandas as pd
import numpy as np

trd = pd.read_csv('trainingdata.csv', index_col = 0)

x = trd.ix[:, 1:-2].as_matrix()
y1 = trd.ix[:, -2].as_matrix()
y2 = trd.ix[:, -1].as_matrix()

fvaluesBuy, pvaluesBuy = f_regression(x,y1)
fvaluesSell, pvaluesSell = f_regression(x,y2)

# selecting best p-value features
a = np.where(pvaluesBuy<=0.001)
# converting to a list format
a = list(a[0])

b = np.where(pvaluesSell<=0.001)
b = list(b[0])

dfTrainBuy = trd.iloc[:, a]
dfTrainSell = trd.iloc[:, b]

dfTrainBuy.to_csv('buyvtrain.csv')
dfTrainSell.to_csv('sellvtrain.csv')
# ^files generated already

td = pd.read_csv('testinput.csv', index_col = 0)

dfTestBuy = td.iloc[:, a]
dfTestSell = td.iloc[:, b]

dfTestBuy.to_csv('buyvtestinput.csv')
dfTestSell.to_csv('sellvtestinput.csv')

