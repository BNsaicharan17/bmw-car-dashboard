import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BMW Car Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('bmw (1).csv')
    df['model'] = df['model'].str.strip()
    return df

df = load_data()

# Title
st.title("🚗 BMW Car Market Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📊 Filters")
selected_models = st.sidebar.multiselect(
    "Select Car Models",
    options=sorted(df['model'].unique()),
    default=sorted(df['model'].unique())
)

selected_fuel = st.sidebar.multiselect(
    "Select Fuel Types",
    options=sorted(df['fuelType'].unique()),
    default=sorted(df['fuelType'].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['year'].min()),
    max_value=int(df['year'].max()),
    value=(int(df['year'].min()), int(df['year'].max()))
)

# Filter data
filtered_df = df[
    (df['model'].isin(selected_models)) &
    (df['fuelType'].isin(selected_fuel)) &
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1])
]

# KPI metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Cars", len(filtered_df), delta=f"out of {len(df)}")

with col2:
    avg_price = filtered_df['price'].mean()
    st.metric("Avg Price", f"£{avg_price:,.0f}")

with col3:
    avg_mileage = filtered_df['mileage'].mean()
    st.metric("Avg Mileage", f"{avg_mileage:,.0f} miles")

with col4:
    avg_mpg = filtered_df['mpg'].mean()
    st.metric("Avg MPG", f"{avg_mpg:.1f}")

with col5:
    avg_engine = filtered_df['engineSize'].mean()
    st.metric("Avg Engine", f"{avg_engine:.1f}L")

st.markdown("---")

# Main dashboard content
col1, col2 = st.columns(2)

# Price distribution by model
with col1:
    st.subheader("Price Distribution by Model")
    fig_price = px.box(
        filtered_df,
        x='model',
        y='price',
        color='model',
        title="",
        labels={'price': 'Price (£)', 'model': 'Car Model'}
    )
    fig_price.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_price, use_container_width=True)

# Transmission distribution
with col2:
    st.subheader("Distribution by Transmission")
    transmission_counts = filtered_df['transmission'].value_counts()
    fig_transmission = px.pie(
        values=transmission_counts.values,
        names=transmission_counts.index,
        title="",
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    fig_transmission.update_layout(height=400)
    st.plotly_chart(fig_transmission, use_container_width=True)

# Price vs Mileage
st.subheader("Price vs Mileage Analysis")
col1, col2 = st.columns(2)

with col1:
    fig_scatter = px.scatter(
        filtered_df,
        x='mileage',
        y='price',
        color='fuelType',
        size='engineSize',
        hover_data=['model', 'year', 'transmission'],
        title="",
        labels={'mileage': 'Mileage (miles)', 'price': 'Price (£)'}
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_mpg = px.scatter(
        filtered_df,
        x='mpg',
        y='price',
        color='model',
        size='engineSize',
        hover_data=['year', 'transmission'],
        title="",
        labels={'mpg': 'MPG', 'price': 'Price (£)'}
    )
    fig_mpg.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_mpg, use_container_width=True)

# Price by year and fuel type
st.subheader("Average Price Trends")
col1, col2 = st.columns(2)

with col1:
    price_by_year = filtered_df.groupby('year')['price'].agg(['mean', 'count']).reset_index()
    fig_year = px.line(
        price_by_year,
        x='year',
        y='mean',
        markers=True,
        title="",
        labels={'mean': 'Average Price (£)', 'year': 'Year'}
    )
    fig_year.update_layout(height=400)
    st.plotly_chart(fig_year, use_container_width=True)

with col2:
    price_by_fuel = filtered_df.groupby('fuelType')['price'].mean().sort_values(ascending=False)
    fig_fuel = px.bar(
        x=price_by_fuel.index,
        y=price_by_fuel.values,
        labels={'x': 'Fuel Type', 'y': 'Average Price (£)'},
        title="",
        color=price_by_fuel.values,
        color_continuous_scale='Viridis'
    )
    fig_fuel.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_fuel, use_container_width=True)

# Engine size analysis
st.subheader("Engine Size & Tax Analysis")
col1, col2 = st.columns(2)

with col1:
    fig_engine = px.box(
        filtered_df,
        x='fuelType',
        y='engineSize',
        color='transmission',
        title="",
        labels={'engineSize': 'Engine Size (L)', 'fuelType': 'Fuel Type'}
    )
    fig_engine.update_layout(height=400)
    st.plotly_chart(fig_engine, use_container_width=True)

with col2:
    fig_tax = px.scatter(
        filtered_df,
        x='tax',
        y='price',
        color='year',
        size='engineSize',
        hover_data=['model', 'fuelType'],
        title="",
        labels={'tax': 'Tax (£)', 'price': 'Price (£)', 'year': 'Year'}
    )
    fig_tax.update_layout(height=400)
    st.plotly_chart(fig_tax, use_container_width=True)

# Data table
st.subheader("📋 Detailed Data")
if st.checkbox("Show raw data", value=False):
    st.dataframe(filtered_df, use_container_width=True)

# Summary statistics
if st.checkbox("Show summary statistics", value=False):
    st.subheader("Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)
