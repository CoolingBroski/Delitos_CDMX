import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from pathlib import Path

seccion = st.sidebar.selectbox(
    "Sección:",
    ('Introducción', 'Visualización', 'Conclusión'))
    
if seccion == 'Introducción':
    introduccion = Path('intro.md').read_text()
    st.markdown(introduccion, unsafe_allow_html=True)
    
elif seccion == 'Visualización':
    st.header('Visualización Interactiva')
    m = folium.Map(location=[39.94, -75.15], zoom_start=16)
    tooltip="Liberty Bell"
    folium.Marker([39.9, -75.15], pupul="Liberty Bell", tooltip=tooltip).add_to(m)
    
    folium_static(m)
    
    texto = Path('visualizacion.md').read_text()
    st.markdown(texto, unsafe_allow_html=True)
    
elif seccion == 'Conclusión':
    st.write('prueba')
