import pandas as pd
import plotly.express as px
import streamlit as st

# Leer el conjunto de datos
car_data = pd.read_csv('vehicles_us.csv')

# Crear encabezado
st.header("Exploración de Datos de Vehículos Usados")

# Casilla de verificación para el histograma
show_histogram = st.checkbox("Mostrar Histograma del Odómetro")

if show_histogram:
    st.write("Creación de un histograma para el conjunto de datos de anuncios de venta de coches")

    # Crear un histograma con colores
    fig_hist = px.histogram(
        car_data, 
        x="odometer",
        title="Distribución del Odómetro en los Vehículos",
        labels={"odometer": "Kilometraje"},
        color_discrete_sequence=["blue"]  # Color personalizado
    )

    # Mostrar gráfico interactivo
    st.plotly_chart(fig_hist, use_container_width=True)

# Casilla de verificación para el gráfico de dispersión
show_scatter = st.checkbox("Mostrar Gráfico de Dispersión Kilometraje vs. Precio")

if show_scatter:
    st.write("Creación de un gráfico de dispersión para analizar la relación entre el Kilometraje y el Precio")

    # Crear gráfico de dispersión con colores según condición del vehículo
    fig_scatter = px.scatter(
        car_data, 
        x="odometer", 
        y="price", 
        color="condition",  # Colorea los puntos según la condición del auto
        title="Relación entre Kilometraje y Precio de Vehículos",
        labels={"odometer": "Kilometraje", "price": "Precio"},
        color_discrete_sequence=px.colors.qualitative.Set1  # Paleta de colores llamativa
    )

    # Mostrar gráfico interactivo
    st.plotly_chart(fig_scatter, use_container_width=True)
