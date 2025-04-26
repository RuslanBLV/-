# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key_stocks = os.getenv('API_STOCKS')
api_key_currencies = os.getenv("API_CURRENCIES")

current_dir = os.path.dirname(__file__)
root_dir = os.path.join(current_dir, "..")
settings_file_path = os.path.join(root_dir, "user_settings.json")


def reader_excel(path):
    """Выводит список словарей странзакций из файла .xlsx"""
    pf = pd.read_excel(path)
    df_cleaned = pf.dropna(how='all')
    file_dataframe = pd.DataFrame(df_cleaned)
    return file_dataframe


def day_time_now():
    current_date_time = datetime.datetime.now()
    hour = current_date_time.hour
    if 0 <= hour < 6 or 22 <= hour <= 23:
        return "Доброй ночи"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    elif 7 <= hour <= 11:
        return "Доброе утро"
    else:
        return "Добрый день"


def get_user_settings():
    with open(settings_file_path, encoding="utf-8") as file:
        settings = json.load(file)
    return settings


def get_currency_rates(currencies):
    rates = {}
    for currency in currencies:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/USD')
        if response.status_code == 200:
            rates[currency] = response.json().get('rates', {}).get(currency, None)
    return rates


def get_stock_prices(user_stocks):
    stock_prices = {}
    for stock in user_stocks:
        response = requests.get(
            f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key_stocks}')
        stock_data = response.json()
        stock_prices[stock] = stock_data.get('latestPrice', 0)
    return stock_prices

