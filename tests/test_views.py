import unittest
from unittest.mock import patch
import pandas as pd
import json
from src.views import home


class TestHomeFunction(unittest.TestCase):
    @patch('src.utils.get_stock_prices')
    @patch('src.utils.get_currency_rates')
    @patch('src.utils.get_user_settings')
    @patch('src.utils.reader_excel')
    @patch('src.utils.day_time_now')
    def test_home(self, mock_day_time_now, mock_reader_excel, mock_get_user_settings,
                  mock_get_currency_rates, mock_get_stock_prices):
        mock_day_time_now.return_value = "Добрый день"

        data = {
            "Дата операции": ["15.06.2023 10:00:00", "15.06.2023 15:00:00", "01.05.2023 09:00:00"],
            "Номер карты": ["0123456789", "0987654321", None],
            "Сумма операции с округлением": [1500.0, 2500.0, 100.0],
            "Сумма операции": [1499.75, 2500.20, 100.50],
            "Категория": ["Питание", "Транспорт", "Развлечения"],
            "Описание": ["Обед в кафе", "Такси", "Кино"]
        }
        df = pd.DataFrame(data)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        mock_reader_excel.return_value = df

        mock_get_user_settings.return_value = {
            'user_currencies': ['EUR', 'USD'],
            'user_stocks': ['AAPL', 'MSFT']
        }

        mock_get_currency_rates.return_value = {'EUR': 0.9, 'USD': 1.0}

        mock_get_stock_prices.return_value = {'AAPL': 150.0, 'MSFT': 250.0}

        result_json = home("2023-06-15 23:59:59")
        result = json.loads(result_json)

        self.assertIn("greeting", result)
        self.assertIn("cards", result)
        self.assertIn("top_transactions", result)
        self.assertIn("currency_rates", result)
        self.assertIn("stock_prices", result)

        self.assertEqual(len(result['cards']), 0)
        self.assertEqual(len(result['top_transactions']), 0)

        self.assertEqual(result['currency_rates']['EUR'], 0.88)
        self.assertEqual(result['stock_prices']['AAPL'], 0)


if __name__ == '__main__':
    unittest.main()
