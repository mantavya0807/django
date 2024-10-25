# data_fetcher/management/commands/fetch_stock_data.py

import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from data_fetcher.models import StockPrice
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Fetches daily stock prices from Alpha Vantage and stores them in the database.'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for (e.g., AAPL)')

    def handle(self, *args, **kwargs):
        symbol = kwargs['symbol'].upper()
        api_key = settings.ALPHA_VANTAGE_API_KEY
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'datatype': 'json',
            'apikey': api_key,
        }

        self.stdout.write(f"Fetching data for {symbol} from Alpha Vantage...")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Check for errors in response
            if "Error Message" in data:
                raise CommandError(f"Error from API: {data['Error Message']}")
            if "Note" in data:
                raise CommandError(f"Note from API: {data['Note']}")
            if "Time Series (Daily)" not in data:
                raise CommandError("Invalid data format received from Alpha Vantage.")

            time_series = data["Time Series (Daily)"]

            bulk_create = []
            for date_str, metrics in time_series.items():
                try:
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
                except (KeyError, ValueError) as e:
                    self.stderr.write(f"Skipping date {date_str} due to error: {e}")
                    continue

            # Bulk create with ignore_conflicts to avoid duplicates
            StockPrice.objects.bulk_create(bulk_create, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully fetched and stored data for {symbol}"))

        except requests.exceptions.HTTPError as http_err:
            raise CommandError(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            raise CommandError(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            raise CommandError(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            raise CommandError(f"An error occurred: {req_err}")
        except CommandError as ce:
            raise ce
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")
