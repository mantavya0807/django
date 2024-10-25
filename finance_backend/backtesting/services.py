# backtesting/services.py

import pandas as pd
from .models import Backtest, BacktestResult
from data_fetcher.models import StockPrice

def perform_backtest(backtest_id):
    try:
        backtest = Backtest.objects.get(id=backtest_id)
    except Backtest.DoesNotExist:
        return

    symbol = backtest.symbol
    initial_investment = backtest.initial_investment
    buy_ma = backtest.buy_moving_average
    sell_ma = backtest.sell_moving_average

    # Fetch historical data
    data = StockPrice.objects.filter(symbol=symbol).order_by('date')
    df = pd.DataFrame(list(data.values('date', 'close_price')))
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    if df.empty:
        return

    # Calculate moving averages
    df['MA_buy'] = df['close_price'].rolling(window=buy_ma).mean()
    df['MA_sell'] = df['close_price'].rolling(window=sell_ma).mean()

    # Initialize variables
    position = False
    buy_price = 0.0
    shares = 0
    cash = initial_investment
    trades = 0
    portfolio_values = []

    for current_date, row in df.iterrows():
        if pd.isna(row['MA_buy']) or pd.isna(row['MA_sell']):
            portfolio_values.append(cash if not position else shares * row['close_price'])
            continue

        # Buy condition
        if not position and row['close_price'] < row['MA_buy']:
            shares = cash / row['close_price']
            buy_price = row['close_price']
            cash = 0.0
            position = True
            trades += 1

        # Sell condition
        elif position and row['close_price'] > row['MA_sell']:
            cash = shares * row['close_price']
            shares = 0
            position = False
            trades += 1

        # Calculate current portfolio value
        portfolio_value = shares * row['close_price'] if position else cash
        portfolio_values.append(portfolio_value)

    # Final portfolio value
    if position:
        cash = shares * df.iloc[-1]['close_price']
        portfolio_values[-1] = cash

    total_return = ((cash - initial_investment) / initial_investment) * 100

    # Calculate max drawdown
    portfolio_series = pd.Series(portfolio_values, index=df.index)
    rolling_max = portfolio_series.cummax()
    drawdown = (portfolio_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100  # As percentage

    # Save results
    BacktestResult.objects.create(
        backtest=backtest,
        total_return=total_return,
        max_drawdown=max_drawdown,
        trades_executed=trades
    )
