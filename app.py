import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configure Streamlit page
st.set_page_config(page_title="Flight Analysis Dashboard", layout="wide")
sns.set(style="whitegrid")

# =====================
# Load Dataset
# =====================
df = pd.read_csv("Flight_delay_final.csv")  # update path

# Ensure numeric columns
delay_cols = ['ArrDelay','DepDelay','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']
for col in delay_cols + ['Cancelled']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# =====================
# Sidebar Filters
# =====================
st.sidebar.header("Filters")
airline_filter = st.sidebar.multiselect("Select Airlines", options=df['Airline'].unique(), default=df['Airline'].unique())
route_filter = st.sidebar.multiselect("Select Routes", options=df['Route'].unique(), default=df['Route'].unique())
month_filter = st.sidebar.multiselect("Select Months", options=df['Month'].unique(), default=df['Month'].unique())
df = df[df['Airline'].isin(airline_filter) & df['Route'].isin(route_filter) & df['Month'].isin(month_filter)]

# =====================
# Dashboard Title
# =====================
st.title("✈ Flight Analysis Dashboard")
st.markdown("Interactive dashboard for **Week 7 & 8 Flight Delay and Cancellation Analysis**")

# =====================
# ROUTE ANALYSIS
# =====================
st.subheader("Top Routes Analysis")

# Top 10 Routes by Average ArrDelay
top_routes_delay = df.groupby('Route')['ArrDelay'].mean().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_routes_delay.values, y=top_routes_delay.index, palette="magma", ax=ax1)
ax1.set_xlabel("Average Arrival Delay (min)")
ax1.set_ylabel("Route")
ax1.set_title("Routes with Highest Average Arrival Delay")
st.pyplot(fig1)

# Top 10 Routes by Number of Flights
top_routes_count = df['Route'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_routes_count.values, y=top_routes_count.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Number of Flights")
ax2.set_ylabel("Route")
ax2.set_title("Busiest Flight Routes")
st.pyplot(fig2)

# =====================
# AIRLINE ANALYSIS
# =====================
st.subheader("Airline Analysis")

# Average Delay by Airline
avg_delay_airline = df.groupby('Airline')['ArrDelay'].mean().sort_values(ascending=False)
fig3, ax3 = plt.subplots()
sns.barplot(x=avg_delay_airline.index, y=avg_delay_airline.values, palette="coolwarm", ax=ax3)
ax3.set_ylabel("Average Arrival Delay (min)")
ax3.set_xlabel("Airline")
ax3.set_title("Average Arrival Delay by Airline")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Flights Count by Airline
flights_count_airline = df['Airline'].value_counts()
fig4, ax4 = plt.subplots()
sns.barplot(x=flights_count_airline.index, y=flights_count_airline.values, palette="Blues", ax=ax4)
ax4.set_ylabel("Number of Flights")
ax4.set_xlabel("Airline")
ax4.set_title("Number of Flights by Airline")
plt.xticks(rotation=45)
st.pyplot(fig4)

# =====================
# AIRPORT ANALYSIS
# =====================
st.subheader("Airport Analysis")

# Top 10 Airports by Avg Arrival Delay
top_airports_delay = df.groupby('Origin')['ArrDelay'].mean().sort_values(ascending=False).head(10)
fig5, ax5 = plt.subplots()
sns.barplot(x=top_airports_delay.values, y=top_airports_delay.index, palette="Reds", ax=ax5)
ax5.set_xlabel("Average Arrival Delay")
ax5.set_ylabel("Origin Airport")
ax5.set_title("Airports with Highest Average Arrival Delay")
st.pyplot(fig5)

# Top 10 Busiest Airports
top_airports_count = df['Origin'].value_counts().head(10)
fig6, ax6 = plt.subplots()
sns.barplot(x=top_airports_count.values, y=top_airports_count.index, palette="Greens", ax=ax6)
ax6.set_xlabel("Number of Flights")
ax6.set_ylabel("Origin Airport")
ax6.set_title("Top 10 Busiest Airports")
st.pyplot(fig6)

# =====================
# CANCELLATION ANALYSIS
# =====================
st.subheader("Cancellation Analysis")

# Monthly Cancellation Trend
monthly_cancel = df.groupby('Month')['Cancelled'].sum()
fig7, ax7 = plt.subplots()
sns.lineplot(x=monthly_cancel.index, y=monthly_cancel.values, marker='o', ax=ax7)
ax7.set_xlabel("Month")
ax7.set_ylabel("Number of Cancellations")
ax7.set_title("Monthly Cancellation Trend")
st.pyplot(fig7)

# Cancellation Reasons Pie Chart
cancel_reason_counts = df[df['Cancelled']==1]['CancellationCode'].value_counts()
fig8, ax8 = plt.subplots()
ax8.pie(cancel_reason_counts, labels=cancel_reason_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax8.set_title("Cancellation Reasons Distribution")
st.pyplot(fig8)

# =====================
# You can add more visuals similarly
# =====================
st.info("You can add more charts for Seasonal Analysis, Hourly Delay, Route Heatmap, Holiday Analysis, etc.")

st.markdown("### Dashboard Complete ✅")
