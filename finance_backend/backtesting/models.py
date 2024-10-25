# backtesting/models.py

from django.db import models

class Backtest(models.Model):
    initial_investment = models.FloatField()
    buy_moving_average = models.IntegerField(default=50)
    sell_moving_average = models.IntegerField(default=200)
    symbol = models.CharField(max_length=10, default='AAPL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backtest {self.id} for {self.symbol}"

class BacktestResult(models.Model):
    backtest = models.OneToOneField(Backtest, on_delete=models.CASCADE, related_name='result')
    total_return = models.FloatField()
    max_drawdown = models.FloatField()
    trades_executed = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for Backtest {self.backtest.id}"
