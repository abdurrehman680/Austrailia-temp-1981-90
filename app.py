import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Daily Minimum Temperatures Dashboard")

raw_csv = pd.read_csv("monthly_min_avg_temp.csv", parse_dates=["Date"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Minimum Average Temperature")
    fig, ax = plt.subplots()
    ax.plot(raw_csv["Date"], raw_csv["MinTemp"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.set_title("Monthly Minimum Average Temperature From 1981 to 1990")
    st.pyplot(fig)