from django.shortcuts import render
from rest_framework.views import APIView
from .tasks import fetch_stock_data

class FetchStockDataView(APIView):
    def post(self, request):
        symbol = request.data.get('symbol', 'AAPL').upper()
        context = {'symbol': symbol, 'error': None, 'message': None}

        try:
            fetch_stock_data(symbol)
            context['message'] = f"Data fetching for {symbol} completed."
        except Exception as e:
            context['error'] = str(e)

        return render(request, 'fetch_stocks.html', context)
