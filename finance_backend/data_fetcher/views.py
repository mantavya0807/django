from django.shortcuts import render

# data_fetcher/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import fetch_stock_data

class FetchStockDataView(APIView):
    def post(self, request):
        symbol = request.data.get('symbol', 'AAPL').upper()
        fetch_stock_data.delay(symbol)
        return Response({"message": f"Data fetching for {symbol} initiated."}, status=status.HTTP_202_ACCEPTED)
