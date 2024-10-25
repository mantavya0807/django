from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import generate_predictions
from .models import Prediction
from .serializers import PredictionSerializer

class PredictionCreateView(APIView):
    def post(self, request, format=None):
        symbol = request.data.get('symbol', 'AAPL').upper()
        days = request.data.get('days', 30)

        try:
            days = int(days)
            if days <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid 'days' parameter. Must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            generate_predictions(symbol=symbol, days=days)
        except FileNotFoundError as fnf_err:
            return Response({"error": str(fnf_err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Retrieve the latest predictions
        predictions = Prediction.objects.filter(symbol=symbol).order_by('-prediction_date')[:days]
        serializer = PredictionSerializer(predictions, many=True)

        # Instead of returning a JSON response, we render the result using a template
        context = {
            'predictions': predictions,
            'symbol': symbol
        }
        return render(request, 'predictions_result.html', context)
