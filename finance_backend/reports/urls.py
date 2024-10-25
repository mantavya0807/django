# reports/urls.py

from django.urls import path
from .views import (
    BacktestReportPDFView,
    BacktestReportJSONView,
    PredictionReportPDFView
)

urlpatterns = [
    path('backtest/<int:backtest_id>/report/pdf/', BacktestReportPDFView.as_view(), name='backtest-report-pdf'),
    path('backtest/<int:backtest_id>/report/json/', BacktestReportJSONView.as_view(), name='backtest-report-json'),
    path('prediction/<str:symbol>/report/pdf/', PredictionReportPDFView.as_view(), name='prediction-report-pdf'),
]
