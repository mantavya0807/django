# backtesting/tests.py

from django.test import TestCase
from .models import Backtest, BacktestResult
from data_fetcher.models import StockPrice
from .services import perform_backtest
from datetime import date

class BacktestTestCase(TestCase):
    def setUp(self):
        # Create sample stock data
        StockPrice.objects.create(symbol='AAPL', date=date(2022, 1, 1), open_price=150, high_price=155, low_price=149, close_price=154, volume=1000000)
        StockPrice.objects.create(symbol='AAPL', date=date(2022, 1, 2), open_price=154, high_price=156, low_price=153, close_price=155, volume=1100000)
        # Add more data as needed for testing

    def test_backtest_creation(self):
        backtest = Backtest.objects.create(
            initial_investment=10000,
            buy_moving_average=2,
            sell_moving_average=3,
            symbol='AAPL'
        )
        perform_backtest(backtest.id)
        result = BacktestResult.objects.get(backtest=backtest)
        self.assertIsNotNone(result)
        self.assertIn('total_return', result.__dict__)
