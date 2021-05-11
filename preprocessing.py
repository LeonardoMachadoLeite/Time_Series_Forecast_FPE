# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:55:17 2021

@author: leoml
"""

import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
home_dir = os.environ['HOME_DIR']

def cvt_currency_to_float(value):
    result = value[2:].replace('.','')
    result = result.replace(',','.')
    return float(result)
    

fpe = pd.read_csv(home_dir + '\\data\\raw\\detalhamento_transferencias.csv', sep=';', encoding='latin1')

fpe.index = pd.date_range(start='31/01/1997', end='28/02/2021', freq='M')
fpe = fpe.loc[fpe.index < '01/01/2020']
fpe['Total'] = fpe['Total'].apply(lambda x: cvt_currency_to_float(x))
fpe.drop(['UF', 'Ano', 'Mês', 'Transferência',
          '1º Decêndio', '2º Decêndio', '3º Decêndio'], axis = 1, inplace=True)

fpe = fpe.reset_index()
fpe.rename({'index':'Data'}, axis=1, inplace=True)

fpe.to_csv(home_dir + '\\data\\preprocessed\\FPE.csv', sep=';', index=False)
