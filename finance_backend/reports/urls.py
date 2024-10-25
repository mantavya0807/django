# reports/urls.py

from django.urls import path
from .views import (
    BacktestReportPDFView,
    BacktestReportJSONView,
    PredictionReportPDFView
)

urlpatterns = [
    path('report/backtest/<int:backtest_id>/pdf/', BacktestReportPDFView.as_view(), name='backtest-report-pdf'),
    path('report/backtest/<int:backtest_id>/json/', BacktestReportJSONView.as_view(), name='backtest-report-json'),
    path('report/prediction/<str:symbol>/pdf/', PredictionReportPDFView.as_view(), name='prediction-report-pdf'),
]
