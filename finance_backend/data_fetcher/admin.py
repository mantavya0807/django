# data_fetcher/admin.py

from django.contrib import admin
from .models import StockPrice

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume')
    search_fields = ('symbol',)
    list_filter = ('symbol', 'date')
