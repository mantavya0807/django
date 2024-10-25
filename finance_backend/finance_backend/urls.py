# finance_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from reports.views import (
    BacktestReportPDFView,
    BacktestReportJSONView,
    PredictionReportPDFView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),  # Include frontend URLs with namespace
    path('api/', include('backtesting.urls')),
    path('api/', include('predictions.urls')),
    path('api/', include('reports.urls')),
    path('fetch_stock/', include('data_fetcher.urls')),
    # Report URLs
    path('report/backtest/<int:backtest_id>/pdf/', BacktestReportPDFView.as_view(), name='backtest-report-pdf'),
    path('report/backtest/<int:backtest_id>/json/', BacktestReportJSONView.as_view(), name='backtest-report-json'),
    path('report/prediction/<str:symbol>/pdf/', PredictionReportPDFView.as_view(), name='prediction-report-pdf'),
]
