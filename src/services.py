import os
from src.utils import reader_excel
import re
import logging

logger = logging.getLogger("news")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("news.log", encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_dir = os.path.dirname(__file__)
data_dir = os.path.join(current_dir, "..", "data")
operations_file_path = os.path.join(data_dir, "operations.xlsx")


def services(date: str):
    """Выводит сумму операции и имя физ. лица"""
    all_operations = reader_excel(operations_file_path)
    filtered_operations_dict = all_operations.to_dict(orient="records")
    operations_list = []
    for operation in filtered_operations_dict:
        total_spent = operation.get('Сумма платежа')
        name = operation.get("Описание")
        if operation.get("Категория") == "Переводы":
            pattern = re.compile(r"([А-ЯЁ][a-zA-ZёЁа-яА-Я]+\s+[А-ЯЁ]\.)")
            match = pattern.findall(name)
            if match:
                full_name = ' '.join(match)
                operations_list.append({
                    "total_spent": total_spent,
                    "name": full_name
                })
    result = {
        "translations": operations_list
    }
    logger.info(f"Найдено {len(operations_list)} транзакций")
    return result


# print(services("2021-07-01 01:02:03"))
