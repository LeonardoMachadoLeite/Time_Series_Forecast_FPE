# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:17:38 2021

@author: leoml
"""


import os
from dotenv import load_dotenv, find_dotenv
import mysql.connector
import pandas as pd

__all__ = ['DatabaseConnection', 'TableColumns']

# Connect the path with your '.env' file name
load_dotenv(find_dotenv())


class DatabaseConnection(object):
    
    def __init__(self):
        self.cnx = mysql.connector.connect(user=os.getenv("USER"),
                              password=os.getenv("PASSWORD"),
                              host=os.getenv("HOST"),
                              database=os.getenv("DATABASE"))
    
    def query(self, sql, cursor = None):
        if cursor == None:
            cursor = self.cnx.cursor()
        
        cursor.execute(sql)
        
        ans = []
        for row in cursor:
            ans.append(row)
        
        cursor.close()
        return ans
    
    def obter_cenario_mape(self, v_idt_modelo, v_idt_periodo, v_parametro, v_mape):
        cursor = self.cnx.cursor()
        
        cursor.callproc('obter_cenario_mape', args=(v_idt_modelo, v_idt_periodo, v_parametro, v_mape))
        
        return cursor
    
    def inserir_log_exec(self, v_idt_exec, v_idt_modelo, v_idt_periodo, v_parametro, v_mape):
        cursor = self.cnx.cursor()
        
        cursor.callproc('inserir_log_exec', args=(v_idt_exec, v_idt_modelo, v_idt_periodo, v_parametro, v_mape))
        
        return cursor
    
    def close(self):
        self.cnx.close()

class TableColumns():
    
    def modelo(self):
        return ['IDT_MODELO', 'DSC_MODELO']
    
    def cenario(self):
        return ['IDT_CENARIO', 'IDT_MODELO', 'IDT_PERIODO', 'PARAMETRO', 'MAPE']
    
    def periodo(self):
        return ['IDT_PERIODO', 'INICIO', 'FIM', 'DURACAO']

class SarimaDbController():
    
    def __init__(self, periodo, modelo):
        self.idt_periodo = periodo
        self.idt_modelo = modelo
    
    def get_mape(self):
        return 0


# =============================================================================
# db = DatabaseConnection()
# cols = TableColumns()
# =============================================================================

# =============================================================================
# result = db.query("""
#                   select * from modelo_previsao;
#                   """)
# 
# model = pd.DataFrame(data=result, columns=cols.modelo())
# 
# print(model)
# =============================================================================

