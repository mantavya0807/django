# frontend/forms.py

from django import forms

class FetchStockForm(forms.Form):
    symbol = forms.CharField(max_length=10, label='Stock Symbol', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AAPL'}))

class BacktestForm(forms.Form):
    initial_investment = forms.FloatField(label='Initial Investment ($)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10000'}))
    buy_moving_average = forms.IntegerField(label='Buy Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50'}))
    sell_moving_average = forms.IntegerField(label='Sell Moving Average (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 200'}))
    symbol = forms.CharField(max_length=10, label='Stock Symbol', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AAPL'}))

class PredictionForm(forms.Form):
    symbol = forms.CharField(max_length=10, label='Stock Symbol', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AAPL'}))
    days = forms.IntegerField(label='Number of Days to Predict', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 30'}))
