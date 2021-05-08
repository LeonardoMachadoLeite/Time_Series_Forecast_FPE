# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 18:49:18 2021

@author: leoml
"""
from statsmodels.tsa.api import Holt
import random
import math


class Holt_Constructor(object):
    
    def __init__(self):
        self.args = '1'*29
        self.dic = {
            'exponential': 0,
            'damped': 1,
            'smoothing_level': list(range(2,2 + 8)),
            'smoothing_slope': list(range(10,10 + 9)),
            'optimized': 19,
            'damping_slope': list(range(20,20 + 9)),
        }
    
    def create_Holt_Winters(self, series, param):
        assert type(param) == str
        self.args = param
        
        # self.print_params(param)
        
        model = Holt(series, 
                     exponential=self.get_bool('exponential'),
                     damped=self.get_bool('damped'))
        return model.fit(smoothing_level=self.get_float('smoothing_level'),
                              smoothing_slope=self.get_float('smoothing_slope'),
                              optimized=self.get_bool('optimized'),
                              damping_slope=self.get_float('damping_slope'))
    
    def get_bool(self, par_name):
        return self.args[self.dic[par_name]] == '1'
    
    def get_float(self, par_name):
        indices = self.dic[par_name]
        if par_name == 'smoothing_level':
            div = 100
        else:
            div = 10000
        return int(self.args[indices[0]:indices[-1]], 2) / div
    
    def print_params(self, param):
        assert type(param) == str
        self.args = param
        
        print(self.args, ' = {')
        print('\texponential =\t', self.get_bool('exponential'))
        print('\tdamped =\t', self.get_bool('damped'))
        print('\tsmoothing_lvl =\t', self.get_float('smoothing_level'))
        print('\tsmoothing_slp =\t', self.get_float('smoothing_slope'))
        print('\toptimized =\t', self.get_bool('optimized'))
        print('\tdamping_slope =\t', self.get_float('damping_slope'))
        print('}')


class RandomBinaryGenerator(object):
    
    def __init__(self, bits):
        self.bits = bits
    
    def random_binary(self):
        number = ''
        for i in range(self.bits):
            number += str(round(random.random()))
        return number

