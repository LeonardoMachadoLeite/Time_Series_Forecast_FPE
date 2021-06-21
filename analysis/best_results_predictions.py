# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 17:53:35 2021

@author: leoml
"""

import sys
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())

home_dir = os.getenv("HOME_DIR")

sys.path.append(home_dir + '\\classes')

from sarimax_constructor import SARIMAX_Constructor
from holt_constructor import Holt_Constructor

fpe = pd.read_csv(home_dir + '\\data\\preprocessed\\FPE.csv', sep=';', index_col='Data')['Total']

# Endog
fpe_1m = fpe.loc[fpe.index < fpe.index[-11]]
fpe_6m = fpe.loc[fpe.index < fpe.index[-6]]
fpe_12m = fpe

params = pd.read_csv(home_dir + '\\analysis\\best_parameters.csv', sep=';')

#Metodo que vai calcular o Erro do Modelo-SARIMAX
def treinar_sarimax(desp_serie, param, intervalo):
    arr_real =[]
    inter_real = []
    for i in range(intervalo):
        max_size = max(desp_serie.index)
        arr_real.append(desp_serie[max_size])
        inter_real.append(max_size)
        desp_serie = desp_serie.drop(max_size)

    model_fit = SARIMAX_Constructor(desp_serie).fit_model(param)

    start = len(desp_serie)
    end = len(desp_serie)+intervalo-1
    previsto = model_fit.predict(start = start, end = end)

    return previsto

#Metodo que vai calcular o Erro do Modelo Holt-Winters
def treinar_holt(desp_serie, param, intervalo):
    arr_real =[]
    inter_real = []
    
    for i in range(intervalo):
        max_size = max(desp_serie.index)
        arr_real.append(desp_serie[max_size])
        inter_real.append(max_size)
        desp_serie = desp_serie.drop(max_size)

    holt_const = Holt_Constructor()
    model_fit = holt_const.create_Holt_Winters(desp_serie, param)

    start = len(desp_serie)
    end = len(desp_serie)+intervalo-1

    previsto = model_fit.predict(start = start, end = end)

    return previsto


def get_holts(df):
    return df[df['modelo'].apply(lambda x: 'holts' in x)]

def get_sarimax(df):
    return df[df['modelo'].apply(lambda x: 'sarimax' in x)]

def get_hill_climb(df):
    return df[df['modelo'].apply(lambda x: 'hill_climb' in x)]

def get_simulated_annealing(df):
    return df[df['modelo'].apply(lambda x: 'simulated_annealing' in x)]

params_holts = []
params_sarimax = []

for periodo in [1, 6, 12]:
    aux = params.loc[params['periodo'] == periodo]
    
    holt_param = get_holts(aux)
    sarimax_param = get_sarimax(aux)
    
    best_param_holts = holt_param.sort_values(by='MPA_ATUAL')['PARAM_ATUAL'].iloc[0]
    best_param_sarimax = sarimax_param.sort_values(by='MPA_ATUAL')['PARAM_ATUAL'].iloc[0]
    
    params_holts.append(best_param_holts)
    params_sarimax.append(best_param_sarimax)

trained_holts = [
    treinar_holt(fpe_1m, params_holts[0], 1),
    treinar_holt(fpe_6m, params_holts[1], 6),
    treinar_holt(fpe_12m, params_holts[2], 12)
    ]
trained_sarimax = [
    treinar_sarimax(fpe_1m, params_sarimax[0], 1),
    treinar_sarimax(fpe_6m, params_sarimax[1], 6),
    treinar_sarimax(fpe_12m, params_sarimax[2], 12)
    ]


real_fpe = fpe.loc[fpe.index > fpe.index[-13]].tolist()

# Holt-Winters Predict
holts_predict_1m = pd.DataFrame({'PREDICT': trained_holts[0]})
holts_predict_1m['MODELO'] = 'HOLTS_PREDICT_1M'
holts_predict_1m['DATA'] = pd.date_range(start='01/01/2019', end='02/01/2019', freq='M')

holts_predict_6m = pd.DataFrame({'PREDICT': trained_holts[1]})
holts_predict_6m['MODELO'] = 'HOLTS_PREDICT_6M'
holts_predict_6m['DATA'] = pd.date_range(start='01/01/2019', end='07/01/2019', freq='M')

holts_predict_12m = pd.DataFrame({'PREDICT': trained_holts[2]})
holts_predict_12m['MODELO'] = 'HOLTS_PREDICT_12M'
holts_predict_12m['DATA'] = pd.date_range(start='01/01/2019', end='01/01/2020', freq='M')


#SARIMA Predict
sarimax_predict_1m = pd.DataFrame({'PREDICT': trained_sarimax[0]})
sarimax_predict_1m['MODELO'] = 'SARIMA_PREDICT_1M'
sarimax_predict_1m['DATA'] = pd.date_range(start='01/01/2019', end='02/01/2019', freq='M')

sarimax_predict_6m = pd.DataFrame({'PREDICT': trained_sarimax[1]})
sarimax_predict_6m['MODELO'] = 'SARIMA_PREDICT_6M'
sarimax_predict_6m['DATA'] = pd.date_range(start='01/01/2019', end='07/01/2019', freq='M')

sarimax_predict_12m = pd.DataFrame({'PREDICT': trained_sarimax[2]})
sarimax_predict_12m['MODELO'] = 'SARIMA_PREDICT_12M'
sarimax_predict_12m['DATA'] = pd.date_range(start='01/01/2019', end='01/01/2020', freq='M')

#FPE Real
real_fpe = pd.DataFrame({'PREDICT': fpe.loc[fpe.index > fpe.index[-13]].tolist()})
real_fpe['MODELO'] = 'FPE_REAL'
real_fpe['DATA'] = pd.date_range(start='01/01/2019', end='01/01/2020', freq='M')


predictions = pd.concat([holts_predict_1m, holts_predict_6m, holts_predict_12m,
                         sarimax_predict_1m, sarimax_predict_6m, sarimax_predict_12m,
                         real_fpe])
predictions.to_csv(home_dir + '\\analysis\\predictions.csv', index=False, sep=';')

