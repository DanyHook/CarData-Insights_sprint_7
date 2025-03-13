import pandas as pd
import plotly.express as px
import streamlit as st
import os

# 📌 Verificar si el archivo CSV existe antes de cargarlo
DATA_FILE = "vehicles_us.csv"

if not os.path.exists(DATA_FILE):
    st.error(f"Error: No se encontró el archivo `{DATA_FILE}`. Asegúrate de que está en la carpeta correcta.")
    st.stop()  # Detiene la ejecución si no hay datos

# 📌 Cargar el conjunto de datos
car_data = pd.read_csv(DATA_FILE)

# 📌 Validar que las columnas esenciales existen
REQUIRED_COLUMNS = {"odometer", "price", "condition"}
if not REQUIRED_COLUMNS.issubset(car_data.columns):
    st.error(f"Error: El conjunto de datos no contiene las columnas necesarias: {REQUIRED_COLUMNS}")
    st.stop()

# 📌 Encabezado de la aplicación
st.header("🚗 CarData Insights: Exploración de Vehículos Usados")

# 📌 Filtrado interactivo de datos
st.sidebar.header("🎛 Filtros de Datos")

# Selector de rango para "odometer"
min_km, max_km = st.sidebar.slider(
    "Selecciona el rango de kilometraje:",
    int(car_data["odometer"].min()), 
    int(car_data["odometer"].max()), 
    (int(car_data["odometer"].min()), int(car_data["odometer"].max()))
)

# Selector de rango para "price"
min_price, max_price = st.sidebar.slider(
    "Selecciona el rango de precio:",
    int(car_data["price"].min()), 
    int(car_data["price"].max()), 
    (int(car_data["price"].min()), int(car_data["price"].max()))
)

# Aplicar filtros al dataset
car_data = car_data[(car_data["odometer"].between(min_km, max_km)) & 
                    (car_data["price"].between(min_price, max_price))]


# 📌 Función para crear y mostrar gráficos
def create_chart(chart_type, x, y=None, color=None, title="Gráfico"):
    """Genera y muestra un gráfico con Plotly Express en Streamlit."""
    if chart_type == "histogram":
        fig = px.histogram(car_data, x=x, title=title, color_discrete_sequence=["blue"])
    elif chart_type == "scatter":
        fig = px.scatter(car_data, x=x, y=y, color=color, title=title, color_discrete_sequence=px.colors.qualitative.Set1)
    else:
        st.error("Tipo de gráfico no soportado.")
        return
    st.plotly_chart(fig, use_container_width=True)


# 📌 Casillas de verificación para mostrar gráficos
if st.checkbox("📊 Mostrar Histograma del Odómetro"):
    create_chart("histogram", x="odometer", title="Distribución del Odómetro")

if st.checkbox("📈 Mostrar Gráfico de Dispersión (Kilometraje vs Precio)"):
    create_chart("scatter", x="odometer", y="price", color="condition", title="Relación entre Kilometraje y Precio")
