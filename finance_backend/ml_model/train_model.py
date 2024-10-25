import os
import sys
import django
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Set the DJANGO_SETTINGS_MODULE environment variable before importing any Django-related modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_backend.settings')

# Add finance_backend directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
django.setup()

# Now import the models after setting up Django
from data_fetcher.models import StockPrice
from django.conf import settings

def train_and_save_model():
    # Fetch historical data
    data = StockPrice.objects.filter(symbol='AAPL').order_by('date')
    df = pd.DataFrame(list(data.values('date', 'close_price')))
    
    # Ensure 'day' column exists
    df['day'] = range(len(df))

    X = df[['day']]
    y = df['close_price']

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    model_dir = os.path.join(settings.BASE_DIR, 'ml_model')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'linear_regression.pkl')
    joblib.dump(model, model_path)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_and_save_model()
