from unittest.mock import call
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import argparse
import os
import logging
import sys
import json
import requests
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import warnings
warnings.filterwarnings("ignore")
import joblib

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.model = None
        self.stock = yf.Ticker(self.ticker)
        
    def historical_prices(self, period='1y', interval='1d'):
        logging.info(f"Fetching data for {self.ticker}")
        df = self.stock.history(period=period, interval=interval)
        if df.empty:
            logging.error(f"No data found for ticker {self.ticker}")
            sys.exit(1)
        return df
    
    def balance_sheet(self):
        logging.info(f"Fetching financials for {self.ticker}")
        df = self.stock.get_balance_sheet()
        return df
    
    def plot_prices(self, df):
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['Close'], label='Close Price')
        plt.title(f"{self.ticker} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()


