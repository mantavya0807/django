# data_fetcher/urls.py

from django.urls import path
from .views import FetchStockDataView

urlpatterns = [
    path('fetch/', FetchStockDataView.as_view(), name='fetch_stock_data'),
]
