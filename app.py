import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv('train.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    return df

df = load_data()

st.title("⏰ Hourly Bike Rental Trends")
st.markdown("**Washington D.C. hourly analysis (2011-2012)**")

# 3 Widgets (different)
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", df['year'].unique())
dayofweek = st.sidebar.selectbox("Day of Week", 
    ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
hour_min, hour_max = st.sidebar.slider("Hour Range", 0, 23, (0, 23))

# Filter
filtered = df[(df['year']==year) & 
              (df['hour'].between(hour_min, hour_max))]

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", filtered['count'].sum())
col2.metric("Peak Hour", filtered['hour'].map(filtered.groupby('hour')['count'].mean()).max())
col3.metric("Records", len(filtered))

# PLOT 1: Hourly Heatmap (UNIQUE)
hourly_avg = filtered.groupby(['hour', 'dayofweek'])['count'].mean().reset_index()
fig1 = px.density_heatmap(hourly_avg, x='hour', y='dayofweek', 
                         z='count', title="Hourly Heatmap by Day",
                         color_continuous_scale='Viridis')
st.plotly_chart(fig1, use_container_width=True)

# PLOT 2: Day-of-week bar
day_avg = filtered.groupby('dayofweek')['count'].mean().reset_index()
day_avg['day_name'] = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
fig2 = px.bar(day_avg, x='day_name', y='count', 
              title="Average Rentals by Day", color='count')
st.plotly_chart(fig2)

# PLOT 3: Hourly line
hourly = filtered.groupby('hour')['count'].mean().reset_index()
fig3 = px.line(hourly, x='hour', y='count', 
               title="Hourly Rental Patterns")
st.plotly_chart(fig3)

# PLOT 4: Casual vs Registered pie (NEW)
casual_reg = filtered[['casual','registered']].sum()
fig4 = px.pie(values=casual_reg.values, names=['Casual','Registered'],
              title="User Type Split")
st.plotly_chart(fig4)

# PLOT 5: Month violin
monthly = filtered.groupby('month')['count'].mean().reset_index()
fig5 = px.violin(filtered, x='month', y='count', 
                 title="Monthly Distribution")
st.plotly_chart(fig5)

st.success("**5 plots + 3 widgets** - Hourly rental insights!")
