from unittest.mock import call
from pyparsing import alphas
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
import scipy.stats as ss


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
    
    def main_statistics(self, period='1y', interval='1d'):
        historical_prices = self.historical_prices(period,interval)
        returns = historical_prices['Close'].pct_change().dropna()
        alpha = ( historical_prices['Close'][-1] - historical_prices['Close'][0] ) / historical_prices['Close'][0]
        volatility = returns.std()
        match interval:
            case '1d':
                volatility *= np.sqrt(252)
            case '1w':
                volatility *= np.sqrt(52)
            case '1m':
                volatility *= np.sqrt(12)
        return alpha,volatility
    
    def alpha(self, period='1y', interval='1d'):
        alpha,volatility = self.main_statistics()
        return alpha
    
    def volatility(self, period='1y', interval='1d'):
        alpha,volatility = self.main_statistics()
        return volatility
    
    def correl(self, stock, period='1y', interval='1d', hp_self = None):
        if hp_self is None:
            logging.info(f"Fetching info for {self.ticker}")
            hp_self = self.historical_prices(period, interval)        
        logging.info(f"Fetching info for {stock.ticker}")
        hp_stock = stock.historical_prices(period, interval)
        hp_merged = pd.concat([hp_self["Close"].rename("Close_self"),
                               hp_stock["Close"].rename("Close_stock")],
                               axis=1).dropna()
        returns_self = hp_merged["Close_self"].pct_change().dropna()
        returns_stock = hp_merged["Close_stock"].pct_change().dropna()
        return ss.pearsonr(returns_self , returns_stock)[0]


    def plot_prices(self, period='1y', interval='1d'):
        historical_prices = self.historical_prices(period=period, interval=interval)
        plt.figure(figsize=(14, 7))
        plt.plot(historical_prices.index, historical_prices['Close'], label='Close Price')
        plt.title(f"{self.ticker} Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

class Portfolio:
    def __init__(self, stocks, weights = None):
        self.stocks = stocks
        self.weights = weights if weights else [1] * len(stocks)
        
    def add_stock(self, stock, weight = 1):
        self.stocks.append(stock)
        self.weights.append(weight)
        
    def main_statistics(self, period='1y', interval='1d'):
        alphas, volatilities = [], []
        for stock in self.stocks:
            alphas = [alphas, stock.alpha(period=period, interval=interval) ]
            volatilities = [volatilities, stock.volatility(period=period, interval=interval)]
        return alphas, volatilities
    
    def alphas(self, period='1y', interval='1d'):
        alphas, volatilities = self.main_statistics(period=period, interval=interval)
        return alphas
    
    def volatilities(self, period='1y', interval='1d'):
        alphas, volatilities = self.main_statistics(period=period, interval=interval)
        return volatilities
    
    def correlation_matrix(self, period='1y', interval='1d'):
        n = len(self.stocks)
        corr = np.ones([n,n])
        for i in range(n):
            hp_self = self.stocks[i].historical_prices(period, interval)  
            for j in range(i+1, n):
                corr[i,j] = self.stocks[i].correl(self.stocks[j], period, interval, hp_self = hp_self)
                corr[j,i] = corr[i,j]
        return corr
             



    def plot_prices(self, period='1y', interval='1d'):
        plt.figure(figsize=(14, 7))
        for stock in self.stocks:
            historical_prices = stock.historical_prices(period=period, interval=interval)
            plt.plot(historical_prices.index, historical_prices['Close'], label=stock.ticker)
        plt.title("Portfolio Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
