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

# 📌 Función para crear y mostrar gráficos con filtros individuales
def create_chart(chart_type, x, y=None, color=None, title="Gráfico"):
    """Genera y muestra un gráfico con filtros específicos en Streamlit."""

    # 📌 Agregar filtros personalizados dentro de cada gráfico
    st.subheader(f"🎛 Filtros para {title}")
    
    # Filtro de kilometraje dentro del gráfico
    min_km, max_km = st.slider(
        "Selecciona el rango de kilometraje:",
        int(car_data["odometer"].min()), 
        int(car_data["odometer"].max()), 
        (int(car_data["odometer"].min()), int(car_data["odometer"].max()))
    )

    # Filtro de precio dentro del gráfico
    min_price, max_price = st.slider(
        "Selecciona el rango de precio:",
        int(car_data["price"].min()), 
        int(car_data["price"].max()), 
        (int(car_data["price"].min()), int(car_data["price"].max()))
    )

    # Aplicar filtros al dataset específico de este gráfico
    filtered_data = car_data[(car_data["odometer"].between(min_km, max_km)) & 
                             (car_data["price"].between(min_price, max_price))]

    # 📌 Generar el gráfico
    if chart_type == "histogram":
        fig = px.histogram(filtered_data, x=x, title=title, color_discrete_sequence=["blue"])
    elif chart_type == "scatter":
        fig = px.scatter(filtered_data, x=x, y=y, color=color, title=title, color_discrete_sequence=px.colors.qualitative.Set1)
    else:
        st.error("Tipo de gráfico no soportado.")
        return

    # 📌 Mostrar el gráfico en la app
    st.plotly_chart(fig, use_container_width=True)


# 📌 Casillas de verificación para mostrar gráficos con sus propios filtros
if st.checkbox("📊 Mostrar Histograma del Odómetro"):
    create_chart("histogram", x="odometer", title="Distribución del Odómetro")

if st.checkbox("📈 Mostrar Gráfico de Dispersión (Kilometraje vs Precio)"):
    create_chart("scatter", x="odometer", y="price", color="condition", title="Relación entre Kilometraje y Precio")
