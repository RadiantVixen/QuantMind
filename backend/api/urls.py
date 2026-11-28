from django.urls import path
from .views import (
    AnalysisView,
    ApprovalView,
    LoginView,
    LogoutView,
    MarketDataView,
    MeView,
    RegisterView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("analysis/", AnalysisView.as_view(), name="analysis"),
    path("approval/", ApprovalView.as_view(), name="approval"),
    path("market-data/", MarketDataView.as_view(), name="market-data"),
]
