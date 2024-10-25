# predictions/models.py

from django.db import models

class Prediction(models.Model):
    symbol = models.CharField(max_length=10)
    prediction_date = models.DateField()
    predicted_price = models.FloatField()
    actual_price = models.FloatField(null=True, blank=True)  # To compare later
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('symbol', 'prediction_date')

    def __str__(self):
        return f"{self.symbol} - {self.prediction_date}"
