# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 17:53:35 2021

@author: leoml
"""

# import pprint
import pandas as pd
from scipy.stats import shapiro, friedmanchisquare, kruskal, wilcoxon, shapiro
# import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv, find_dotenv

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())

home_dir = os.getenv("HOME_DIR")

log_files = [
    'log_holts_hill_climb_1m',
    'log_holts_hill_climb_6m',
    'log_holts_hill_climb_12m',
    'log_sarimax_hill_climb_1m',
    'log_sarimax_hill_climb_6m',
    'log_sarimax_hill_climb_12m',
    'log_holts_simulated_annealing_1m',
    'log_holts_simulated_annealing_6m',
    'log_holts_simulated_annealing_12m',
    'log_sarimax_simulated_annealing_1m',
    'log_sarimax_simulated_annealing_6m',
    'log_sarimax_simulated_annealing_12m'
    ]


best_results = pd.read_csv(home_dir + '\\analysis\\best_results.csv', sep=';')

results_shapiro = {}


for i in range(0,len(log_files)):
    
    modelo = log_files[i]
    
    log = best_results.loc[best_results['modelo'] == modelo]
    log = log['MPA_MELHOR']
    
    stat, p = shapiro(log)
    
    results_shapiro[modelo] = (stat, p)

print('\nShapiro Wilk nomarlity test:')
for key in results_shapiro.keys():
    print(key + ': ', results_shapiro[key])

results_wilcoxon = {}


for i in range(0,int(len(log_files) / 2)):
    
    modelo_a = log_files[i]
    modelo_b = log_files[i + int(len(log_files) / 2)]
    
    log_a = best_results.loc[best_results['modelo'] == modelo_a]
    log_a = log_a['MPA_MELHOR']
    
    log_b = best_results.loc[best_results['modelo'] == modelo_b]
    log_b = log_b['MPA_MELHOR']
    
    w, p = wilcoxon(log_a, log_b)
    
    key = modelo_a + ' x ' + modelo_b
    results_wilcoxon[key] = (w, p)

print('\nWilcoxon test:')
for key in results_wilcoxon.keys():
    print(key + ': ', results_wilcoxon[key])

# =============================================================================
# # Creating plot 
# data = ([log_a, log_b])
# plt.boxplot(data, labels=[modelo_a, modelo_b]) 
#   
# # show plot 
# plt.show()
# =============================================================================
