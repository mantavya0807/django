# backtesting/urls.py

from django.urls import path
from .views import BacktestCreateView

urlpatterns = [
    path('backtest/', BacktestCreateView.as_view(), name='backtest-create'),
]
