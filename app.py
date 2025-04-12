import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
car_data = pd.read_csv('vehicles_us.csv')
car_data['manufacturer'] = car_data['model'].str.split().str[0].str.lower()

st.header("🚗 Used Car Data Exploration")

# 1. Data viewer: Include manufacturers with less than 1000 ads
st.subheader("🔍 Manufacturers with Less Than 1000 Listings")
manufacturer_counts = car_data['manufacturer'].value_counts()
rare_makers = manufacturer_counts[manufacturer_counts < 1000].index
filtered_data = car_data[car_data['manufacturer'].isin(rare_makers)]
st.dataframe(filtered_data[['manufacturer', 'model', 'price', 'condition', 'type']])

# 2. Vehicle types by manufacturer
st.subheader("🚙 Vehicle Types by Manufacturer")
type_counts = car_data.groupby('manufacturer')['type'].count().reset_index()
fig_type_count = px.bar(type_counts, x='manufacturer', y='type',
                        labels={'type': 'Vehicle Count'},
                        title='Vehicle Count by Manufacturer')
st.plotly_chart(fig_type_count, use_container_width=True)

# 3. Histogram of condition vs model_year
st.subheader("📅 Histogram: Condition vs. Model Year")
valid_condition = car_data.dropna(subset=['model_year', 'condition'])
fig_cond_year = px.histogram(valid_condition, x='model_year', color='condition',
                             barmode='group',
                             title='Vehicle Condition by Model Year',
                             labels={'model_year': 'Model Year', 'condition': 'Condition'})
st.plotly_chart(fig_cond_year, use_container_width=True)

# 4. Compare price between manufacturers
st.subheader("💰 Compare Prices Between Manufacturers")

# Dropdowns
makers = sorted(car_data['manufacturer'].dropna().unique())
maker1 = st.selectbox("Select Manufacturer 1", makers, index=0)
maker2 = st.selectbox("Select Manufacturer 2", makers, index=1)

# Optional normalization
normalize = st.checkbox("Normalize Histogram (Percentage)")

# Filter data by manufacturer and valid prices
data_compare = car_data[car_data['manufacturer'].isin([maker1, maker2])]
data_compare = data_compare[data_compare['price'] > 0]

# Comparative histogram
fig_price = px.histogram(data_compare, x='price', color='manufacturer',
                         nbins=50,
                         histnorm='percent' if normalize else None,
                         title=f"Price Comparison: {maker1} vs {maker2}",
                         labels={'price': 'Price', 'manufacturer': 'Manufacturer'})
st.plotly_chart(fig_price, use_container_width=True)
