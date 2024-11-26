import streamlit as st
import pandas as pd

# Título de la página
st.markdown("# Mi bici 2024")

# Cargar datos resumidos
trips_per_day = pd.read_csv('./datos/trips_per_day.csv')
trips_per_hour = pd.read_csv('./datos/trips_per_hour.csv')
trips_per_weekday = pd.read_csv('./datos/trips_per_weekday.csv')

# Mostrar gráficas
st.write("Viajes por día")
st.line_chart(trips_per_day.set_index('inicio_del_viaje')['num_trips'])

st.write("Viajes por hora del día")
st.bar_chart(trips_per_hour.set_index('hora_del_dia')['num_trips'])

st.write("Viajes por día de la semana")
st.bar_chart(trips_per_weekday.set_index('dia_de_la_semana')['num_trips'])