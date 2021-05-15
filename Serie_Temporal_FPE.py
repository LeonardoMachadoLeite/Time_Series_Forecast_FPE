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


exec_log = []

#Metodo que vai calcular o Erro do Modelo-SARIMAX
def calculo_erro_sarimax(desp_serie, param, intervalo):
    try:
        arr_real =[]
        inter_real = []
        for i in range(intervalo):
            max_size = max(desp_serie.index)
            arr_real.append(desp_serie[max_size])
            inter_real.append(max_size)
            desp_serie = desp_serie.drop(max_size)
    
        model_fit = SARIMAX_Constructor(desp_serie, exec_log).fit_model(param)
    
        start = len(desp_serie)
        end = len(desp_serie)+intervalo-1
    
        exec_log.append(('P1', param, 'Done', None))
        previsto = model_fit.predict(start = start, end = end)
        exec_log.append(('P2', param, 'Done', None))
        serie_real = pd.Series(arr_real, inter_real)
    
        size = len(previsto)
        erro = []
    
        for i in range(size):
            parc_erro = (previsto[i] - serie_real.iloc[i])/serie_real.iloc[i]
            erro.append(abs(parc_erro))
    
        erro_medio = np.mean(erro)
        return abs(erro_medio)
    except Exception as e:
        exec_log.append(('E', param, str(e), None))
        return 99999

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
    if pd.isna(erro_medio):
        return 1.0
    return abs(erro_medio)
                

warnings.filterwarnings('ignore')

# =============================================================================
# Hill Climb
# =============================================================================
# 1 month

intervalo = 1

hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 26)

hill_holts.start_random_initialization(25, intervalo, fpe_1m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_1m)

test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_1m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(100, intervalo, fpe_1m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_hill_climb_1m.csv', sep=';', index=False)
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_hill_climb_1m.csv', sep=';', index=False)

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt1.csv', sep=';')

# =============================================================================
# 6 months

intervalo = 6

hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 26)

hill_holts.start_random_initialization(25, intervalo, fpe_6m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_6m)

test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_6m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(100, intervalo, fpe_6m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_hill_climb_6m.csv', sep=';', index=False)
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_hill_climb_6m.csv', sep=';', index=False)

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt2.csv', sep=';')

# =============================================================================
# 12 months

intervalo = 12

hill_holts = HillClimbOptimization(calculo_erro_holt, 29)
hill_sarimax = HillClimbOptimization(calculo_erro_sarimax, 26)

hill_holts.start_random_initialization(25, intervalo, fpe_12m)
hill_sarimax.start_random_initialization(25, intervalo, fpe_12m)

test_results_holt, log_holts = hill_holts.optimize(1000, intervalo, fpe_12m)
test_results_sarimax, log_sarimax = hill_sarimax.optimize(100, intervalo, fpe_12m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_hill_climb_12m.csv', sep=';', index=False)
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_hill_climb_12m.csv', sep=';', index=False)

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt3.csv', sep=';')

# =============================================================================
# Simulated Annealing
# =============================================================================
# 1 month

intervalo = 1

anneal_holts = SimulatedAnnealingOptimization(calculo_erro_holt, 29)
anneal_sarimax = SimulatedAnnealingOptimization(calculo_erro_sarimax, 26)

anneal_holts.start_random_initialization(25, intervalo, fpe_1m)
anneal_sarimax.start_random_initialization(25, intervalo, fpe_1m)

test_results_holt, log_holts = anneal_holts.optimize(1000, intervalo, fpe_1m)
test_results_sarimax, log_sarimax = anneal_sarimax.optimize(100, intervalo, fpe_1m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_simulated_annealing_1m.csv', sep=';', index=False)
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_simulated_annealing_1m.csv', sep=';', index=False)

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt4.csv', sep=';')

# =============================================================================
# 6 months

intervalo = 6

anneal_holts = SimulatedAnnealingOptimization(calculo_erro_holt, 29)
anneal_sarimax = SimulatedAnnealingOptimization(calculo_erro_sarimax, 26)

anneal_holts.start_random_initialization(25, intervalo, fpe_6m)
anneal_sarimax.start_random_initialization(25, intervalo, fpe_6m)

test_results_holt, log_holts = anneal_holts.optimize(1000, intervalo, fpe_6m)
test_results_sarimax, log_sarimax = anneal_sarimax.optimize(100, intervalo, fpe_6m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_simulated_annealing_6m.csv', sep=';', index=False)
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_simulated_annealing_6m.csv', sep=';', index=False)

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt5.csv', sep=';')

# =============================================================================
# 12 months

intervalo = 12

anneal_holts = SimulatedAnnealingOptimization(calculo_erro_holt, 29)
anneal_sarimax = SimulatedAnnealingOptimization(calculo_erro_sarimax, 26)

anneal_holts.start_random_initialization(25, intervalo, fpe_12m)
anneal_sarimax.start_random_initialization(25, intervalo, fpe_12m)

test_results_holt, log_holts = anneal_holts.optimize(1000, intervalo, fpe_12m)
test_results_sarimax, log_sarimax = anneal_sarimax.optimize(100, intervalo, fpe_12m)

log_holts.to_csv(home_dir + '\\data\\logs\\log_holts_simulated_annealing_12m.csv', sep=';')
log_sarimax.to_csv(home_dir + '\\data\\logs\\log_sarimax_simulated_annealing_12m.csv', sep=';')

df_log = pd.DataFrame(exec_log)
df_log.to_csv(home_dir + '\\data\\logs\\exec_logs\\exec_log_pt6.csv', sep=';')