# backtesting/admin.py

from django.contrib import admin
from .models import Backtest, BacktestResult

@admin.register(Backtest)
class BacktestAdmin(admin.ModelAdmin):
    list_display = ['id', 'symbol', 'initial_investment', 'buy_moving_average', 'sell_moving_average', 'created_at']
    search_fields = ['symbol']

@admin.register(BacktestResult)
class BacktestResultAdmin(admin.ModelAdmin):
    list_display = ['backtest', 'total_return', 'max_drawdown', 'trades_executed', 'generated_at']
