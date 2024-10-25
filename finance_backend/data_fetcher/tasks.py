# data_fetcher/tasks.py
import requests
from django.conf import settings
from .models import StockPrice
from datetime import datetime, timedelta
import time
from django.db import IntegrityError


def fetch_stock_data(symbol='AAPL'):
    api_key = settings.ALPHA_VANTAGE_API_KEY
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'apikey': api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'Error Message' in data:
            raise ValueError(f"API Error: {data['Error Message']}")
        elif 'Time Series (Daily)' not in data:
            raise ValueError("Unexpected response structure from Alpha Vantage")

        time_series = data['Time Series (Daily)']

        bulk_create = []
        for date_str, metrics in time_series.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            open_price = float(metrics['1. open'])
            high_price = float(metrics['2. high'])
            low_price = float(metrics['3. low'])
            close_price = float(metrics['4. close'])
            volume = int(metrics['5. volume'])

            stock_price = StockPrice(
                symbol=symbol,
                date=date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume
            )
            bulk_create.append(stock_price)

        # Bulk create with ignore_conflicts to avoid duplicates
        StockPrice.objects.bulk_create(bulk_create, ignore_conflicts=True)
        print(f"Successfully fetched and stored data for {symbol}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except ValueError as val_err:
        print(f"Value error: {val_err}")
    except IntegrityError as ie:
        print(f"Database integrity error: {ie}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
