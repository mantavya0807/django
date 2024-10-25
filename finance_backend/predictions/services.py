# predictions/services.py

import os
import joblib
import pandas as pd
from datetime import timedelta, date
from django.conf import settings
from .models import Prediction
from data_fetcher.models import StockPrice

def generate_predictions(symbol='AAPL', days=30):
    # Load the pre-trained model
    model_path = os.path.join(settings.BASE_DIR, 'ml_model', 'linear_regression.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Pre-trained model not found. Please train the model first.")

    model = joblib.load(model_path)

    # Fetch historical data
    data = StockPrice.objects.filter(symbol=symbol).order_by('date')
    df = pd.DataFrame(list(data.values('date', 'close_price')))
    df = df.sort_values('date')
    df.reset_index(drop=True, inplace=True)

    if df.empty:
        raise ValueError("No historical data available for predictions.")

    # **Add the 'day' column required for the model**
    df['day'] = range(len(df))

    last_day = df['day'].max()
    last_date = df['date'].max()

    # Prepare data for prediction
    future_days = [[last_day + i + 1] for i in range(days)]
    predictions = model.predict(future_days)

    prediction_objects = []
    for i in range(days):
        prediction_date = last_date + timedelta(days=i+1)
        predicted_price = predictions[i]
        prediction = Prediction(
            symbol=symbol,
            prediction_date=prediction_date,
            predicted_price=predicted_price
        )
        prediction_objects.append(prediction)

    # Bulk create predictions, ignoring duplicates
    Prediction.objects.bulk_create(prediction_objects, ignore_conflicts=True)
    print(f"Generated predictions for {symbol} for the next {days} days.")
