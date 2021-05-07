# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:00:03 2021

@author: leoml
"""

import pandas as pd
from datetime import datetime as dt
import statsmodels.api as sm

row = 0b111110100

class SARIMAX_Constructor(object):
    
    def __init__(self):
        self.args = '11111111'
        self.dic = {
            'measurement_error': 0,
            'time_varying_reg': 1,
            'simple_differencing': 2,
            'enforce_stationary': 3,
            'enforce_invertibility': 4,
            'hamilton_repres': 5,
            'concentrate_scale': 6,
            'mle_regression': 7
        }
    
    def create_SARIMAX(self, series, param):
        assert type(param) == int
        self.args = '{:08d}'.format(int(bin(param)[2:]))
        
        # self.print_params(param)
        
        if self.args[self.dic['time_varying_reg']] == '1' and self.args[self.dic['mle_regression']] == '1':
            # print('inside if')
            param -= 1
            self.args = '{:08d}'.format(int(bin(param)[2:]))
        
        # self.print_params(param)
        return sm.tsa.statespace.SARIMAX(
                                  endog=series.to_numpy(),
                                  order=(12, 0, 1),
                                  measurement_error=self.get('measurement_error'),
                                  time_varying_regression=self.get('time_varying_reg'),
                                  simple_differencing=self.get('simple_differencing'),
                                  enforce_stationarity=self.get('enforce_stationary'),
                                  enforce_invertibility=self.get('enforce_invertibility'),
                                  hamilton_representation=self.get('hamilton_repres'),
                                  concentrate_scale=self.get('concentrate_scale'),
                                  mle_regression=self.get('mle_regression'))
    
    def get(self, par_name):
        return self.args[self.dic[par_name]] == '1'
    
    def print_params(self, param):
        assert type(param) == int
        args = bin(param)
        print(args, ' = {')
        print('\tmeasurement_error =\t', self.get('measurement_error'))
        print('\ttime_varying_reg =\t', self.get('time_varying_reg'))
        print('\tsimple_differencing =\t', self.get('simple_differencing'))
        print('\tenforce_stationarity =\t', self.get('enforce_stationary'))
        print('\tenforce_invertibility =\t', self.get('enforce_invertibility'))
        print('\thamilton_repres =\t', self.get('hamilton_repres'))
        print('\tconcentrate_scale =\t', self.get('concentrate_scale'))
        print('\tmle_regression =\t', self.get('mle_regression'))
        print('}')

sarimax_const = SARIMAX_Constructor()
# sarimax_const.create_SARIMAX(series, row)