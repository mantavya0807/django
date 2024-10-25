from django.shortcuts import render, redirect
from django.contrib import messages
from data_fetcher.models import StockPrice
from backtesting.models import Backtest, BacktestResult
from predictions.models import Prediction
from backtesting.services import perform_backtest
from predictions.services import generate_predictions
from django.urls import reverse
from django.http import HttpResponse, Http404
import json
from .forms import FetchStockForm, BacktestForm, PredictionForm
from backtesting.models import Backtest
from predictions.models import Prediction
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')

def fetch_stock_data(request):
    stock_data = None
    stock_symbol = None
    form = FetchStockForm()
    if request.method == 'POST':
        form = FetchStockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()
            try:
                from django.core.management import call_command
                call_command('fetch_stock_data', symbol)
                messages.success(request, f"Successfully fetched data for {symbol}.")
                stock_symbol = symbol
                stock_data = StockPrice.objects.filter(symbol=symbol).order_by('-date')[:100]
            except Exception as e:
                messages.error(request, f"Error fetching data for {symbol}: {str(e)}")
    return render(request, 'fetch_stock.html', {'form': form, 'stock_data': stock_data, 'stock_symbol': stock_symbol})

def backtest_view(request):
    backtest_result = None
    form = BacktestForm()
    if request.method == 'POST':
        form = BacktestForm(request.POST)
        if form.is_valid():
            initial_investment = form.cleaned_data['initial_investment']
            buy_ma = form.cleaned_data['buy_moving_average']
            sell_ma = form.cleaned_data['sell_moving_average']
            symbol = form.cleaned_data['symbol'].upper()
            try:
                if buy_ma >= sell_ma:
                    messages.error(request, "Buy MA should be less than Sell MA.")
                    return render(request, 'backtest.html', {'form': form})
                
                backtest = Backtest.objects.create(
                    initial_investment=initial_investment,
                    buy_moving_average=buy_ma,
                    sell_moving_average=sell_ma,
                    symbol=symbol
                )
                
                perform_backtest(backtest.id)
                
                backtest_result = backtest.result
                messages.success(request, f"Backtest completed for {symbol}.")
            except Exception as e:
                messages.error(request, f"Error during backtest: {str(e)}")
    return render(request, 'backtest.html', {'form': form, 'backtest_result': backtest_result})

def predictions_view(request):
    predictions = None
    form = PredictionForm()
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol'].upper()
            days = form.cleaned_data['days']
            try:
                generate_predictions(symbol=symbol, days=days)
                messages.success(request, f"Generated predictions for {symbol} for the next {days} days.")
                predictions = Prediction.objects.filter(symbol=symbol).order_by('-prediction_date')[:days]
            except Exception as e:
                messages.error(request, f"Error generating predictions: {str(e)}")
    return render(request, 'predictions.html', {'form': form, 'predictions': predictions})



def reports_view(request):
    # Backtest search and pagination
    backtest_search_query = request.GET.get('backtest_search', '')
    backtests = Backtest.objects.filter(symbol__icontains=backtest_search_query).order_by('-created_at')
    
    paginator_backtest = Paginator(backtests, 10)  # Show 10 backtests per page
    page_number_backtest = request.GET.get('page_backtest')
    page_backtests = paginator_backtest.get_page(page_number_backtest)

    # Prediction search and pagination
    prediction_search_query = request.GET.get('prediction_search', '')
    predictions = Prediction.objects.filter(symbol__icontains=prediction_search_query).order_by('-created_at')

    paginator_prediction = Paginator(predictions, 10)  # Show 10 predictions per page
    page_number_prediction = request.GET.get('page_prediction')
    page_predictions = paginator_prediction.get_page(page_number_prediction)

    context = {
        'backtests': page_backtests,
        'predictions': page_predictions,
    }

    return render(request, 'reports.html', context)
