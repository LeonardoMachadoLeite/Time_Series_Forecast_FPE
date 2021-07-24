# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 15:49:29 2021

@author: leoml
"""


import sys
import os
import pandas as pd
import numpy as np
from sarimax_constructor import SARIMAX_Constructor
from holt_constructor import Holt_Constructor
from dotenv import load_dotenv, find_dotenv
from database_connection import *

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())

home_dir = os.getenv("HOME_DIR")

sys.path.append(home_dir + '\\classes')

class Executor(object):
    
    def __init__(self, idt_exec, idt_modelo, idt_periodo):
        self.idt_exec = idt_exec
        self.idt_modelo = idt_modelo
        self.idt_periodo = idt_periodo
        
        self.db = DatabaseConnection()
        self.cols = TableColumns()
    
    #Metodo que vai calcular o Erro do Modelo-SARIMAX
    def calculo_erro_sarimax(self, desp_serie, param, intervalo):
        try:
            arr_real =[]
            inter_real = []
            for i in range(intervalo):
                max_size = max(desp_serie.index)
                arr_real.append(desp_serie[max_size])
                inter_real.append(max_size)
                desp_serie = desp_serie.drop(max_size)
            
            v_mape = None
            v_mape = self.db.obter_cenario_mape(self.idt_modelo, self.idt_periodo, param, v_mape)
            
            if v_mape != None:
                self.db.inserir_log_exec(self.idt_exec, self.idt_modelo, self.idt_periodo, param, v_mape)
                return v_mape
            
            constructor = SARIMAX_Constructor(desp_serie, param)
            model_fit = constructor.fit_model()
        
            start = len(desp_serie)
            end = len(desp_serie)+intervalo - 1
        
            previsto = model_fit.predict(start = start, end = end)
            serie_real = pd.Series(arr_real, inter_real)
        
            size = len(previsto)
            erro = []
        
            for i in range(size):
                parc_erro = (previsto[i] - serie_real.iloc[i])/serie_real.iloc[i]
                erro.append(abs(parc_erro))
        
            erro_medio = abs(np.mean(erro))
            self.db.inserir_log_exec(self.idt_exec, self.idt_modelo, self.idt_periodo, param, erro_medio)
            return erro_medio
        except Exception as e:
            #exec_log.append(('E', param, str(e), None))
            self.db.inserir_log_exec(self.idt_exec, self.idt_modelo, self.idt_periodo, param, 99999)
            return 99999

    #Metodo que vai calcular o Erro do Modelo Holt-Winters
    def calculo_erro_holt(self, desp_serie, param, intervalo):
        arr_real =[]
        inter_real = []
        for i in range(intervalo):
            max_size = max(desp_serie.index)
            arr_real.append(desp_serie[max_size])
            inter_real.append(max_size)
            desp_serie = desp_serie.drop(max_size)
    
    
        holt_const = Holt_Constructor()
        model_fit = holt_const.create_Holt_Winters(desp_serie, param)
    
        start = len(desp_serie)
        end = len(desp_serie)+intervalo-1
    
        previsto = model_fit.predict(start = start, end = end)
        serie_real = pd.Series(arr_real, inter_real)
    
        size = len(previsto)
        erro = []
    
        for i in range(size):
            parc_erro = (previsto[i] - serie_real.iloc[i])/serie_real.iloc[i]
            erro.append(abs(parc_erro))
    
        erro_medio = np.mean(erro)
        if pd.isna(erro_medio):
            return 1.0
        return abs(erro_medio)
    
    def close(self):
        self.db.close()