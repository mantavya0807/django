# backtesting/serializers.py

from rest_framework import serializers
from .models import Backtest, BacktestResult

class BacktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backtest
        fields = ['id', 'initial_investment', 'buy_moving_average', 'sell_moving_average', 'symbol', 'created_at']

class BacktestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = BacktestResult
        fields = ['total_return', 'max_drawdown', 'trades_executed', 'generated_at']
