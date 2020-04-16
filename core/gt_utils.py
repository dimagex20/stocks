import os
import sys
import datetime
import json
import random
import requests
import pandas as pd
from pandas.tseries.offsets import BDay

import pprint
import pytz



################################
### PANDAS FUNCTIONS
################################
def df_to_csv(df, fpath, fname):
    df.to_csv(os.path.join(fpath, fname), sep=',')

def csv_to_df(fpath, fname):
    return pd.read_csv(os.path.join(fpath, fname))



################################
### DF FUNCTIONS
################################
def clean_dict_db(d, ticker):
    d['t_ticker'] = ticker.split('.')[0]
    d['t_open'] = d['1. open']
    d['t_high'] = d['2. high']
    d['t_low'] = d['3. low']
    d['t_close'] = d['4. close']
    d['t_volume'] = d['5. volume']
    d['t_date'] = datetime.datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S')

    del d['1. open']
    del d['2. high']
    del d['3. low']
    del d['4. close']
    del d['5. volume']
    del d['date']
    del d['Unnamed: 0']
    
    return d









