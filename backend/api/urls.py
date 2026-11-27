from django.urls import path
from .views import AnalysisView, ApprovalView

urlpatterns = [
    path("analysis/", AnalysisView.as_view()),
    path("approval/", ApprovalView.as_view(), name="approval"),
]