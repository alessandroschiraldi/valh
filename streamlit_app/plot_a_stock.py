import sys
from pathlib import Path

# add project root to Python path so local modules can be imported
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import ipywidgets as widgets
from IPython.display import display
from mkt_data import stock_analyzer as sa
from mkt_data import ticker_download as td

# set base directory
base_dir = project_root

# web page
st.title("Stock Analyser")

# get the list of stocks from the file
stocks = td.get_tickers(file_name= base_dir / "mkt_data" / 'list_of_tickers.txt', call_API = False)
stocks_name = stocks['name'].tolist()

# create a selectbox for the user to choose a stock
st.selectbox("Choose a stock", options=stocks_name, key="selected_stock")

# get the stock
stock = sa.Stock(stocks.loc[stocks['name'] == st.session_state.selected_stock, 'ticker'].values[0])

# select the time period for the historical data and main stats
st.selectbox("Time period", options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], key="selected_period")

# get historical data and main stats
histdata = stock.historical_prices(period=st.session_state.selected_period, interval="1d")
stats = stock.main_statistics(period=st.session_state.selected_period, interval="1d")

# plot historical data
st.line_chart(histdata['Close'])

# plot main statistics
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Alpha", value=round(stats[0], 4))

with col2:
    st.metric(label="Yearly Volatility", value=round(stats[1], 4))




