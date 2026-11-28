from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from .models import AnalysisRun
from .serializers import (
    AnalysisSerializer,
    ApprovalSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from .services import run_analysis, resume_analysis
from intelligence.data.ingestion import ingest_market_data


def _auth_response(user, status_code=status.HTTP_200_OK):
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {"token": token.key, "user": UserSerializer(user).data},
        status=status_code,
    )


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return _auth_response(user, status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return _auth_response(serializer.validated_data["user"])


class LogoutView(APIView):
    def post(self, request):
        # Deleting the token invalidates it everywhere.
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

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
        except Exception:
            return Response(
                {"error": "Analysis failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Record who owns this thread so only they can approve it.
        AnalysisRun.objects.create(
            user=request.user,
            thread_id=result["thread_id"],
            symbol=serializer.validated_data["symbol"],
            timeframe=serializer.validated_data["timeframe"],
            decision=result.get("decision", ""),
            approval_status=(
                "PENDING" if result.get("approval_required")
                else result.get("status", "FAILED")
            ),
        )
        return Response(result)


class ApprovalView(APIView):
    def post(self, request):
        serializer = ApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread_id = serializer.validated_data["thread_id"]

        # 404 (not 403) so other users' thread ids aren't confirmed to exist.
        run = AnalysisRun.objects.filter(
            thread_id=thread_id, user=request.user
        ).first()
        if run is None:
            return Response(
                {"error": "Analysis not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if run.approval_status != "PENDING":
            return Response(
                {"error": "This analysis has already been reviewed."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            result = resume_analysis(
                thread_id=thread_id,
                approved=serializer.validated_data["approved"],
            )

            run.approval_status = result.get("approval_status", "REJECTED")
            run.save(update_fields=["approval_status"])
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