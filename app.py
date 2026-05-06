
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Lulu Hypermarket Dashboard", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('lulu_hypermart_dubai_sales.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'lulu_sales_data.csv' is in the repository.")
    st.stop()

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/d/d8/LuLu_Group_International_Logo.svg/1200px-LuLu_Group_International_Logo.svg.png", width=150)
st.sidebar.title("Dashboard Filters")
branch_filter = st.sidebar.multiselect("Select Branch", options=df['Branch'].unique(), default=df['Branch'].unique())
segment_filter = st.sidebar.multiselect("Customer Segment", options=df['Customer_Segment'].unique(), default=df['Customer_Segment'].unique())

df_filtered = df[df['Branch'].isin(branch_filter) & df['Customer_Segment'].isin(segment_filter)]

# Main Dashboard
st.title("🛒 Lulu Hypermarket Sales Analytics")
st.markdown("Real-time performance metrics for Dubai branches.")

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total Sales (AED)", f"{df_filtered['Total_Sales_AED'].sum():,.2f}")
with kpi2:
    st.metric("Avg Transaction Value", f"{df_filtered['Total_Sales_AED'].mean():,.2f}")
with kpi3:
    st.metric("Total Orders", len(df_filtered))

st.divider()

# Charts
c1, c2 = st.columns(2)

with c1:
    fig_cat = px.bar(df_filtered.groupby('Category')['Total_Sales_AED'].sum().reset_index(), 
                     x='Category', y='Total_Sales_AED', title="Sales by Product Category",
                     color_discrete_sequence=['#2E8B57'])
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    fig_pay = px.pie(df_filtered, values='Total_Sales_AED', names='Payment_Method', 
                     title="Market Share by Payment Method", hole=0.4)
    st.plotly_chart(fig_pay, use_container_width=True)

# Time Series
st.subheader("Sales Trend (2024)")
fig_trend = px.line(df_filtered.groupby('Date')['Total_Sales_AED'].sum().reset_index(), 
                    x='Date', y='Total_Sales_AED', template="plotly_white")
st.plotly_chart(fig_trend, use_container_width=True)

# Data Table
with st.expander("View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)
