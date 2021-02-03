import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

from viz import *

delitos =  "datos/datoscrimen/datoscrimen.shp"
alcaldias = "datos/alcaldias/alcaldias.shp"

seccion = st.sidebar.selectbox(
    "Sección:",
    ('Introducción', 'Visualización', 'Conclusión'))
    
if seccion == 'Introducción':
    introduccion = Path('intro.md').read_text()
    st.markdown(introduccion, unsafe_allow_html=True)
    
elif seccion == 'Visualización':
    st.header('Visualización Interactiva')
    
    
    delito = gpd.read_file(delitos, SHAPE_RESTORE_SHX='YES')
    alcaldia = gpd.read_file(alcaldias, SHAPE_RESTORE_SHX='YES')
    
    delito, delito_count = preprocessing(delito)
    
    tipos_d = delito['delito'].unique()
    
    d = st.selectbox(
    'Tipo de delito',
    tipos_d)
    
    alcaldia, delito_d = select(d, delito_count, alcaldia)
    
    delito = delito.astype({'latitud': float, 'longitud': float})
    
    m = folium.Map(delito[['latitud', 'longitud']].values.mean(axis=0))

    # Los tipos de dato de los objetos feature del shape deben de coincidir con el tipo de dato en la columna del dataframe con la cual se realizara el merge
    choropleth = folium.Choropleth(geo_data = alcaldia, data = delito_d, key_on = 'feature.properties.municipio', columns = ['municipio', 'count'], fill_color='YlGn', legend_name="Numero de crimenes de %s"%(d)).add_to(m)

    folium.LayerControl().add_to(m)

    # Display Region Label
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['count'], labels=False)
    )
    
    folium_static(m)
    
    texto = Path('visualizacion.md').read_text()
    st.markdown(texto, unsafe_allow_html=True)
    
elif seccion == 'Conclusión':
    st.write('prueba')
