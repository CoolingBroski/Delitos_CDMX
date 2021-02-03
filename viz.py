import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

dic = {'MILPA ALTA' : '9',
       'BENITO JUAREZ' : '14',
       'GUSTAVO A MADERO' : '5',
        'COYOACAN' : '3',
        'MIGUEL HIDALGO' : '16',
        'LA MAGDALENA CONTRERAS' : '8',
        'TLAHUAC' : '11',
        'AZCAPOTZALCO' : '2',
        'IZTACALCO' : '6',
        'ALVARO OBREGON' : '10',
        'XOCHIMILCO' : '13',
        'VENUSTIANO CARRANZA' : '17',
        'TLALPAN' : '12',
        'CUAJIMALPA DE MORELOS' : '4',
        'CUAUHTEMOC' : '15',
        'IZTAPALAPA' : '7'}

def preprocessing(delito_in):
    global dic
    
    delito = delito_in.loc[delito_in['latitud'] != 'NA']
    delito_count = delito.groupby(['alcaldia_he', 'delito']).agg(['count']).max(axis=1).reset_index(name='count')
    delito_count['municipio'] = delito_count['alcaldia_he'].apply(lambda x: dic[x])
    
    delito_count = pd.DataFrame(delito_count)
    
    delito_count = delito_count.astype({'count': float})
    
    return delito, delito_count

def select(d, delito_count, alcaldia_in):
    
    delito_d = delito_count.loc[delito_count['delito'] == d].copy()
    alcaldia = alcaldia_in.merge(delito_d, how = 'outer', on='municipio')
    nans = alcaldia.loc[np.isnan(alcaldia['count'])][['municipio', 'count']]
    alcaldia.fillna(0, inplace=True)
    delito_d = delito_d.append(nans)
    delito_d.fillna(0, inplace=True)
    
    return alcaldia, delito_d
    
