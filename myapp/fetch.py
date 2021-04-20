# coding: UTF-8
import sys
import os
import datetime
import yfinance as yf
import pandas as pd
    
class Scraper():
    def __init__(self, param={}):
        # set default param
        self._setDefaultParam()
        # set user defined param
        for k, v in param.items():  setattr(self, k, v)        

        # create directory
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    """
    interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    start: YYYY-MM-DD
    end: YYYY-MM-DD
    """        
    def _setDefaultParam(self):
        # param
        self.save_folder = "data"
        self.save_format = param['save_folder']+"/code_{}.csv"
        self.interval = "1d"
        # download today data
        today, tomorrow = datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1)
        self.start = today.strftime('%Y-%m-%d')
        self.end = tomorrow.strftime('%Y-%m-%d')

    """
    Download
    """
    def download(self, code):
        msft = yf.Ticker(str(code)+".T")
        data = msft.history(period="max", interval=self.interval, start=self.start, end=self.end)
        data.to_csv(self.save_format.format(code))

    """
    Update
    """
    def update(self, code):
        data = pd.read_csv(self.save_format.format(code), index_col="Date")
        start = data.index[-1]
        
        if start==self.start:
            print('code {} have updated already')
            return
            
        msft = yf.Ticker(str(code)+".T")
        row = msft.history(period="max", interval=self.interval, start=start, end=self.end)
        row.index = row.index.astype(str)

        data = pd.concat([data, row], axis=0)
        data.to_csv(self.save_format.format(code)) 



operation = 'download'
if len(sys.argv) > 1:   operation = sys.argv[1]

param = {}
"""
param['interval'] = '1d'
param['start'] = '2021-01-01'
param['end'] = '2021-04-01'
"""
Scraper = Scraper(param)
df = pd.read_csv("stock_list.csv")

if operation == 'download': function = getattr(Scraper, 'download')
elif operation == 'update': function = getattr(Scraper, 'update')
else:   print("Not Supported Operation")
    
for i in range(len(df)):
    print(df.iloc[i, 2])
    function(df["code"].iloc[i])
