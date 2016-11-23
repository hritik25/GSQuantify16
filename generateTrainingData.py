# this file will generate the training data from one month
# history data combined with static data for 8 one month training 
# windows

import pandas as pd
import numpy as np
from datetime import datetime

dfHistory = pd.read_csv('dataset.csv')
dfStatic = pd.read_csv('staticdata.csv')

# the cleaning and segregation required irrespective of time frames
dfHistory['date'] = pd.to_datetime(dfHistory['date'], format = '%d%b%Y')
dfHistory.drop(['time', 'timeofday'], inplace = True, axis = 1)

# A dictionary to hold the 4 dataframes which will be created
# by shifting training time slots over the period of 3 months
# These will later be combined into one 
dfTotalTrd = pd.DataFrame()

startDate = dfHistory['date'].min()
startTrialDate = datetime(2016, 04, 15)
gap = pd.Timedelta('7 days')

for i in range(8):
	# dataframe to generate training input
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


	# dataframe to generate training output
	dfo = dfHistory[(dfHistory['date'] >= startTrialDate) & (dfHistory['date'] <= startTrialDate + pd.Timedelta('4 days'))]

	dfob = pd.DataFrame(dfo[dfo['side'] == 'B'])
	dfob = dfob.drop(['price', 'date'], axis = 1)

	dfos = pd.DataFrame(dfo[dfo['side'] == 'S'])
	dfos = dfos.drop(['price', 'date'], axis = 1)

	dfobg = dfob.groupby(['isin'], as_index = False).sum()
	dfobg=dfobg.rename(columns = {'volume':'buyVolumeO'})

	dfosg = dfos.groupby(['isin'], as_index = False).sum()
	dfosg=dfosg.rename(columns = {'volume':'sellVolumeO'})

	dfo.drop(['side', 'volume'], inplace = True, axis = 1)
	dfog = dfo.groupby(['isin'], as_index= False).count()
	dfog = pd.DataFrame(dfog['isin'])

	dfog = pd.merge(dfog, dfobg, how='left', on='isin')	
	dfog = pd.merge(dfog, dfosg, how='left', on='isin')

	dfog.fillna(0, inplace = True)

	# colplete input + output history dataframe 
	dfh = pd.merge(df, dfog, how = 'left', on = 'isin')
	dfh.fillna(0, inplace = True)

	# complete input with all varibles
	dfCompleteInput = pd.merge(dfh, dfStatic, how = 'left', on = 'isin')
	dfTotalTrd = dfTotalTrd.append(dfCompleteInput)

	# shift the window by 7
	startDate = startDate + gap
	startTrialDate = startTrialDate + gap

buyVolumeO = dfTotalTrd['buyVolumeO']
sellVolumeO = dfTotalTrd['sellVolumeO']
dfTotalTrd.drop(['buyVolumeO', 'sellVolumeO'], axis = 1, inplace = True)
dfTotalTrd['buyVolumeO'] = buyVolumeO
dfTotalTrd['sellVolumeO'] = sellVolumeO 

# write all this training data to a csv
dfTotalTrd.to_csv('trainingdata.csv')
