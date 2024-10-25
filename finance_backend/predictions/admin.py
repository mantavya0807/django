from django.contrib import admin
from .models import Prediction
# Register your models here.

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'prediction_date', 'predicted_price', 'actual_price', 'created_at']
    search_fields = ['symbol']
    list_filter = ['symbol', 'prediction_date']
    date_hierarchy = 'prediction_date'
    ordering = ['-prediction_date']
    list_editable = ['actual_price']