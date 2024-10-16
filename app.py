import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import streamlit as st
from datetime import datetime

# Load Data
base_dir = r'C:\\Users\\javie\\Desktop\\ITESO\\05 Quinto Semestre\\Mineria de datos\\Notebook - David\\mi_bici\\datos'
data_frames = []

for year in range(2024, 2024 + 1):
    year_dir = os.path.join(base_dir, str(year))
    csv_files = glob.glob(os.path.join(year_dir, '*.csv'))
    for file in csv_files:
        df = pd.read_csv(file, encoding='latin1')
        if 'Ã±o_de_nacimiento' in df.columns:
            df.rename(columns={'Ã±o_de_nacimiento': 'Año_de_nacimiento'}, inplace=True)
        if 'AÃ±o_de_nacimiento' in df.columns:
            df.rename(columns={'AÃ±o_de_nacimiento': 'Año_de_nacimiento'}, inplace=True)
        elif 'A}äe_nacimiento' in df.columns:
            df.rename(columns={'A}äe_nacimiento': 'Año_de_nacimiento'}, inplace=True)
        elif 'Año_de_nacimiento' in df.columns:
            df.rename(columns={'Año_de_nacimiento': 'Año_de_nacimiento'}, inplace=True)
        data_frames.append(df)

dfGlobal = pd.concat(data_frames, ignore_index=True)
dfGlobal.columns = [x.lower() for x in dfGlobal.columns]

nomenclaturaDf = pd.read_csv('./datos/nomenclatura_2024_08.csv', encoding='latin1')
nomenclaturaDf.columns = [x.lower() for x in nomenclaturaDf.columns]

# Data Transformation
dfGlobal['inicio_del_viaje'] = pd.to_datetime(dfGlobal['inicio_del_viaje'])
dfGlobal['fin_del_viaje'] = pd.to_datetime(dfGlobal['fin_del_viaje'])
dfGlobal['duracion_viaje'] = (dfGlobal['fin_del_viaje'] - dfGlobal['inicio_del_viaje']).dt.total_seconds() / 60
dfGlobal['año'] = dfGlobal['inicio_del_viaje'].dt.year
dfGlobal['dia_de_la_semana'] = dfGlobal['inicio_del_viaje'].dt.day_name()
dfGlobal['hora_del_dia'] = dfGlobal['inicio_del_viaje'].dt.hour
dfGlobal['rango_duracion'] = dfGlobal['duracion_viaje'].apply(
    lambda x: 1 if x < 10 else 2 if x < 20 else 3 if x < 30 else 4 if x < 40 else 5 if x < 50 else 6 if x < 60 else 7
)
dfGlobal['edad'] = pd.to_datetime('today').year - dfGlobal['año_de_nacimiento']
dfGlobal = dfGlobal[(dfGlobal['edad'] >= 13) & (dfGlobal['edad'] <= 90)]
dfGlobal['mes'] = dfGlobal['inicio_del_viaje'].dt.month

# Streamlit Interface
st.title("PROYECTO MI BICI")
st.markdown("**Francisco Javier De la Torre Silva 745974**")

# Display Data
st.header("Datos Globales")
st.write(dfGlobal.head())

# Display Plots
st.header("Análisis Exploratorio")
fig, ax = plt.subplots()
sns.countplot(data=dfGlobal, x='dia_de_la_semana', ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots()
sns.histplot(dfGlobal['duracion_viaje'], bins=30, kde=True, ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots()
sns.boxplot(data=dfGlobal, x='mes', y='duracion_viaje', ax=ax)
st.pyplot(fig)