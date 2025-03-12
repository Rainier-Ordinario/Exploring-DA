# Title: Python Interactive Dashboard of Superstore Sales
# Author: Rainier Ordinario
# Description: Exploring Data Analysis!

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
st.title(" :bar_chart: Superstore EDA ")
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

# Time Series Analysis
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

# Create linechart for time series
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y = "Sales", labels = {"Sales": "Amount"}, height = 500, width = 1000,template="gridon")

st.plotly_chart(fig2,use_container_width=True)

# Allow user to download time series data
with st.expander("View Data of Time Series:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime = 'text/csv')

# Create a tree map based on Region, Category, and Sub-Category
st.subheader("Hierarchical View of Sales using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                  color = "Sub-Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

'''
Segment
'''

# Create a pie chart for segment wise sales
chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

# Create a pie chart for category wise sales
with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

# Create summary table
import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, user_container_width=True)

    # Include a month wise sub-category table as a markdown in summary table
    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create scatter plot 
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1.update_layout(title="Relationship between Sales and Profit using Scatter Plot.")
                    #    titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                    #    yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

# Allow user to view data
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Allow user to download the original DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")

'''
Customer Surveys
'''

# Title for customer survey section
st.title("Customer Feedback Survey")

# Allow user to input
name = st.text_input("Your Name:")
email = st.text_input("Your Email:")
rating = st.slider("Rate our service (1 to 5)", 1, 5)
feedback = st.text_area("Additional Comments:")

# Button to submit the survey
if st.button("Submit Feedback"):
    # Store the data locally (in a CSV file)
    survey_data = pd.DataFrame({
        "Name": [name],
        "Email": [email],
        "Rating": [rating],
        "Feedback": [feedback]
    })
    
    # Save responses to CSV (appends if file exists)
    survey_data.to_csv("customer_feedback.csv", mode='a', header=False, index=False)
    
    # Display confirmation
    st.success("Thank you for your feedback!")

    # Optionally, display the collected data (for demonstration purposes)
    st.write(f"Name: {name}")
    st.write(f"Email: {email}")
    st.write(f"Rating: {rating}")
    st.write(f"Feedback: {feedback}")


