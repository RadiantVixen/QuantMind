from django.urls import path
from .views import AnalysisView, ApprovalView, MarketDataView

urlpatterns = [
    path("analysis/", AnalysisView.as_view()),
    path("approval/", ApprovalView.as_view(), name="approval"),
    path("market-data/", MarketDataView.as_view(), name="market-data"),
]
