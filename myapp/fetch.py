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
        if len(data)>0: data.to_csv(self.save_format.format(code))

    """
    Update
    """
    def update(self, code):
        if os.path.exists(self.save_format.format(code))==False:
            self.download(code)
            return
        
        data = pd.read_csv(self.save_format.format(code), index_col="Date")
        start = data.index[-1]
                
        msft = yf.Ticker(str(code)+".T")
        row = msft.history(period="max", interval=self.interval, start=start, end=self.end)
        row.index = row.index.astype(str)
        
        # yfinance library get out of range data
        # ex. param (start='2021-04-24', end='2021-04-27') returned 2021-04-23 data
        # That's why remove duplicated data to maintain accuracy
        data = pd.concat([data, row], axis=0)
        data = data[~data.index.duplicated(keep='first')]
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

# yahoo finance price is not accurate
# ex. (DENSO 4902.T 2021-04-12 ~ 2021-04-16) prices were multiplied x100
if operation == 'download': function = getattr(Scraper, 'download')
elif operation == 'update': function = getattr(Scraper, 'update')
else:   print("Not Supported Operation")
    
for i in range(len(df)):
    print(df.iloc[i, 2])
    function(df["code"].iloc[i])
