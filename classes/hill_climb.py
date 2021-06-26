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
    
    def __init__(self, f_calcular_erro, bits):
        self.generator = RandomBinaryGenerator(bits)
        self.bits = bits
        self.log = {
            'ID': [],
            'ITERACAO': [],
            'PARAM_ATUAL': [],
            'MPA_ATUAL': [],
            'PARAM_MELHOR': [],
            'MPA_MELHOR': []
        }
        self.test_results = {
            'ID': [],
            'ITERACOES': [],
            'PARAM': [],
            'MPA': []
        }
        self.f_calcular_erro = f_calcular_erro
    
    def start_random_initialization(self, n, intervalo, fpe):
        for i in range(n):
            print('init: ', i)
            param = self.generator.random_binary()
            
            erro_medio = self.f_calcular_erro(fpe, param, intervalo)
            
            self.test_results['ID'].append(i)
            self.test_results['ITERACOES'].append(1)
            self.test_results['PARAM'].append(param)
            self.test_results['MPA'].append(erro_medio)
            
            self.log = {
                'ID': self.test_results['ID'].copy(),
                'ITERACAO': self.test_results['ITERACOES'].copy(),
                'PARAM_ATUAL': self.test_results['PARAM'].copy(),
                'MPA_ATUAL': self.test_results['MPA'].copy(),
                'PARAM_MELHOR': self.test_results['PARAM'].copy(),
                'MPA_MELHOR': self.test_results['MPA'].copy()
            }

    def optimize(self, max_iter, intervalo, fpe):
        for i in range(len(self.test_results['ITERACOES'])):
            print('Iteração: ', i + 1)
            # tentativas_sem_melhoria = 0
            
            while self.test_results['ITERACOES'][i] < max_iter:
                self.test_results['ITERACOES'][i] += 1
                # tentativas_sem_melhoria += 1
                
                if self.test_results['ITERACOES'][i] % 10 == 0: print('i: ', self.test_results['ITERACOES'][i])
                
                id_ = self.test_results['ID'][i]
                param = self.generator.bit_flip_mutation(self.test_results['PARAM'][i], 1/self.bits)
                
                erro_medio = self.f_calcular_erro(fpe, param, intervalo)
                
                self.log['ID'].append(id_)
                self.log['ITERACAO'].append(self.test_results['ITERACOES'][i])
                self.log['PARAM_ATUAL'].append(param)
                self.log['MPA_ATUAL'].append(erro_medio)
                
                if erro_medio <= self.test_results['MPA'][i]:
                    self.test_results['ID'][i] = id_
                    self.test_results['PARAM'][i] = param
                    self.test_results['MPA'][i] = erro_medio
                    
                self.log['PARAM_MELHOR'].append(self.test_results['PARAM'][i])
                self.log['MPA_MELHOR'].append(self.test_results['MPA'][i])

        # return self.test_results_holt, self.log_holts
        return pd.DataFrame(self.test_results), pd.DataFrame(self.log).sort_values(by=['ID', 'ITERACAO'], ascending=True)
