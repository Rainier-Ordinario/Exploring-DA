# Title: Basic EDA
# Author: Rainier Ordinario
# Description: Some Football Exploratory Data Analysis

import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib as plt
import os
import warnings
warnings.filterwarnings('ignore')

# Set layout for page
st.set_page_config(page_title="Title!!!", page_icon=":bar_chart:",layout="wide")

# Set title and format
st.title(" :bar_chart: Sample EDA ")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

# Allow users to upload file
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else: 
    os.chdir(r"/Users/rainier/Documents/Projects/DataAnalysis")
    df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")

# Allow users to select a date
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Get the minimum and maximum date
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filterdata based on seleted date range
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Filter data based on region
st.sidebar.header("Choose your filter: ")
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())

# Allow user to not select any region
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Filter data based on state
state = st.sidebar.multiselect("Pick your State", df2["State"].unique())

# Allow user to not select any state
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# Filter data based on city
city = st.sidebar.multiselect("Pick your City", df3["City"].unique())

# Allow user to not select any city
if not city:
    df2 = df.copy()
else:
    df2 = df[df["City"].isin(city)]

# Filter the data based on Region, State, and City (go through each combination)

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Subheader 
category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

# Bar chart for category wise sales
with col1:
    st.subheader("Category Sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    
    # Fit to screen size
    st.plotly_chart(fig,user_container_width=True, height = 200)

# Pie chart for region sales
with col2:
    st.subheader("Region Sales")
    fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.3)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

# Allow user to Category Data
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_VewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

# Allow user to download Region Data
with cl2:
    with st.expander("Region_VewData"):
        region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

