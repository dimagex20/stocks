import os
import sys
import datetime
from time import sleep
import time
import json
import logging
import logging.config

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
from numpy import nan

from alpha_vantage.timeseries import TimeSeries

sys.path.append(r'/home/gtserver/code/repos/stocks/')

import core.gt_db as dbm
import core.gt_inputs as fdi
import core.gt_functions as mf
import core.gt_utils as ut
import core.gt_calcs as cs
#from gt_email import GTEmail


from multiprocessing import Process

mypath = "/home/gtserver/code/repos/stocks/data/raw/5min"
calc_path = "/home/gtserver/code/repos/stocks/data/calcd/5min"

mypath = "/home/gtserver/code/repos/stocks/data/raw/5min"
mypath = "/home/gtserver/code/repos/stocks/data/calcd/5min"

final_data = []

def get_calcd_data(stocks):
    for ticker in stocks:
        df = ut.csv_to_df(mypath, ticker)
        df = df.iloc[-1]
        final_data.append(ut.clean_dict_db(df.to_dict(), ticker))


stocks = [f for f in listdir(mypath) if isfile(join(mypath, f))]
get_calcd_data(stocks)

dbm.insert_live_5min(final_data)



