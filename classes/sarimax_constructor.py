# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:00:03 2021

@author: leoml
"""

import statsmodels.api as sm

#row = '1'*24

__all__ = ['SARIMAX_Constructor']

class SARIMAX_Constructor(object):
    
    def __init__(self):
        self.args = '1'*24
        self.dic = {
            'measurement_error': 0,
            'time_varying_reg': 1,
            'simple_differencing': 2,
            'enforce_stationary': 3,
            'enforce_invertibility': 4,
            'hamilton_repres': 5,
            'concentrate_scale': 6,
            'mle_regression': 7,
            'p': list(range(8, 8 + 5)),
            'd': list(range(13, 13 + 5)),
            'q': list(range(18, 18 + 5))
        }
    
    def create_SARIMAX(self, series, param):
        assert type(param) == str
        self.args = param
        
        # self.print_params(param)
        
        if self.args[self.dic['time_varying_reg']] == '1' and self.args[self.dic['mle_regression']] == '1':
            # print('inside if')
            i = self.dic['mle_regression']
            self.args = param[:i] + '0' + param[i+1:]
        
        p = self.get_float('p')
        d = self.get_float('d')
        q = self.get_float('q')
        
        # self.print_params(param)
        return sm.tsa.statespace.SARIMAX(
                                  endog=series.to_numpy(),
                                  order=(p, d, q),
                                  measurement_error=self.get_bool('measurement_error'),
                                  time_varying_regression=self.get_bool('time_varying_reg'),
                                  simple_differencing=self.get_bool('simple_differencing'),
                                  enforce_stationarity=self.get_bool('enforce_stationary'),
                                  enforce_invertibility=self.get_bool('enforce_invertibility'),
                                  hamilton_representation=self.get_bool('hamilton_repres'),
                                  concentrate_scale=self.get_bool('concentrate_scale'),
                                  mle_regression=self.get_bool('mle_regression'))
    
    def get_bool(self, par_name):
        return self.args[self.dic[par_name]] == '1'
    
    def get_float(self, par_name):
        indices = self.dic[par_name]
        return int(self.args[indices[0]:indices[-1]], 2)
    
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

# =============================================================================
# sarimax_const = SARIMAX_Constructor()
# sarimax_const.get_float('q')
# 
# model = sarimax_const.create_SARIMAX(pd.Series([0, 1, 2, 3]), row)
# =============================================================================
