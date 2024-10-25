# frontend/urls.py

from django.urls import path
from . import views

app_name = 'frontend'  # Define the app namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch_stock/', views.fetch_stock_data, name='fetch_stock'),
    path('backtest/', views.backtest_view, name='backtest'),
    path('predictions/', views.predictions_view, name='predictions'),
    path('reports/', views.reports_view, name='reports'),
]
