# scraper
## 概要
日経平均構成銘柄をWEBから取得  
取得した銘柄のデータを取得

## 構成
#### 言語
- Python 3.7.1
#### ライブラリ
- pandas
- bs4
- yfinance

## Docker
```
git clone https://github.com/stupid-sugar/scraper.git scraper
cd scraper
docker-compose up -d
docker exec -it myapp bash
python scrape.py
python fetch.py
```
## 使用方法
scrape.pyで構成銘柄を取得してCSVデータとして保存  
fetch.pyでデータを取得  
fetch.py updateでデータを更新

## 注意点
- 現状、日足での動作しか確認できていません
- yfinanceで取得できる価格が正しくないことがあります
