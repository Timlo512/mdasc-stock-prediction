import yahoo_info.stock_info as si
import talib

import pandas as pd
import numpy as np

class Data(object):

    def __inif__(self):
        self.tickers = si.tickers_nasdaq()

    def get_nasdaq_tickers(self):
        return self.tickers

    # Get Stock Price

    # Get TA Indicators
