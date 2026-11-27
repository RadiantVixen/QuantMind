from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalysisSerializer
from .services import run_analysis
from .serializers import ApprovalSerializer
from .services import resume_analysis
from intelligence.data.ingestion import ingest_market_data

class AnalysisView(APIView):

    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = run_analysis(serializer.validated_data)
            return Response(result)

        except Exception:
            return Response(
                {"error": "Analysis failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ApprovalView(APIView):
    def post(self, request):
        serializer = ApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = resume_analysis(
                thread_id=serializer.validated_data["thread_id"],
                approved=serializer.validated_data["approved"],
            )

            return Response(result)

        except Exception:
            return Response(
                {"error": "Unable to resume this analysis."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MarketDataView(APIView):

    def get(self, request):
        symbol = request.query_params.get("symbol", "BTC/USDT")
        timeframe = request.query_params.get("timeframe", "1h")

        try:
            df = ingest_market_data(
                symbol=symbol,
                timeframe=timeframe,
                limit=100,
            )

            candles = df.to_dict("records")

            for candle in candles:
                candle["timestamp"] = candle["timestamp"].isoformat()
                for key in ["open", "high", "low", "close", "volume"]:
                    candle[key] = float(candle[key])

            return Response({
                "symbol": symbol,
                "timeframe": timeframe,
                "candles": candles,
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )