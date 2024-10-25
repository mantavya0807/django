# backtesting/views.py
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Backtest, BacktestResult
from .serializers import BacktestSerializer, BacktestResultSerializer
from .services import perform_backtest

class BacktestCreateView(generics.CreateAPIView):
    serializer_class = BacktestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        backtest = serializer.save()
        perform_backtest(backtest.id)
        try:
            result = backtest.result
            result_serializer = BacktestResultSerializer(result)
            
            # Render the result to an HTML template instead of returning a JSON response
            return render(request, 'backtest_result.html', {
                'backtest': serializer.data,
                'result': result_serializer.data
            })
        except BacktestResult.DoesNotExist:
            # Even if result is not available, render the template with backtest data
            return render(request, 'backtest_result.html', {
                'backtest': serializer.data,
                'result': None
            })
