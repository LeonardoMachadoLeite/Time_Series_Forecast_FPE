# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:55:17 2021

@author: leoml
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

oil = pd.read_csv('Cushing_OK_WTI_Spot_Price_FOB.csv')
oil.info()

oil['Data'] = pd.to_datetime(oil['Month'], infer_datetime_format=True)

scaler = MinMaxScaler()
oil['Oil_Price'] = scaler.fit_transform(oil['Oil_Price'].to_numpy().reshape(-1,1))
oil = oil.drop(columns='Month')

oil = oil.set_index('Data')
oil = oil.resample('M').first()

oil_1m = oil.loc[(oil.index < '2/1/2019') & (oil.index > '12/31/1996')]
oil_6m = oil.loc[(oil.index < '7/1/2019') & (oil.index > '12/31/1996')]
oil_12m = oil.loc[(oil.index < '1/1/2020') & (oil.index > '12/31/1996')]

oil_1m.to_csv('crude_oil_prices_preprocessed_1m.csv')
oil_6m.to_csv('crude_oil_prices_preprocessed_6m.csv')
oil_12m.to_csv('crude_oil_prices_preprocessed_12m.csv')

brl = pd.read_csv('USD_BRL Historical Data.csv')

brl['Data'] = pd.date_range(start='1/1/1997', periods=brl.shape[0], freq='M')

scaler = MinMaxScaler()
brl['Price'] = scaler.fit_transform(brl['Price'].to_numpy().reshape(-1,1))
brl = brl.drop(columns=['Date', 'Open', 'High', 'Low', 'Change %'])


brl = brl.set_index('Data')

brl_1m = brl.loc[(brl.index < '2/1/2019') & (brl.index > '12/31/1996')]
brl_6m = brl.loc[(brl.index < '7/1/2019') & (brl.index > '12/31/1996')]
brl_12m = brl.loc[(brl.index < '1/1/2020') & (brl.index > '12/31/1996')]

brl_1m.to_csv('usd_brl_exchange_rate_preprocessed_1m.csv')
brl_6m.to_csv('usd_brl_exchange_rate_preprocessed_6m.csv')
brl_12m.to_csv('usd_brl_exchange_rate_preprocessed_12m.csv')
