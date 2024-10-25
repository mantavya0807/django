# reports/services.py

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings
from backtesting.models import Backtest
from predictions.models import Prediction
from data_fetcher.models import StockPrice

def generate_backtest_report(backtest_id):
    try:
        backtest = Backtest.objects.get(id=backtest_id)
        result = backtest.result
    except Backtest.DoesNotExist:
        raise ValueError("Backtest not found.")
    except BacktestResult.DoesNotExist:
        raise ValueError("Backtest result not found.")

    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Backtest Report for {backtest.symbol}")

    # Backtest Details
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Initial Investment: ${backtest.initial_investment}")
    p.drawString(50, height - 100, f"Buy Moving Average: {backtest.buy_moving_average}-day")
    p.drawString(50, height - 120, f"Sell Moving Average: {backtest.sell_moving_average}-day")
    p.drawString(50, height - 140, f"Total Return: {result.total_return:.2f}%")
    p.drawString(50, height - 160, f"Max Drawdown: {result.max_drawdown:.2f}%")
    p.drawString(50, height - 180, f"Trades Executed: {result.trades_executed}")

    # Generate graph
    data = StockPrice.objects.filter(symbol=backtest.symbol).order_by('date')
    df = pd.DataFrame(list(data.values('date', 'close_price')))
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df['close_price'], label='Close Price')
    plt.title('Stock Close Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()

    # Save plot to a PNG image in memory
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)

    # Draw image on PDF
    p.drawImage(img_buffer, 50, height - 500, width=500, height=300)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def generate_prediction_report(symbol='AAPL'):
    predictions = Prediction.objects.filter(symbol=symbol).order_by('prediction_date')
    if not predictions.exists():
        raise ValueError("No predictions found for the given symbol.")

    data = list(predictions.values('prediction_date', 'predicted_price', 'actual_price'))
    df = pd.DataFrame(data)
    df['prediction_date'] = pd.to_datetime(df['prediction_date'])

    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Prediction Report for {symbol}")

    # Generate comparison graph
    plt.figure(figsize=(10, 4))
    plt.plot(df['prediction_date'], df['predicted_price'], label='Predicted Price', marker='o')
    actual_data = df.dropna(subset=['actual_price'])
    if not actual_data.empty:
        plt.plot(actual_data['prediction_date'], actual_data['actual_price'], label='Actual Price', marker='x')
    plt.title('Predicted vs Actual Stock Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()

    # Save plot to a PNG image in memory
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)

    # Draw image on PDF
    p.drawImage(img_buffer, 50, height - 500, width=500, height=300)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def generate_backtest_report_json(backtest_id):
    try:
        backtest = Backtest.objects.get(id=backtest_id)
        result = backtest.result
    except Backtest.DoesNotExist:
        raise ValueError("Backtest not found.")
    except BacktestResult.DoesNotExist:
        raise ValueError("Backtest result not found.")

    report = {
        "symbol": backtest.symbol,
        "initial_investment": backtest.initial_investment,
        "buy_moving_average": backtest.buy_moving_average,
        "sell_moving_average": backtest.sell_moving_average,
        "total_return": result.total_return,
        "max_drawdown": result.max_drawdown,
        "trades_executed": result.trades_executed,
        "generated_at": result.generated_at.isoformat(),
    }
    return json.dumps(report, indent=4)
