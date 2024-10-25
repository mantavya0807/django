# reports/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import (
    generate_backtest_report,
    generate_backtest_report_json,
    generate_prediction_report
)
from django.http import FileResponse
import logging

logger = logging.getLogger(__name__)

class BacktestReportPDFView(APIView):
    def get(self, request, backtest_id, format=None):
        try:
            report_pdf = generate_backtest_report(backtest_id)
            logger.debug("Backtest PDF generated: %s", report_pdf)
            report_pdf.seek(0)  # Ensure the buffer is at the beginning
            response = FileResponse(report_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="backtest_report_{backtest_id}.pdf"'
            return response
        except (ValueError, TypeError) as e:
            logger.error("Invalid Backtest ID: %s", str(e))
            return Response({"error": f"Invalid Backtest ID: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected Error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BacktestReportJSONView(APIView):
    def get(self, request, backtest_id, format=None):
        try:
            report_json = generate_backtest_report_json(backtest_id)
            return HttpResponse(report_json, content_type='application/json')
        except (ValueError, TypeError):
            return Response({"error": "Invalid Backtest ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictionReportPDFView(APIView):
    def get(self, request, symbol, format=None):
        try:
            report_pdf = generate_prediction_report(symbol)
            logger.debug("Prediction PDF generated: %s", report_pdf)
            report_pdf.seek(0)  # Ensure the buffer is at the beginning
            response = FileResponse(report_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="prediction_report_{symbol}.pdf"'
            return response
        except ValueError as e:
            logger.error("Invalid symbol: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected Error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

