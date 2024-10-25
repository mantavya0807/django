# predictions/serializers.py

from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['symbol', 'prediction_date', 'predicted_price', 'actual_price', 'created_at']
