# -*- coding: utf-8 -*-
"""
Created on Fri May  7 06:56:58 2021

@author: leoml
"""

import sys
import warnings
warnings.filterwarnings('ignore')

home_dir = 'E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time Series Forecast - FPE'
sys.path.append(home_dir)

import pandas as pd
from random_binary_generator import RandomBinaryGenerator

class SimulatedAnnealingOptimization(object):
    
    def __init__(self):
        self.generator = RandomBinaryGenerator(29)
        self.log_holts = {
            'ID': [],
            'ITERACAO': [],
            'PARAM_ATUAL': [],
            'MPA_ATUAL': [],
            'PARAM_MELHOR': [],
            'MPA_MELHOR': []
        }
        self.test_results_holt = {
            'ID': [],
            'ITERACOES': [],
            'PARAM': [],
            'MPA': []
        }
    
    def start_random_initialization(self, n, intevalo):
        for i in range(n):
            param = self.generator.random_binary()
            
            erro_medio = calculo_erro_holt(fpe, param, 1)
            
            self.test_results_holt['ID'].append(i)
            self.test_results_holt['ITERACOES'].append(1)
            self.test_results_holt['PARAM'].append(param)
            self.test_results_holt['MPA'].append(erro_medio)
            
            self.log_holts = {
                'ID': self.test_results_holt['ID'].copy(),
                'ITERACAO': self.test_results_holt['ITERACOES'].copy(),
                'PARAM_ATUAL': self.test_results_holt['PARAM'].copy(),
                'MPA_ATUAL': self.test_results_holt['MPA'].copy(),
                'PARAM_MELHOR': self.test_results_holt['PARAM'].copy(),
                'MPA_MELHOR': self.test_results_holt['MPA'].copy()
            }
    
    def optimize(self, max_iter, intervalo):
        for i in range(len(self.test_results_holt['ITERACOES'])):
            print('Iteração: ', i + 1)
            
            while self.test_results_holt['ITERACOES'][i] < max_iter:
                self.test_results_holt['ITERACOES'][i] += 1
                
                id_ = self.test_results_holt['ID'][i]
                param = self.generator.simple_binary_tweak(self.test_results_holt['PARAM'][i])
                
                erro_medio = calculo_erro_holt(fpe, param, intervalo)
                
                self.log_holts['ID'].append(id_)
                self.log_holts['ITERACAO'].append(self.test_results_holt['ITERACOES'][i])
                self.log_holts['PARAM_ATUAL'].append(param)
                self.log_holts['MPA_ATUAL'].append(erro_medio)
                
                if erro_medio <= self.test_results_holt['MPA'][i]:
                    
                    self.test_results_holt['ID'][i] = id_
                    self.test_results_holt['PARAM'][i] = param
                    self.test_results_holt['MPA'][i] = erro_medio
                else:
                    p = 1/ (self.test_results_holt['ITERACOES'][i])
                    
                    if random.random() < p:
                        self.test_results_holt['ID'][i] = id_
                        self.test_results_holt['PARAM'][i] = param
                        self.test_results_holt['MPA'][i] = erro_medio
                        
                self.log_holts['PARAM_MELHOR'].append(self.test_results_holt['PARAM'][i])
                self.log_holts['MPA_MELHOR'].append(self.test_results_holt['MPA'][i])
                    
        return pd.DataFrame(self.test_results_holt), pd.DataFrame(self.log_holts)
