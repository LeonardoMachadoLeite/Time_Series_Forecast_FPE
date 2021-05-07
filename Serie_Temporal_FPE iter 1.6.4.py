# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:38:32 2021

@author: leoml
"""
import sys
import warnings
warnings.filterwarnings('ignore')

home_dir = 'E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time Series Forecast - FPE'
sys.path.append(home_dir)

import statsmodels.api as sm
from statsmodels.tsa.api import Holt
import pandas as pd
import numpy as np

from sarimax_constructor import SARIMAX_Constructor
from holt_constructor import Holt_Constructor
from random_binary_generator import RandomBinaryGenerator
from hill_climb import HillClimbOptimization
from simulated_annealing import SimulatedAnnealingOptimization

# Endog
fpe_1m = pd.read_csv(home_dir + '\\FPE_1_M.csv', sep=';', index_col='Data')['Total']
fpe_6m = pd.read_csv(home_dir + '\\FPE_6_M.csv', sep=';', index_col='Data')['Total']
fpe_12m = pd.read_csv(home_dir + '\\FPE_12_M.csv', sep=';', index_col='Data')['Total']

#Metodo que vai calcular o Erro do Modelo-SARIMAX
def calculo_erro_sarimax(desp_serie, param, intervalo):
    arr_real =[]
    inter_real = []
    for i in range(intervalo):
        max_size = max(desp_serie.index)
        arr_real.append(desp_serie[max_size])
        inter_real.append(max_size)
        desp_serie = desp_serie.drop(max_size)

    model = sarimax_const.create_SARIMAX(desp_serie, param)
    model_fit = model.fit(disp=0, cov_type='none', method='bfgs')

    start = len(desp_serie)
    end = len(desp_serie)+intervalo-1

    previsto = model_fit.predict(start = start, end = end)
    serie_real = pd.Series(arr_real, inter_real)

    size = len(previsto)
    erro = []

    for i in range(size):
        parc_erro = (previsto[i] - serie_real.iloc[i])/serie_real.iloc[i]
        erro.append(abs(parc_erro))

    erro_medio = np.mean(erro)
    return abs(erro_medio)

#Metodo que vai calcular o Erro do Modelo Holt-Winters
def calculo_erro_holt(desp_serie, param, intervalo):
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
    serie_real = pd.Series(arr_real, inter_real)

    size = len(previsto)
    erro = []

    for i in range(size):
        parc_erro = (previsto[i] - serie_real.iloc[i])/serie_real.iloc[i]
        erro.append(abs(parc_erro))

    erro_medio = np.mean(erro)
    return abs(erro_medio)
                

#Execução dos testes SARIMAX
sarimax_const = SARIMAX_Constructor()

test_results_sarimax = {
    'ID': [],
    'MPA': []
}
params = list(range(256))



# for i in range(256):
#     print('Iteração: ', i + 1)
#     index = random.randint(0, len(params) - 1)
#     param = params[index]
#     del params[index]
#     erro_medio = calculo_erro_sarimax(fpe_1m, param, 1)
#     erro_medio = calculo_erro_sarimax(fpe_1m, param, 1)
#     test_results_sarimax['ID'].append(param)
#     test_results_sarimax['MPA'].append(erro_medio)

# test_results_sarimax = pd.DataFrame(test_results_sarimax)
# print('Erro Médio SARIMAX: {:.2f}%'.format(erro_medio * 100))


warnings.filterwarnings('ignore')

fpe = fpe_1m
intervalo = 1

hill = HillClimbOptimization()
hill.start_random_initialization(25, intervalo)
test_results_holt, log_holts = hill.optimize(1000, intervalo)

log_holts.to_csv('log_holts_hill_climb_1m.csv', sep=';')

anneal = SimulatedAnnealingOptimization()
anneal.start_random_initialization(25, intervalo)
test_results_holt, log_holts = anneal.optimize(1000, intervalo)

log_holts.to_csv('log_holts_simulated_annealing_1m.csv', sep=';')

fpe = fpe_6m
intervalo = 6

hill = HillClimbOptimization()
hill.start_random_initialization(25, intervalo)
test_results_holt, log_holts = hill.optimize(1000, intervalo)

log_holts.to_csv('log_holts_hill_climb_6m.csv', sep=';')

anneal = SimulatedAnnealingOptimization()
anneal.start_random_initialization(25, intervalo)
test_results_holt, log_holts = anneal.optimize(1000, intervalo)

log_holts.to_csv('log_holts_simulated_annealing_6m.csv', sep=';')

fpe = fpe_12m
intervalo = 12

hill = HillClimbOptimization()
hill.start_random_initialization(25, intervalo)
test_results_holt, log_holts = hill.optimize(1000, intervalo)

log_holts.to_csv('log_holts_hill_climb_12m.csv', sep=';')

anneal = SimulatedAnnealingOptimization()
anneal.start_random_initialization(25, intervalo)
test_results_holt, log_holts = anneal.optimize(1000, intervalo)

log_holts.to_csv('log_holts_simulated_annealing_12m.csv', sep=';')

# test_results_holt = pd.DataFrame(test_results_holt)
# log_holts = pd.DataFrame(log_holts)