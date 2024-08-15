import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
symbol = st.sidebar.text_input("Enter a stock symbol", value="AAPL")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")
data = yf.download(symbol, start=start_date, end=end_date)
# Calculate technical indicators (e.g., moving average)
data['MA9'] = data['Close'].rolling(window=9).mean()
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()
plt.figure(figsize=(10,4))
plt.title(symbol)
plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA9'], label='Moving Average 9')
plt.plot(data['MA20'], label='Moving Average 20')
plt.plot(data['MA50'], label='Moving Average 50')
plt.legend(loc='upper left')
st.pyplot(plt)
