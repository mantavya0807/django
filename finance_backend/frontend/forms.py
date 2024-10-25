# frontend/forms.py

from django import forms
from data_fetcher.models import StockPrice

# List of stock symbols
STOCK_CHOICES = [
    ('AAPL', 'Apple (AAPL)'),
    ('GOOGL', 'Alphabet (GOOGL)'),
    ('AMZN', 'Amazon (AMZN)'),
    ('MSFT', 'Microsoft (MSFT)'),
    ('TSLA', 'Tesla (TSLA)'),
    # Add more stock symbols as needed
]

class FetchStockForm(forms.Form):
    symbol = forms.ChoiceField(choices=STOCK_CHOICES, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))


class BacktestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BacktestForm, self).__init__(*args, **kwargs)

        # Get unique stock symbols from the StockPrice model
        fetched_symbols = StockPrice.objects.values_list('symbol', flat=True).distinct()

        # Combine initial predefined choices and fetched symbols
        all_choices =[(symbol, symbol) for symbol in fetched_symbols]

        # Set up the symbol field with the combined choices
        self.fields['symbol'] = forms.ChoiceField(choices=all_choices, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))

    initial_investment = forms.FloatField(label='Initial Investment ($)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10000'}))
    buy_moving_average = forms.IntegerField(label='Buy Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50'}))
    sell_moving_average = forms.IntegerField(label='Sell Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 200'}))

class PredictionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)

        # Get unique stock symbols from the StockPrice model
        fetched_symbols = StockPrice.objects.values_list('symbol', flat=True).distinct()

        # Combine initial predefined choices and fetched symbols
        all_choices =[(symbol, symbol) for symbol in fetched_symbols]

        # Set up the symbol field with the combined choices
        self.fields['symbol'] = forms.ChoiceField(choices=all_choices, label='Stock Symbol', widget=forms.Select(attrs={'class': 'form-control'}))
    days = forms.IntegerField(label='Number of Days to Predict', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30'}))