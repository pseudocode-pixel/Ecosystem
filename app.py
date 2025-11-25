import streamlit as st
from datetime import date, timedelta
from modules.fetch import fetch_stock

st.set_page_config(page_title = "AI driven Investments", layout="wide",)
st.title("AI powered Investments")
st.write("This is our first minimal APP")

symbol="RELIANCE.NS"
end = date.today()
start = end - timedelta(days=365)

df = fetch_stock(symbol,start,end)
st.header(f"showing data for:{symbol}")
st.dataframe(df.tail(10))
