from rest_framework import serializers


class AnalysisSerializer(serializers.Serializer):
    symbol = serializers.CharField(default="BTC/USDT")
    timeframe = serializers.ChoiceField(
        choices=["15m", "1h", "4h", "1d"],
        default="1h",
    )

    portfolio_value = serializers.FloatField(
        required=False, default=10000.0, min_value=0.01
    )
    risk_per_trade_pct = serializers.FloatField(
        required=False, default=1.0, min_value=0.01, max_value=100
    )
    stop_loss_pct = serializers.FloatField(
        required=False, default=2.0, min_value=0.01, max_value=100
    )
    max_exposure_pct = serializers.FloatField(
        required=False, default=20.0, min_value=0, max_value=100
    )
    current_exposure_pct = serializers.FloatField(
        required=False, default=0.0, min_value=0, max_value=100
    )



class ApprovalSerializer(serializers.Serializer):
    thread_id = serializers.CharField()
    approved = serializers.BooleanField()