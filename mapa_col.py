# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 17:03:32 2025

@author: luish
"""

! pip install streamlit
! pip install pandas
! pip install folium
! pip install streamlit-folium

import streamlit as st
import pandas as pd
import folium
import os

from folium.plugins import MiniMap
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from folium.plugins import HeatMap
from folium.plugins import DualMap

from streamlit_folium import st_folium
#from pyngrok import ngrok

#os.chdir("C:/Users/luish/OneDrive/Documentos/Datos")
url_1 = "https://raw.githubusercontent.com/LuisHRiosC18/Colonias_jeje/refs/heads/main/sin_pago.csv"
url_2= "https://raw.githubusercontent.com/LuisHRiosC18/Colonias_jeje/refs/heads/main/con_pago_unico.csv"

no_pagan = pd.read_csv(url_1)
no_pagan['paga'] = False  # Columna que indica que no pagan

# Cargar datos de personas que sí pagan
si_pagan = pd.read_csv(url_2)
si_pagan['paga'] = True  # Columna que indica que sí pagan

# Unir los dos DataFrames
todos = pd.concat([no_pagan, si_pagan])

# Agrupar por colonia y calcular la proporción de personas que pagan
pagos_por_colonia = todos.groupby('colonia_cobro').agg(
    total=('paga', 'count'),
    pagan=('paga', lambda x: x.sum()),  # Suma True (1) y False (0)
    latitud = ('latitud', 'mean'),
    longitud = ('longitud','mean')
).reset_index()

pagos_por_colonia['proporcion'] = pagos_por_colonia['pagan'] / pagos_por_colonia['total']

#Creamos el mapa

mexicali_coords = [32.6278, -115.4572]

# Crear el mapa
mapa_colonias = folium.Map(location=mexicali_coords, zoom_start=12)

# Agregar marcadores o círculos para cada colonia
for index, row in pagos_por_colonia.iterrows():
    proporcion = row['proporcion']
    color = 'green' if proporcion > 0.5 else 'red'  # Verde si pagan más del 50%, rojo si no
    radius = 5 + (proporcion * 20)  # Radio basado en la proporción

    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Colonia: {row['colonia_cobro']}<br>Proporción de pagos: {proporcion:.2f}"
    ).add_to(mapa_colonias)

# Mostrar el mapa
st_folium(mapa_colonias,width=700,height=500)
