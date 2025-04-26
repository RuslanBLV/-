# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import json
from src.utils import day_time_now, reader_excel
from src.utils import get_user_settings, get_stock_prices, get_currency_rates
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger("news")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("news.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv()
api_key_stocks = os.getenv('API_STOCKS')
api_key_currencies = os.getenv('API_CURRENCIES')

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "..", "data")
operations_file_path = os.path.join(data_dir, "operations.xlsx")

current_dir = os.path.dirname(__file__)
root_dir = os.path.join(current_dir, "..")
settings_file_path = os.path.join(root_dir, "user_settings.json")


def home(date: str):
    date_today = day_time_now()
    end_point = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_point = end_point.replace(day=1, hour=0, minute=0, second=0)

    all_operations = reader_excel(operations_file_path)
    filtered_operations = all_operations.loc[
        (pd.to_datetime(all_operations["Дата операции"], dayfirst=True) >= start_point) &
        (pd.to_datetime(all_operations["Дата операции"], dayfirst=True) <= end_point)]

    date_dict = filtered_operations.to_dict(orient="records")
    sorted_filtered_operations = filtered_operations.sort_values(by='Сумма операции с округлением', ascending=False)
    sorted_filtered_operations_head = sorted_filtered_operations.head().to_dict(orient="records")

    cards = []
    top_transactions = []
    for card in date_dict:
        card_number = card.get('Номер карты')
        total_spent = card.get('Сумма операции с округлением')
        cashback = round((total_spent / 100), 2)

        if card_number and not pd.isna(card_number):
            last_digits = card_number[1:]
            cards.append({
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback,
            })

    for transactions in sorted_filtered_operations_head:
        date = transactions.get("Дата операции")
        amount = transactions.get("Сумма операции")
        category = transactions.get("Категория")
        description = transactions.get("Описание")
        top_transactions.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })

    user_settings = get_user_settings()
    currency_rates = get_currency_rates(user_settings['user_currencies'])
    stock_prices = get_stock_prices(user_settings['user_stocks'])

    result = {
        "greeting": date_today,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    logger.info(f"Найдено {len(cards)} транзакций с переводами физ. лицам")
    return json.dumps(result, ensure_ascii=False, indent=4)

# print(home("2021-12-17 01:02:03"))
