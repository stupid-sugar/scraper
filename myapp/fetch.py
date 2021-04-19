# coding: UTF-8
import os
import yfinance as yf
import pandas as pd

"""
code: stock code
interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
start: YYYY-MM-DD
end: YYYY-MM-DD
"""
def download(save_format, code, interval, start, end):
    msft = yf.Ticker(str(code)+".T")
    data = msft.history(period="max", interval=interval, start=start, end=end)
    data.to_csv(save_format.format(code))

# param
df = pd.read_csv("stock_list.csv")
save_folder = "data"
save_format = save_folder+"/code_{}.csv"
interval = "1d"
start = "2021-01-01"
end = "2021-04-01"

# ディレクトリが存在しない場合に作成
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# データの取得  
for i in range(len(df)):
    print(df.iloc[i, 2])
    download(save_format, df["code"].iloc[i], interval, start, end)

