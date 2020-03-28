import os
import sys
import datetime
from time import sleep
import time
import json
import logging
import logging.config

import pprint
from threading import Thread
import subprocess
import random
import requests


# from pandas_datareader import data
#import matplotlib.pyplot as plt
#import pandas as pd
#from pandas.tseries.offsets import BDay
#import statistics

from alpha_vantage.timeseries import TimeSeries


sys.exit(0)
sys.path.append(r'/home/usaman14ever/gtspython/core')


import sql_db as dbm
import fixed_data_inputs as fdi
import main_functions as mf
import calcs_live as cs
from gt_email import GTEmail

logging.basicConfig(filename=fdi.LOGGING_CONFIG_FILE, level=logging.INFO)
logging.info('can you see this')

total_email_scan_tickers = []
total_hits = 0

final_stock_data = []
final_stock_data_daily = []

def get_live_data(stocks):
    try:
        dbm.delete_stock_daily(datetime.date.today())
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    
    for ticker in stocks:
        try:
            ts = TimeSeries(key='WU1NJSA5J52X92E3', output_format='pandas')
            df, meta_data = ts.get_intraday(symbol=ticker,interval='5min', outputsize='full')
            df = df.iloc[::-1]

            global total_hits
            total_hits += 1

            data = {}

            
           
            data['t_ticker'] = ticker
            data['t_date'] = df.index[-1].to_pydatetime()
            data['t_open'] = df.iloc[-1]['1. open']
            data['t_high'] = df.iloc[-1]['2. high']
            data['t_low'] = df.iloc[-1]['3. low']
            data['t_close'] = df.iloc[-1]['4. close']
            data['t_volume'] = df.iloc[-1]['5. volume']

            # data['sma20'] = cs.calc_smas(df, 20).iloc[-1]
            # data['sma50'] = cs.calc_smas(df, 50).iloc[-1]
            # data['sma100'] = cs.calc_smas(df, 100).iloc[-1]
            # data['sma200'] = cs.calc_smas(df, 200).iloc[-1]

            # data['ema9'] = cs.calc_emas(df, 9).iloc[-1]
            # data['ema15'] = cs.calc_emas(df, 15).iloc[-1]
            # data['ema65'] = cs.calc_emas(df, 65).iloc[-1]
            # data['ema200'] = cs.calc_emas(df, 200).iloc[-1]
            data['rsi'] = cs.calc_rsi(df).iloc[-1]
            data['pct_rng'] = cs.calc_pct_rng(df.iloc[-1])
            data['pct_chng'] = mf.get_pct_chng(data['t_open'], data['t_close'])

            final_stock_data.append(data)
            daily_data = cs.calc_create_day(df)
            daily_data['t_date'] = datetime.date.today()
            daily_data['t_ticker'] = ticker
            final_stock_data_daily.append(daily_data)

            logging.info(ticker)
            logging.info(data)

     
            #####################   Itraday spike     #####################
            if abs(cs.scan_pct_change(df.tail(1))) > .8:
                total_email_scan_tickers.append(ticker)

        except Exception as ex:
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname  = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print exc_type, fname, exc_tb.tb_lineno
            # dbm.insert_bad_tickers(ticker)
            print (ex)
            pass
            # raise ex


start = time.time()


# time.sleep(10)



print(mf.is_market_open("e"))

list_of_stocks = mf.chunk_list(list(fdi.SP500), 15)
# list_of_stocks = [["GE"]]
# sys.exit(0)

threads = []
nums = []

# if True:
if mf.is_market_open("e"):
    for i in range(len(list_of_stocks)):
        t = Thread(target=get_live_data, args=(list_of_stocks[i],))
        threads.append(t)


    [t.start() for t in threads]
    [t.join() for t in threads]

    if len(total_email_scan_tickers) > 0:
        try:
            html = "http://geraldgale.com/chart?tickers={}".format(','.join(total_email_scan_tickers))
            # e = GTEmail()
            # e.send_email_basic("gerald.gale@gmail.com", "JUMP", html)
        except Exception as e:
            pass


try:
    dbm.delete_live_5min(mf.get_date_midnight(mf.get_past_date(mf.get_now(), 1)))
except Exception as e:
    logging.error("Exception occurred", exc_info=True)

try:
    dbm.insert_live_5min(final_stock_data)
except Exception as e:
    logging.error("Exception occurred", exc_info=True)




try:
    dbm.insert_live_daily(final_stock_data_daily)
except Exception as e:
    logging.error("Exception occurred", exc_info=True)


# try:
#     dbm.insert_live_5min_archive(final_stock_data)
# except Exception as e:
#     logging.error("Exception occurred", exc_info=True)









# try:
#     dbm.delete_live_5min(mf.get_date_midnight(mf.get_past_date(mf.get_now(), 1)))
#     dbm.insert_live_5min(final_stock_data)
#     dbm.delete_stock_daily(datetime.date.today())
#     dbm.insert_live_daily(final_stock_data_daily)
#     dbm.insert_live_5min_archive(final_stock_data)
#     e.send_email_basic("gerald.gale@gmail.com", "bbbbbbbbbbbbbbbb", "bbbbbbbbbbbbbbb")
# except Exception as e:
#     e.send_email_basic("gerald.gale@gmail.com", "cccccccccccc", "cccccccccccccc")
#     print (e)
#     pass

# n = datetime.datetime.now()
# if n.hour > 16 and n.minute > 5 and n.minute < 20:
#     yest_midnight = datetime.datetime(n.year, n.month, n.day) - datetime.timedelta(days = 1)
# dbm.delete_live_5min(yest_midnight)
# dbm.delete_stock_news(ticker)

end = time.time()
print(end - start)

print(total_hits)














































# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=aapl&interval=5min&outputsize=full&apikey=WU1NJSA5J52X92E3'

# resp = requests.get(url=url)
# data = resp.json()

# print(data)

# ticker = "AAPL"

# ts = TimeSeries(key='WU1NJSA5J52X92E3', output_format='pandas')
# df, meta_data = ts.get_intraday(symbol=ticker,interval='5min', outputsize='full')

# print(df)





