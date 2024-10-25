from django.shortcuts import render

# Create your views here.
# backtesting/views.py

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
            return Response({
                'backtest': serializer.data,
                'result': result_serializer.data
            }, status=status.HTTP_201_CREATED)
        except BacktestResult.DoesNotExist:
            return Response({
                'backtest': serializer.data,
                'result': None
            }, status=status.HTTP_201_CREATED)
