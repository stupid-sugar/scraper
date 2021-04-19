# coding: UTF-8
import urllib.request  as urllib2
from bs4 import BeautifulSoup
import pandas as pd

url = "https://indexes.nikkei.co.jp/nkave/index/component?idx=nk225"
html = urllib2.urlopen(url)
soup = BeautifulSoup(html, "html.parser", from_encoding='utf-8')


# select nikkei info block
nikkei_info = soup.select(".container .col-sm-8 .component-list")

code, stock_name, company_name = [], [], []
for row in nikkei_info:
    code.append(row.select_one("div:nth-of-type(1)").text)
    stock_name.append(row.select_one("div:nth-of-type(2)").text)
    company_name.append(row.select_one("div:nth-of-type(3)").text)

df = pd.DataFrame()
df['code'] = code
df['stock_name'] = stock_name
df['company_name'] = company_name

df.to_csv("stock_list.csv", encoding="utf-8-sig", index=False)
