from typing import Any, Optional
import pandas as pd
import os
from src.utils import reader_excel
import logging

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "..", "data")
operations_file_path = os.path.join(data_dir, "operations.xlsx")

transaction = reader_excel(operations_file_path)

logger = logging.getLogger("news")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("news.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def reports(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict[Any, Any]]:
    """Возвращает траты по заданной категории за последние три месяца."""
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.Timestamp(date)
    start_date = date - pd.DateOffset(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        ]
    df_dict = filtered_transactions.to_dict(orient='records')
    result = []
    for i in df_dict:
        result.append({i["Категория"]: i["Сумма операции с округлением"]})
    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")
    return result

# print(reports(transaction, 'Супермаркеты'))
