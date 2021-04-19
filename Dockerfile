FROM python:3.7-slim

WORKDIR /root/app

RUN pip install bs4 && pip install yfinance
