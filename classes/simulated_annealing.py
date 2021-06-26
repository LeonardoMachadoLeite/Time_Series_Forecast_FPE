# -*- coding: utf-8 -*-
"""
Created on Fri May  7 06:56:58 2021

@author: leoml
"""

import sys
import warnings
import math
from functools import lru_cache
warnings.filterwarnings('ignore')

home_dir = 'E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time Series Forecast - FPE'
sys.path.append(home_dir)

import pandas as pd
import random
from random_binary_generator import RandomBinaryGenerator

class SimulatedAnnealingOptimization(object):
    
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
    
    @lru_cache(maxsize=2)
    def calc_temperatura(self, iteracao, max_iter):
        if iteracao == 0:
            return 1.0
        aux = self.calc_temperatura(iteracao - 1.0, max_iter)
        return aux / (1.0 + aux)
    
    def calc_change_pct(self, iteracao, max_iter):
        ans = math.floor(self.bits * 0.7 * math.floor((max_iter - iteracao) / 100.0) / 10.0)
        if ans > 1.0:
            return float(ans)
        return 1.0
    
    def calc_probabilidade(self, novo_erro, erro_melhor, temperatura):
        if temperatura < 0.0013: # Estabilidade do sistema
            return 0.0
        return math.exp((erro_melhor - novo_erro) / temperatura)
    
    def test_values(self, max_iter):
        for i in range(max_iter + 1):
            
            temp = self.calc_temperatura(i, max_iter)
            change = self.calc_change_pct(i, max_iter)
            prob = self.calc_probabilidade(0.3, 0.21, temp)
            
            if i % 25 == 0:
                print('\nIteração: ', i)
                print('Temperatura: ', temp)
                print('Change%: ', change)
                print('Probabilidade: ', prob)
            
    
    def optimize(self, max_iter, intervalo, fpe):
        for i in range(len(self.test_results['ITERACOES'])):
            print('Iteração: ', i + 1)
            
            while self.test_results['ITERACOES'][i] < max_iter:
                self.test_results['ITERACOES'][i] += 1
                
                temperatura = self.calc_temperatura(self.test_results['ITERACOES'][i], max_iter)
                change = self.calc_change_pct(self.test_results['ITERACOES'][i], max_iter)
                
                if self.test_results['ITERACOES'][i] % 10 == 0: print('i: ', self.test_results['ITERACOES'][i])
                
                id_ = self.test_results['ID'][i]
                param = self.generator.bit_flip_mutation(self.test_results['PARAM'][i], change / self.bits)
                
                erro_medio = self.f_calcular_erro(fpe, param, intervalo)
                
                self.log['ID'].append(id_)
                self.log['ITERACAO'].append(self.test_results['ITERACOES'][i])
                self.log['PARAM_ATUAL'].append(param)
                self.log['MPA_ATUAL'].append(erro_medio)
                
                if erro_medio <= self.test_results['MPA'][i]:
                    
                    self.test_results['ID'][i] = id_
                    self.test_results['PARAM'][i] = param
                    self.test_results['MPA'][i] = erro_medio
                else:
                    prob = self.calc_probabilidade(erro_medio, self.test_results['MPA'][i], temperatura)
                    aux = random.random()
                    
                    if aux < prob:
                        # print('Novo erro: ', erro_medio)
                        # print('Melhor erro: ', self.test_results['MPA'][i])
                        # print('Temperatura: ', temperatura)
                        # print(aux, ' < ', prob)
                        self.test_results['ID'][i] = id_
                        self.test_results['PARAM'][i] = param
                        self.test_results['MPA'][i] = erro_medio
                        
                self.log['PARAM_MELHOR'].append(self.test_results['PARAM'][i])
                self.log['MPA_MELHOR'].append(self.test_results['MPA'][i])
                    
        return pd.DataFrame(self.test_results), pd.DataFrame(self.log)

def calc_erro(fpe, param, intervalo):
    return 0.10

# sim_anneal = SimulatedAnnealingOptimization(calc_erro, 29)
# sim_anneal.calc_temperatura(769, 1000)
# sim_anneal.test_values(1000)