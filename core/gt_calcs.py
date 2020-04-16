import os
import sys
import datetime
import json
import random
import requests

import pprint
import pytz



import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay
import ta

import core.gt_functions as mf

from alpha_vantage.timeseries import TimeSeries


################################################################################
#####   CALC TECHNICAL INDICATOR FUNCTIONS
################################################################################
def calc_smas(data, sma_len=20):
    try:
        smas = data['4. close'].rolling(sma_len).mean()

        return smas
    except Exception as e:
        # print e
        raise e



def calc_emas(data, ema_len=9):
    try:
        emas = ta.trend.EMAIndicator(data['4. close'], ema_len, False)
        
        return emas.ema_indicator()
    except Exception as e:
        # print e
        raise e

def calc_rsi(data):
    try:
        rsi = ta.momentum.RSIIndicator(data['4. close'])
        
        return rsi.rsi()
    except Exception as e:
        # print e
        raise e


def calc_pct_rng(data):
    try:
        o = data['1. open']
        h = data['2. high']
        l = data['3. low']
        c = data['4. close']
        
        rng = h - l
        dff = c - o
        pct = 0

        if rng != 0 and dff != 0:
            pct = dff / rng

        return pct
    except Exception as e:
        # print e
        raise e


def calc_pct_strch(df):
    
    try:
        tmp_strch = []
#        print(df)
        counter = 0
        for index, row in df.iterrows():

            if counter == 0:
                # print(index, df[index])
                # df[row['pct_strch']] = 0
                tmp_strch.append(0)
                counter += 1
                continue


            pvo = df.iloc[counter - 1]['1. open']
            pvc = df.iloc[counter - 1]['4. close']
            pvpct_rng = df.iloc[counter - 1]['pct_rng']
            pvchng = mf.get_pct_chng(pvo, pvc)
            o = df.iloc[counter]['1. open']
            c = df.iloc[counter]['4. close']
            pct_rng = df.iloc[counter - 1]['pct_rng']
            chng = mf.get_pct_chng(o, c)

            if (pvchng > 0) != (chng > 0):
                # df[row['pct_strch']] = 0
                tmp_strch.append(0)
                counter += 1
                continue

            drctn = (chng > 0)

            if abs(pct_rng) < .6 or abs(pvpct_rng) < .6:
                # df[row['pct_strch']] = 0
                tmp_strch.append(0)
                counter += 1
                continue

            

            tmp_strch.append(1)

            # access data using column names
            # print(df.iloc[counter])
            # print(index, row['delay'], row['distance'], row['origin'])
            counter += 1
        df['pct_strch'] = tmp_strch
#        print(tmp_strch)
        return tmp_strch
    except Exception as e:
        raise e


################################################################################
#####   SCAN  FUNCTIONS
################################################################################
def scan_pct_change(price_data):
    try:
        t_open = price_data.iloc[-1]['1. open']
        t_high = price_data.iloc[-1]['2. high']
        t_low = price_data.iloc[-1]['3. low']
        t_close = price_data.iloc[-1]['4. close']

        pct_diff = mf.get_pct_chng(t_open, t_close)
        # pct_rng = mf.get_bar_range_pct(t_open, t_close, t_high, t_low)

        return pct_diff
    except Exception as e:
        raise e




























