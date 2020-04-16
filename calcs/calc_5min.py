import os
import sys
import datetime
from time import sleep
import time
import json
import logging
import logging.config
import math

from os import listdir
from os.path import isfile, join

import pprint
from threading import Thread
import subprocess
import random
import requests


from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from pandas.tseries.offsets import BDay
import statistics

from alpha_vantage.timeseries import TimeSeries

sys.path.append(r'/home/gtserver/code/repos/stocks/')

#import sql_db as dbm
import core.gt_inputs as fdi
import core.gt_functions as mf
import core.gt_utils as ut
import core.gt_calcs as cs
#from gt_email import GTEmail


from multiprocessing import Process

mypath = "/home/gtserver/code/repos/stocks/data/raw/5min"
calc_path = "/home/gtserver/code/repos/stocks/data/calcd/5min"

def get_live_data(stocks):
    for ticker in stocks:
        try:
            df = ut.csv_to_df(mypath, ticker)

            df['sma20'] = cs.calc_smas(df, 20).round(2)
            df['sma50'] = cs.calc_smas(df, 50).round(2)
            df['sma100'] = cs.calc_smas(df, 100).round(2)
            df['sma200'] = cs.calc_smas(df, 200).round(2)

            df['ema9'] = cs.calc_emas(df, 9).round(2)
            df['ema15'] = cs.calc_emas(df, 15).round(2)
            df['ema65'] = cs.calc_emas(df, 65).round(2)
            df['ema200'] = cs.calc_emas(df, 200).round(2)

            df['rsi'] = cs.calc_rsi(df).round(2)
            # df['pct_rng'] = df.apply(cs.calc_pct_rng, axis=1).round(2)
            # df['pct_strch'] = cs.calc_pct_strch(df)
            #continue
            df['sma20'].replace(math.nan, 0.0,inplace=True)
            df['sma50'].replace(math.nan, 0.0,inplace=True)
            df['sma100'].replace(math.nan, 0.0,inplace=True)
            df['sma200'].replace(math.nan, 0.0,inplace=True)
            df['ema9'].replace(math.nan, 0.0,inplace=True)
            df['ema15'].replace(math.nan, 0.0,inplace=True)
            df['ema65'].replace(math.nan, 0.0,inplace=True)
            df['ema200'].replace(math.nan, 0.0,inplace=True)

            ut.df_to_csv(df, calc_path, ticker)

         #   print(ticker, sma200)


        except Exception as e:
            raise e


start = time.time()

stocks = [f for f in listdir(mypath) if isfile(join(mypath, f))]

list_of_stocks = mf.chunk_list(stocks, 5)

threads = []
nums = []

ps = []
for i in list_of_stocks:
    p = Process(target=get_live_data, args=(i,))
    ps.append(p)
    p.start()


print(time.time() - start)


sys.exit(0)


if True:
#if mf.is_market_open("e"):
    for i in range(len(list_of_stocks)):
        t = Thread(target=get_live_data, args=(list_of_stocks[i],))
        threads.append(t)


    [t.start() for t in threads]
    [t.join() for t in threads]


end = time.time()
print(end - start)






