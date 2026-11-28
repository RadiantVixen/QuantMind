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



# ---------- Authentication ----------

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate(self, attrs):
        # Runs Django's AUTH_PASSWORD_VALIDATORS (length, common passwords, ...).
        validate_password(
            attrs["password"],
            user=User(username=attrs["username"], email=attrs.get("email", "")),
        )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError(
                {"error": "Invalid username or password."}
            )
        attrs["user"] = user
        return attrs
