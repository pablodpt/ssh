import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Definir el símbolo de la acción (este es un ejemplo, puedes cambiarlo por el que desees)


# Definir el rango de fechas (desde hace un año hasta hoy)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

symbol = st.sidebar.text_input("Enter a stock symbol", value="AAPL")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")





# Obtener los datos de la acción
df = yf.download(symbol, start=start_date, end=end_date)
# Calcular las medias móviles y el promedio móvil exponencial
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()
df['EMA_9'] = df['Close'].ewm(span=9).mean()

# Calcular las bandas de Bollinger
df['middle_band'] = df['Close'].rolling(window=20).mean()
df['upper_band'] = df['middle_band'] + 1.96*df['Close'].rolling(window=20).std()
df['lower_band'] = df['middle_band'] - 1.96*df['Close'].rolling(window=20).std()

# Calcular el RSI
delta = df['Close'].diff()
up = delta.clip(lower=0)
down = -1*delta.clip(upper=0)
ema_up = up.ewm(com=13, adjust=False).mean()
ema_down = down.ewm(com=13, adjust=False).mean()
rs = ema_up/ema_down
df['RSI'] = 100 - (100/(1 + rs))
# Crear el gráfico
fig, ax1 = plt.subplots(figsize=(12, 6))



# Crear el gráfico de las medias móviles

ax1.plot(df['Close'], label='Close Price')
ax1.plot(df['SMA_20'], label='20 Day SMA')
ax1.plot(df['SMA_50'], label='50 Day SMA')
ax1.plot(df['SMA_200'], label='200 Day SMA')
ax1.plot(df['EMA_9'], label='9 Day EMA')

plt.legend(loc='upper left')
plt.title('Moving Averages')
# Gráfico del volumen (barras)
ax2 = ax1.twinx()
ax2.bar(df.index, df['Volume'], color='gray', alpha=0.5, label='Volumen')
ax2.set_ylabel('Volumen', color='gray')
ax2.tick_params('y', colors='gray')
# Mostrar el gráfico
st.pyplot(plt)

# Calcular RSI con Pandas Ta

# Crear el gráfico de las bandas de Bollinger
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(df['Close'], label='Close Price')
ax1.plot(df['middle_band'], label='Middle Band')
ax1.plot(df['upper_band'], label='Upper Band')
ax1.plot(df['lower_band'], label='Lower Band')
plt.legend(loc='upper left')
plt.title('Bollinger Bands')
st.pyplot(plt)
#Grafico RSI
plt.figure()
fig, ax1 = plt.subplots()
ax1.set_title("rsi")
fig.subplots_adjust(bottom=0.2)
ax1.plot(df["RSI"])
ax1.set_ylim(0, 100)
ax1.axhline(y=70, color='r', linestyle='-')
ax1.axhline(y=30, color='r', linestyle='-')
ax1.grid(True)
ax1.set_ylabel(r'RSI')
for label in ax1.get_xticklabels(which='major'):
  label.set(rotation=30, horizontalalignment='right')
st.pyplot(plt)
