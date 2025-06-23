import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date, timedelta

def fetch_tickers():
    listed = sorted(pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].to_list())
    tickers = [{'label':ticker, 'value':ticker} for ticker in listed]

    return tickers

def load_data(ticker: str, period: str):
    start = (date.today() - timedelta(days=int(period))).strftime("%Y-%m-%d")
    data = yf.download(tickers=ticker, start=start)
    data = data.reset_index()
    data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    data = data.rename(columns={'Date':'date', 'Open':'open', 'High':'high',
                                'Low':'low', 'Close':'close', 'Volume':'volume'})

    return data