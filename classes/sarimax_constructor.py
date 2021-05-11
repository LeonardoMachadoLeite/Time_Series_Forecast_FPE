# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:00:03 2021

@author: leoml
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import statsmodels.api as sm

import time
def measuretime(func):
    def wrapper():
        starttime = time.perf_counter()
        func()
        endtime = time.perf_counter()
        print(f"Time needed: {endtime - starttime} seconds")
    return wrapper

__all__ = ['SARIMAX_Constructor']

class SARIMAX_Constructor(object):
    
    def __init__(self):
        self.args = '1'*23
        self.dic = {
            'measurement_error': 0,
            'time_varying_reg': 1,
            'enforce_stationary': 2,
            'enforce_invertibility': 3,
            'concentrate_scale': 4,
            'cov_type': 5,
            'trend_offset': 6,
            'method': 7,
            'p': list(range(8, 8 + 5)),
            'd': list(range(13, 13 + 5)),
            'q': list(range(18, 18 + 5))
        }
    
    def create_SARIMAX(self, series, param):
        assert type(param) == str
        self.args = param
        
        # self.print_params(param)
        
        # if self.args[self.dic['time_varying_reg']] == '1' and self.args[self.dic['mle_regression']] == '1':
        #     # print('inside if')
        #     i = self.dic['mle_regression']
        #     self.args = param[:i] + '0' + param[i+1:]
        
        p = self.get_float('p')
        d = self.get_float('d')
        q = self.get_float('q')
        
        # self.print_params(param)
        return sm.tsa.statespace.SARIMAX(
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
    
    def get_bool(self, par_name):
        return self.args[self.dic[par_name]] == '1'
    
    def get_float(self, par_name):
        indices = self.dic[par_name]
        return int(self.args[indices[0]:indices[-1]], 2)

# =============================================================================
# fpe = pd.read_csv('E:\\leoml\\Documents\\Leonardo\\SEFAZ\\FPE\\Time_Series_Forecast_FPE\\data\\preprocessed\\FPE.csv', sep=';', index_col='Data')['Total']
# 
# row = '1'*16
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
# sarimax_const = SARIMAX_Constructor()
# 
# model = sarimax_const.create_SARIMAX(fpe, row)
# 
# print(row)
# @measuretime
# def fit():
#     model.fit(fpe)
# 
# ret = fit()
# =============================================================================

