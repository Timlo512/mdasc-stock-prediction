import yahoo_fin.stock_info as si
import talib
import concurrent.futures

import pandas as pd
import numpy as np

from datetime import datetime, date, timedelta
import time

class Data(object):

    def __init__(self):
        self.tickers = si.tickers_nasdaq()
        self.si = si
        self.ta = talib

    def get_nasdaq_tickers(self):
        return self.tickers

    # Get data for all tickers
    def get_all_ticker_data(self, fn, args, method = 'async', max_workers = 5, timeout = 60):

        df = pd.DataFrame()

        if method == 'async':
            
            print('Scrape stock price data async')
            with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor:
                
                future_to_data = {executor.submit(fn, **{'ticker': ticker, **args}): ticker for ticker in self.tickers}
                for future in concurrent.futures.as_completed(future_to_data):
                    ticker = future_to_data[future]
                    try:
                        data = future.result(timeout = timeout)
                    except Exception as e:
                        print(f'{ticker} generated an exception: {e}')
                    else:
                        if isinstance(data, pd.DataFrame):
                            print(f'{ticker} has {len(data)} records')
                            df = df.append(data)
                        elif isinstance(data, dict):
                            data = pd.Series(data)
                            df = df.append(data, ignore_index = True)
        
        elif method == 'loop':

            print('Scrape stock price data in series')
            for ticker in self.tickers:
                
                data = fn(**{'ticker': ticker, **args})
                if isinstance(data, pd.DataFrame):
                    print(f'{ticker} has {len(data)} records')
                    df = df.append(data)
                elif isinstance(data, dict):
                    data = pd.Series(data)
                    df = df.append(data, ignore_index = True)

        return df

    def get_ohlc_data(self, **kwargs):

        time_sleep = int(kwargs['time_sleep']) if 'time_sleep' in kwargs.keys() else 10
        data = si.get_data(**kwargs)
        time.sleep(np.random.choice(range(time_sleep)))

        return data
        
    # def _estimate_call_time(self, fn = si.get_data, method = 'async'):

    # Get TA Indicators
