"""
will generate a csv or a dataframe with the static bond data in
the proper format to be fed into the sklearn models.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# read the Static bond data into a dataframe
dfStatic = pd.read_csv('ML_Bond_metadata.csv')

# will not be using the features 'issuer' and 'issue date'
dfStatic = dfStatic.drop(['issuer', 'issue date'], axis = 1)

# 'Market', 'paymentRank', 'ratingAgency1Rating' and 'ratingAgency2Rating' 
# indicate a linear order of importance, so we convert them to integer values
def categoryToNumeric(x):
	return int(filter(str.isdigit, x))

rankedFeatures = ['Market', 'paymentRank', 'ratingAgency1Rating', 'ratingAgency2Rating']
for feature in rankedFeatures:
	dfStatic[feature+'Num'] = dfStatic[feature].apply(categoryToNumeric)
dfStatic.drop(rankedFeatures, inplace = True, axis = 1)


# get all date type features in python datetime data type
def dateProper(x):
	if type(x) == float and  np.isnan(x):
		pass
	else:
		if '-' in x:
			thisDate = datetime.strptime(x , "%d-%b-%y")
			return int((thisDate-datetime(2016, 6, 9)).days)/30
		else:
			thisDate = datetime.strptime(x , "%d%b%Y")
			return int((thisDate-datetime(2016, 6, 9)).days)/30

dateFeatures = ['maturity', 'ratingAgency1EffectiveDate', 'ratingAgency2EffectiveDate']

for feature in dateFeatures:
	dfStatic[feature+'Proper'] = dfStatic[feature].apply(dateProper)
	dfStatic[feature+'Proper'].fillna(int(dfStatic[feature+'Proper'].mean()), inplace = True)
dfStatic.drop(dateFeatures, inplace = True, axis = 1)

# filling in missing values in 'couponFrequency' with mode
mode = float(dfStatic['couponFrequency'].mode())
dfStatic['couponFrequency'] = dfStatic['couponFrequency'].fillna(mode)

# convert categorical variables to dummy variables
categorical = [ 'collateralType', 'couponType', 
		'industryGroup', 'industrySector', 'industrySubgroup',
		'maturityType', 'securityType', '144aFlag',
       'ratingAgency1Watch', 'ratingAgency2Watch' ]

dfStaticEncoded = pd.get_dummies(dfStatic, columns = categorical)

# generate a CSV from this dataframe
dfStaticEncoded.to_csv('staticdata.csv')
