# Title: Basic EDA
# Author: Rainier Ordinario
# Description: Some Football Exploratory Data Analysis

import streamlit as st
import plotly.express as px
import pandas as pd
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
    df = pd.read_csv("wages_cleaned.csv", encoding = "ISO-8859-1")

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

# Filter the Data based on seleted date range
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()
