# -*- coding: utf-8 -*-
"""
Created on Fri May  7 06:47:37 2021

@author: leoml
"""

import sys
import warnings
warnings.filterwarnings('ignore')

home_dir = 'E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time Series Forecast - FPE'
sys.path.append(home_dir)

import pandas as pd
from random_binary_generator import RandomBinaryGenerator

class HillClimbOptimization(object):
    
    def __init__(self, f_calcular_erro):
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
        self.f_calcular_erro = f_calcular_erro
    
    def start_random_initialization(self, n, intevalo, fpe):
        for i in range(n):
            param = self.generator.random_binary()
            
            erro_medio = self.f_calcular_erro(fpe, param, 1)
            
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

    def optimize(self, max_iter, intervalo, fpe):
        for i in range(len(self.test_results_holt['ITERACOES'])):
            print('Iteração: ', i + 1)
            tentativas_sem_melhoria = 0
            
            while self.test_results_holt['ITERACOES'][i] < max_iter:
                self.test_results_holt['ITERACOES'][i] += 1
                tentativas_sem_melhoria += 1
                
                id_ = self.test_results_holt['ID'][i]
                param = self.generator.bit_flip_mutation(self.test_results_holt['PARAM'][i])
                
                erro_medio = self.f_calcular_erro(fpe, param, intervalo)
                
                self.log_holts['ID'].append(id_)
                self.log_holts['ITERACAO'].append(self.test_results_holt['ITERACOES'][i])
                self.log_holts['PARAM_ATUAL'].append(param)
                self.log_holts['MPA_ATUAL'].append(erro_medio)
                
                if erro_medio <= self.test_results_holt['MPA'][i]:
                    tentativas_sem_melhoria = 0
                    
                    self.test_results_holt['ID'][i] = id_
                    self.test_results_holt['PARAM'][i] = param
                    self.test_results_holt['MPA'][i] = erro_medio
                    
                self.log_holts['PARAM_MELHOR'].append(self.test_results_holt['PARAM'][i])
                self.log_holts['MPA_MELHOR'].append(self.test_results_holt['MPA'][i])

        # return self.test_results_holt, self.log_holts
        return pd.DataFrame(self.test_results_holt), pd.DataFrame(self.log_holts).sort_values(by=['ID', 'ITERACAO'], ascending=True)
