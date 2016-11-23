# this file will generate the test input for predicting
# the buy and sell volumes for immediate next 3 business
# days ( 10th June, 13th June and 14th June )from the 3 months
# of recorded history

import pandas as pd
import numpy as np
from datetime import datetime
import csv

dfHistory = pd.read_csv('dataset.csv')
dfStatic = pd.read_csv('staticdata.csv')
allBonds = list(dfStatic['isin'].values)

# the cleaning and segregation required irrespective of time frames
dfHistory['date'] = pd.to_datetime(dfHistory['date'], format = '%d%b%Y')
dfHistory.drop(['time', 'timeofday'], inplace = True, axis = 1)

# A dictionary to hold the 4 dataframes which will be created
# by shifting training time slots over the period of 3 months
# These will later be combined into one 

startDate = dfHistory['date'].min()
startTrialDate = datetime(2016, 04, 15)
gap = pd.Timedelta('7 days')

for i in range(8):
	startDate = startDate + gap
	startTrialDate = startTrialDate + gap


# for creating the test data
df = dfHistory[(dfHistory['date'] < startTrialDate) & (dfHistory['date'] >= startDate)]

dfBuy = df[df['side'] == 'B']
dfBuy = dfBuy.drop(['price', 'date'], axis = 1)
dfBuyGrouped = dfBuy.groupby(['isin'], as_index = False).sum()
dfBuyGrouped=dfBuyGrouped.rename(columns = {'volume':'buyVolume'})

dfSell = df[df['side'] == 'S']
dfSell = dfSell.drop(['price', 'date'], axis = 1)
dfSellGrouped = dfSell.groupby(['isin'], as_index = False).sum()
dfSellGrouped=dfSellGrouped.rename(columns = {'volume':'sellVolume'})

df.drop(['side', 'volume'], inplace = True, axis = 1)
# adding new column to get mean price of each bond after grouping
df['meanPrice'] = pd.Series(df['price'])
# grouping to get one row for each bond and respective mean price and std. dev. in price
df = df.groupby(['isin'], as_index= False).aggregate({'price':'std', 'meanPrice' : 'mean'})
df.fillna(0.0, inplace = True)
df = pd.merge(df, dfBuyGrouped, how='left', on='isin')
df = pd.merge(df, dfSellGrouped, how='left', on='isin')
df.fillna(0, inplace = True)

# write to csv
# df.to_csv('testinputtmp.csv', index = False)
# ^first append with missing bonds then write to csv 

missingBonds = [ bond for bond in allBonds if bond not in list(df['isin'].values)]
missingIsins = pd.DataFrame()

# stdevMean = df['price'].mean()
# avgMean = df['meanPrice'].mean()
# bvMedian = int(df['buyVolume'].median())
# svMedian = int(df['sellVolume'].median())
# row = [ stdevMean, avgMean, bvMedian, svMedian ]

# ^ this was a pretty naive assumption
# most probably, these missin isins have appeared a lot less 
# so taking a mean from their history would be sufficient
dfMissing = dfHistory.loc[dfHistory['isin'].isin(missingBonds)]

dfBuyM = dfMissing[dfMissing['side'] == 'B']
dfBuyM = dfBuyM.drop(['price', 'date'], axis = 1)
dfBuyMGrouped = dfBuyM.groupby(['isin'], as_index = False).sum()
dfBuyMGrouped=dfBuyMGrouped.rename(columns = {'volume':'buyVolume'})

dfSellM = dfMissing[dfMissing['side'] == 'S']
dfSellM = dfSellM.drop(['price', 'date'], axis = 1)
dfSellMGrouped = dfSellM.groupby(['isin'], as_index = False).sum()
dfSellMGrouped=dfSellMGrouped.rename(columns = {'volume':'sellVolume'})

dfMissing.drop(['side', 'volume'], inplace = True, axis = 1)
# adding new column to get mean price of each bond after grouping
dfMissing['meanPrice'] = pd.Series(dfMissing['price'])
# grouping to get one row for each bond and respective mean price and std. dev. in price
dfMissing = dfMissing.groupby(['isin'], as_index= False).aggregate({'price':'std', 'meanPrice' : 'mean'})
dfMissing.fillna(0.0, inplace = True)
dfMissing = pd.merge(dfMissing, dfBuyMGrouped, how='left', on='isin')
dfMissing = pd.merge(dfMissing, dfSellMGrouped, how='left', on='isin')
dfMissing.fillna(0, inplace = True)

df = df.append(dfMissing)
df.to_csv('testinputtmp.csv', index=False)

histTest = pd.read_csv('testinputtmp.csv')
completeInput = pd.merge(histTest, dfStatic, how= 'left', on= 'isin')

# write complete test input to file
completeInput.to_csv('testinput.csv')