# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 17:53:35 2021

@author: leoml
"""

import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())

home_dir = os.getenv("HOME_DIR")

log_files = [
    'log_holts_hill_climb_1m',
    'log_holts_hill_climb_6m',
    'log_holts_hill_climb_12m',
    'log_holts_simulated_annealing_1m',
    'log_holts_simulated_annealing_6m',
    'log_holts_simulated_annealing_12m',
    'log_sarimax_hill_climb_1m',
    'log_sarimax_hill_climb_6m',
    'log_sarimax_hill_climb_12m',
    'log_sarimax_simulated_annealing_1m',
    'log_sarimax_simulated_annealing_6m',
    'log_sarimax_simulated_annealing_12m'
    ]

cvt = {
       '12m': 12,
       '_6m': 6,
       '_1m': 1
   }

log = pd.read_csv(home_dir + '\\data\\logs\\' + log_files[0] + '.csv', sep=';')
log['modelo'] = log_files[0]
log['periodo'] = cvt[log_files[0][-3:]]

for i in range(1,len(log_files)):
    temp = pd.read_csv(home_dir + '\\data\\logs\\' + log_files[i] + '.csv', sep=';')
    temp['modelo'] = log_files[i]
    temp['periodo'] = cvt[log_files[i][-3:]]
    
    log = pd.concat([log, temp])

groupby = log.groupby(['modelo', 'periodo'])['MPA_MELHOR'].min()

right = log.drop(['ID', 'periodo', 'ITERACAO', 'PARAM_MELHOR', 'MPA_MELHOR', 'Unnamed: 0'], axis=1)
right = right.drop_duplicates()

groupby = pd.DataFrame(groupby).reset_index()
groupby = groupby.rename({'MPA_MELHOR': 'MPA_ATUAL'}, axis=1)

groupby = groupby.set_index(['modelo', 'MPA_ATUAL'])
right = right.set_index(['modelo', 'MPA_ATUAL'])

groupby = groupby.join(right,on=['modelo', 'MPA_ATUAL'])
params = groupby.reset_index().groupby(['modelo', 'periodo']).first()

params.to_csv(home_dir + '\\analysis\\best_parameters.csv', index=True, sep=';')

