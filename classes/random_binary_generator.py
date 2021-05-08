# -*- coding: utf-8 -*-
"""
Created on Fri May  7 06:44:13 2021

@author: leoml
"""

import random

__all__ = ['RandomBinaryGenerator']

class RandomBinaryGenerator(object):
    
    def __init__(self, bits):
        self.bits = bits
    
    def random_binary(self):
        number = ''
        for i in range(self.bits):
            number += str(round(random.random()))
        return number
    
    def simple_binary_tweak(self, x):
        assert type(x) == str
        
        tweak_index = random.randint(0, len(x) - 1)
        
        if x[tweak_index] == '0':
            return x[:tweak_index] + '1' + x[tweak_index + 1:]
        else:
            return x[:tweak_index] + '0' + x[tweak_index + 1:]
    
    def bit_flip_mutation(self, param):
        p = 1 / self.bits
        ans = param
        
        for i in range(self.bits):
            if p >= random.random():
                if ans[i] == '0':
                    ans = ans[:i] + '1' + ans[i + 1:]
                else:
                    ans = ans[:i] + '0' + ans[i + 1:]
        
        return ans