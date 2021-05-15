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


log = pd.read_csv(home_dir + '\\data\\logs\\' + log_files[0] + '.csv', sep=';')
log['modelo'] = log_files[0]

for i in range(1,len(log_files)):
    temp = pd.read_csv(home_dir + '\\data\\logs\\' + log_files[i] + '.csv', sep=';')
    temp['modelo'] = log_files[i]
    
    log = pd.concat([log, temp])

groupby = log.groupby(['modelo', 'ID'])['MPA_MELHOR'].min()

aux = groupby
aux.name = 'melhor_MPA'
log = log.set_index(['modelo', 'ID'])
log = log.join(aux)

log = log.loc[log['MPA_MELHOR'] == log['melhor_MPA']]
log = log.reset_index()
aux = log.groupby(['modelo', 'ID'])['ITERACAO'].min()

aux.name = 'min_ITERACAO'
log = log.set_index(['modelo', 'ID'])
log = log.join(aux)

log = log.loc[log['ITERACAO'] == log['min_ITERACAO']]
log = log.drop(['melhor_MPA', 'min_ITERACAO'], axis=1)

log.to_csv(home_dir + '\\analysis\\best_results.csv', index=True, sep=';')
