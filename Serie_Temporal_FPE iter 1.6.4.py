# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:38:32 2021

@author: leoml
"""
import sys
import warnings
warnings.filterwarnings('ignore')
import os
from dotenv import load_dotenv, find_dotenv

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())

home_dir = os.getenv("HOME_DIR")

sys.path.append(home_dir + '\\classes')

import pandas as pd
import numpy as np

from sarimax_constructor import SARIMAX_Constructor
from holt_constructor import Holt_Constructor
from hill_climb import HillClimbOptimization
from simulated_annealing import SimulatedAnnealingOptimization

fpe = pd.read_csv(home_dir + '\\data\\preprocessed\\FPE.csv', sep=';', index_col='Data')['Total']

# Endog
fpe_1m = fpe.loc[fpe.index < fpe.index[-11]]
fpe_6m = fpe.loc[fpe.index < fpe.index[-6]]
fpe_12m = fpe

#Metodo que vai calcular o Erro do Modelo-SARIMAX
def calculo_erro_sarimax(desp_serie, param, intervalo):
    arr_real =[]
    inter_real = []
    for i in range(intervalo):
        max_size = max(desp_serie.index)
        arr_real.append(desp_serie[max_size])
        inter_real.append(max_size)
        desp_serie = desp_serie.drop(max_size)

    sarimax_const = SARIMAX_Constructor()
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
# 1m

warnings.filterwarnings('ignore')
intervalo = 1

# hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 16)

# hill_holts.start_random_initialization(25, intervalo, fpe_1m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_1m)

# test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_1m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(1000, intervalo, fpe_1m)

# log_holts.to_csv('log_holts_hill_climb_1m.csv', sep=';')
log_sarimax.to_csv('\\data\\logs\\log_sarimax_hill_climb_1m.csv', sep=';')


# =============================================================================
# anneal = SimulatedAnnealingOptimization()
# anneal.start_random_initialization(25, intervalo)
# test_results_holt, log_holts = anneal.optimize(1000, intervalo)
# 
# log_holts.to_csv('log_holts_simulated_annealing_1m.csv', sep=';')
# =============================================================================

# =============================================================================
# 6 m
intervalo = 6

# hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 16)

# hill_holts.start_random_initialization(25, intervalo, fpe_1m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_6m)

# test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_1m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(1000, intervalo, fpe_1m)

# log_holts.to_csv('log_holts_hill_climb_1m.csv', sep=';')
log_sarimax.to_csv('\\data\\logs\\log_sarimax_hill_climb_6m.csv', sep=';')


# =============================================================================
# 12 m
intervalo = 12

# hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 16)

# hill_holts.start_random_initialization(25, intervalo, fpe_1m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_12m)

# test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_1m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(1000, intervalo, fpe_1m)

# log_holts.to_csv('log_holts_hill_climb_1m.csv', sep=';')
log_sarimax.to_csv('\\data\\logs\\log_sarimax_hill_climb_12m.csv', sep=';')

# =============================================================================
# fpe = fpe_6m
# intervalo = 6
# 
# hill = HillClimbOptimization()
# hill.start_random_initialization(25, intervalo)
# test_results_holt, log_holts = hill.optimize(1000, intervalo)
# 
# log_holts.to_csv('log_holts_hill_climb_6m.csv', sep=';')
# 
# anneal = SimulatedAnnealingOptimization()
# anneal.start_random_initialization(25, intervalo)
# test_results_holt, log_holts = anneal.optimize(1000, intervalo)
# 
# log_holts.to_csv('log_holts_simulated_annealing_6m.csv', sep=';')
# 
# fpe = fpe_12m
# intervalo = 12
# 
# hill = HillClimbOptimization()
# hill.start_random_initialization(25, intervalo)
# test_results_holt, log_holts = hill.optimize(1000, intervalo)
# 
# log_holts.to_csv('log_holts_hill_climb_12m.csv', sep=';')
# 
# anneal = SimulatedAnnealingOptimization()
# anneal.start_random_initialization(25, intervalo)
# test_results_holt, log_holts = anneal.optimize(1000, intervalo)
# 
# log_holts.to_csv('log_holts_simulated_annealing_12m.csv', sep=';')
# =============================================================================

# test_results_holt = pd.DataFrame(test_results_holt)
# log_holts = pd.DataFrame(log_holts)