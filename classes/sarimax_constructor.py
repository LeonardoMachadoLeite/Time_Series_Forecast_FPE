# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:00:03 2021

@author: leoml
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import statsmodels.api as sm
import random
from functools import lru_cache

import time
def measuretime(func):
    def wrapper():
        starttime = time.perf_counter()
        func()
        endtime = time.perf_counter()
        print(f"Time needed: {endtime - starttime} seconds")
    return wrapper

def random_binary(bits):
        number = ''
        for i in range(bits):
            number += str(round(random.random()))
        return number

__all__ = ['SARIMAX_Constructor']

class SARIMAX_Constructor(object):
    
    def __init__(self, fpe, log = []):
        self.args = '1'*26
        self.dic = {
            'p': list(range(0, 0 + 5)),
            'd': list(range(5, 5 + 5)),
            'q': list(range(10, 10 + 5)),
            'measurement_error': 15,
            'time_varying_reg': 16,
            'enforce_stationary': 17,
            'enforce_invertibility': 18,
            'concentrate_scale': 19,
            'cov_type': list(range(20, 20 + 3)),
            'method': list(range(23, 23 + 3))
        }
        self.methods = [
            'nm',
            'nm',
            'bfgs',
            'lbfgs',
            'powell',
            'cg',
            'ncg',
            'basinhopping'
        ]
        self.cov_types = [
            'opg',
            'oim',
            'robust_approx',
            'robust',
            'robust_approx',
            'none'
        ]
        self.fpe = fpe
        self.log = log
    
    def create_SARIMAX(self, series, param):
        assert type(param) == str
        self.args = param
        
        # self.print_params()
        
        # if self.args[self.dic['time_varying_reg']] == '1' and self.args[self.dic['mle_regression']] == '1':
        #     # print('inside if')
        #     i = self.dic['mle_regression']
        #     self.args = param[:i] + '0' + param[i+1:]
        
        p = self.get_int('p')
        d = self.get_int('d')
        q = self.get_int('q')
        
        # self.print_params(param)
        self.sarimax = sm.tsa.statespace.SARIMAX(
                                  endog=series.to_numpy(),
                                  order=(p, d, q),
                                  seasonal_order=(0, 0, 0, 0),
                                  initialization='approximate_diffuse',
                                  measurement_error=self.get_bool('measurement_error'),
                                  time_varying_regression=self.get_bool('time_varying_reg'),
                                  enforce_stationarity=self.get_bool('enforce_stationary'),
                                  enforce_invertibility=self.get_bool('enforce_invertibility'),
                                  concentrate_scale=self.get_bool('concentrate_scale'),
                                  hamilton_representation=False,
                                  mle_regression=False)
        
        return self
    
    def fit(self):
        # print('fit_method: ', self.get_method())
        # print('cov_type: ', self.get_cov_type())
        return self.sarimax.fit(cov_type=self.get_cov_type(), method=self.get_method(), disp=False)
    
    def get_bool(self, par_name):
        return self.args[self.dic[par_name]] == '1'
    
    def get_int(self, par_name):
        indices = self.dic[par_name]
        return int(self.args[indices[0]:indices[-1]], 2)

    def get_method(self):
        return self.methods[self.get_int('method')]
    
    def get_cov_type(self):
        aux = self.get_int('method') % 6
        return self.cov_types[aux]
        
    def print_params(self):
        p = self.get_int('p')
        d = self.get_int('d')
        q = self.get_int('q')
        
        print('order=(', p, ', ', d, ', ', q,')')
        print('seasonal_order=(0, 0, 0, 0)')
        print("initialization='approximate_diffuse'")
        print('measurement_error=', self.get_bool('measurement_error'))
        print('time_varying_regression=', self.get_bool('time_varying_reg'))
        print('enforce_stationarity=', self.get_bool('enforce_stationary'))
        print('enforce_invertibility=', self.get_bool('enforce_invertibility'))
        print('concenprint(trate_scale=', self.get_bool('concentrate_scale'))
        print('fit_method=', self.get_method())
        print('cov_type=', self.get_cov_type())
    
    @lru_cache(maxsize=100)
    def fit_model(self, param):
        starttime = time.perf_counter()
        self.log.append(('C', param, 'Creating SARIMAX', None))
        
        model = self.create_SARIMAX(self.fpe, param)
        
        self.log.append(('F1', param, 'Before fitting', None))
        model_fit = model.fit()
        
        endtime = time.perf_counter()
        self.log.append(('F2', param, 'After fitting', endtime - starttime))
        
        return model_fit

# =============================================================================
# fpe = pd.read_csv('E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time_Series_Forecast_FPE\\data\\preprocessed\\FPE.csv', sep=';', index_col='Data')['Total']
# 
# # row = '00000110000000111101101010'
# # row = '1'*26
# 
# # 'measurement_error': 0
# # 'time_varying_reg': 0 or 1
# # 'simple_differencing': 1
# # 'enforce_stationary': 0
# # 'enforce_invertibility': 0
# # 'concentrate_scale': 0
# # 'mle_regression': 0
# 
# 
# 
# try:
#     
#     for i in range(5):
#         starttime = time.perf_counter()
#         row = random_binary(25)
#         
#         print('\ni: ', i)
#         print('Args: ', row)
#         model_fit = SARIMAX_Constructor().fit_model(row)
#         
#         endtime = time.perf_counter()
#         print(f"Time needed: {endtime - starttime} seconds")
# except Exception as e:
#     a = str(e)
#     print('Error: ', a)
# =============================================================================
