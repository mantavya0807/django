# reports/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import (
    generate_backtest_report,
    generate_backtest_report_json,
    generate_prediction_report
)
from backtesting.models import Backtest
from django.http import HttpResponse, JsonResponse
import json

class BacktestReportPDFView(APIView):
    def get(self, request, backtest_id, format=None):
        try:
            # backtest_id is passed via GET parameters
            backtest_id = request.GET.get('backtest_id')
            if not backtest_id:
                return Response({"error": "Backtest ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            backtest_id = int(backtest_id)
            report_pdf = generate_backtest_report(backtest_id)
            response = HttpResponse(report_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="backtest_report_{backtest_id}.pdf"'
            return response
        except (ValueError, TypeError):
            return Response({"error": "Invalid Backtest ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BacktestReportJSONView(APIView):
    def get(self, request, backtest_id, format=None):
        try:
            backtest_id = request.GET.get('backtest_id')
            if not backtest_id:
                return Response({"error": "Backtest ID is required."}, status=status.HTTP_400_BAD_REQUEST)
            backtest_id = int(backtest_id)
            report_json = generate_backtest_report_json(backtest_id)
            return HttpResponse(report_json, content_type='application/json')
        except (ValueError, TypeError):
            return Response({"error": "Invalid Backtest ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionReportPDFView(APIView):
    def get(self, request, symbol, format=None):
        try:
            symbol = request.GET.get('symbol')
            if not symbol:
                return Response({"error": "Stock symbol is required."}, status=status.HTTP_400_BAD_REQUEST)
            report_pdf = generate_prediction_report(symbol)
            response = HttpResponse(report_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="prediction_report_{symbol}.pdf"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
