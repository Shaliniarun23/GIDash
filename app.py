import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Supermarket Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("SuperMarket_Enhanced.xlsx", sheet_name="Raw data - SuperMarket", engine='openpyxl')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    df['Day'] = df['Date'].dt.day_name()
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_city = st.sidebar.multiselect("Select City", df["City"].unique(), default=df["City"].unique())
selected_gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
selected_payment = st.sidebar.multiselect("Select Payment Type", df["Payment"].unique(), default=df["Payment"].unique())

# Filtered Data
filtered_df = df[(df["City"].isin(selected_city)) & 
                 (df["Gender"].isin(selected_gender)) & 
                 (df["Payment"].isin(selected_payment))]

st.title("📊 Supermarket Business Insights Dashboard")
st.markdown("This dashboard offers deep insights into sales performance, customer behavior, and operational metrics using supermarket transaction data.")

tab1, tab2, tab3 = st.tabs(["📈 Macro KPIs", "🛒 Product Insights", "👥 Customer Insights"])

with tab1:
    st.subheader("💹 Overall Business Performance")
    st.markdown("Visuals to understand income trends, sales growth, and store-wise performance.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Income", f"${filtered_df['gross income'].sum():,.2f}")
    col2.metric("Total Transactions", len(filtered_df))
    col3.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f} ⭐")

    fig1 = px.line(filtered_df.groupby("Date")["gross income"].sum().reset_index(),
                   x="Date", y="gross income", title="Daily Gross Income")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(filtered_df, x="Branch", y="gross income", color="Branch",
                  title="Branch-wise Gross Income", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(filtered_df, x="Hour", nbins=24, title="Transaction Volume by Hour")
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("📦 Product Line & Sales")
    st.markdown("Dive into product-level performance to optimize inventory and marketing.")

    fig4 = px.box(filtered_df, x="Product line", y="gross income", color="Product line",
                  title="Income Distribution by Product Line")
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.bar(filtered_df.groupby("Product line")["Quantity"].sum().reset_index(),
                  x="Product line", y="Quantity", title="Total Quantity Sold per Product Line")
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.sunburst(filtered_df, path=["City", "Branch", "Product line"],
                       values="gross income", title="Sales Contribution by City > Branch > Product")
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.subheader("👤 Customer Demographics & Preferences")
    st.markdown("Understanding your customers helps personalize offerings and improve retention.")

    col1, col2 = st.columns(2)
    with col1:
        gender_pie = px.pie(filtered_df, names='Gender', title="Gender Split")
        st.plotly_chart(gender_pie, use_container_width=True)
    with col2:
        payment_pie = px.pie(filtered_df, names='Payment', title="Payment Method Preference")
        st.plotly_chart(payment_pie, use_container_width=True)

    fig7 = px.violin(filtered_df, y="gross income", x="Gender", color="Gender",
                     box=True, title="Income Distribution by Gender")
    st.plotly_chart(fig7, use_container_width=True)

    fig8 = px.bar(filtered_df.groupby("Customer type")["gross income"].mean().reset_index(),
                  x="Customer type", y="gross income", title="Avg Income per Customer Type")
    st.plotly_chart(fig8, use_container_width=True)

    fig9 = px.scatter(filtered_df, x="Total", y="Rating", color="Product line",
                      size="gross income", title="Total Purchase vs Rating")
    st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Data: SuperMarket Enhanced | Author: Your Name")
