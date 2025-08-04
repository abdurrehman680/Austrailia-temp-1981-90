import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
import pickle

st.set_page_config(
    page_title = "Dashboard - Temperature Predictions",
    page_icon = "🏠",
    layout="wide"
)

st.title("Minimum Temperature Predictions - Australia")

raw_csv = pd.read_csv("daily-minimum-temperatures-in-me.csv", parse_dates=["Date"])
raw_csv["Daily minimum temperatures"] = pd.to_numeric(raw_csv["Daily minimum temperatures"], errors="coerce")
raw_csv.dropna(subset=["Daily minimum temperatures"], inplace=True)
monthly_avg_temp = pd.read_csv("monthly_min_avg_temp.csv", parse_dates=["Date"])

# Summary

highest_monthly_avg = monthly_avg_temp["MinTemp"].max()
lowest_monthly_avg = monthly_avg_temp["MinTemp"].min()
total_records = len(raw_csv)

sum1, sum2, sum3, sum4, sum5 = st.columns(5)

sum1.metric(
    label = "Total Records",
    value = total_records
)
sum2.metric(
    label = "Highest Monthly Average",
    value = round(highest_monthly_avg, 2)
)
sum3.metric(
    label = "Lowest Monthly Average",
    value = round(lowest_monthly_avg, 3)
)

# Hottest and Coldest month
coldest_row = raw_csv.loc[raw_csv["Daily minimum temperatures"].idxmin()]
coldest_month = coldest_row["Date"].strftime("%B %Y")
lowest_temp = coldest_row["Daily minimum temperatures"]

hottest_row = raw_csv.loc[raw_csv["Daily minimum temperatures"].idxmax()]
hottest_month = hottest_row["Date"].strftime("%B %Y")
highest_temp = hottest_row["Daily minimum temperatures"]

sum4.metric(
    label= "Coldest Month",
    value = coldest_month,
    delta = f"{lowest_temp:.2f} °C",
    delta_color = "off"
)

sum5.metric(
    label= "Hottest Month",
    value = hottest_month,
    delta = f"{highest_temp:.2f} °C"
)

#Display raw data

if st.checkbox("Show Raw Data"):
    st.dataframe(raw_csv)

# Monthly Mean


mean_avg1, mean_avg2 = st.columns(2)

with mean_avg1:
    monthly_avg_temp

with mean_avg2:
    months = [datetime.datetime(year, month, 1)
    for year in range(1981,1990)
    for month in range(1,13)]

    date_range = st.slider(
        "",
        min_value= months[0],
        max_value= months[-1],
        value=(months[0], months[-1]),
        format="MMM, YYYY"
    )
    start = date_range[0].strftime("%Y-%m")
    end = date_range[1].strftime("%Y-%m")
    monthly_avg_temp["Date"] = monthly_avg_temp["Date"].dt.strftime("%Y-%m")
    filtered = monthly_avg_temp[(monthly_avg_temp["Date"] >= start) & (monthly_avg_temp["Date"] <= end)]

    # Graph
    fig, ax = plt.subplots(figsize=(20,8.7))
    ax.plot(filtered["Date"], filtered["MinTemp"], color="purple")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)

# Predicting

target_year = st.selectbox("Choose a year for prediciton",[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000])
start_year = 1990
period = (target_year - start_year) * 12

with open("sarimax_model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

forecast = loaded_model.get_forecast(steps=period)
forecast_values = forecast.predicted_mean
forecast_values = forecast_values[-12:]
forecast_ci = forecast.conf_int()
forecast_ci = forecast_ci[-12:]

if st.checkbox("Show CSV:"):
    st.dataframe(forecast_values)

st.bar_chart(forecast_values)

