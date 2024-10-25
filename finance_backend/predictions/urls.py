# predictions/urls.py

from django.urls import path
from .views import PredictionCreateView

urlpatterns = [
    path('predict/', PredictionCreateView.as_view(), name='prediction-create'),
]
