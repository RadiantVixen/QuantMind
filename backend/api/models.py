from django.conf import settings
from django.db import models


class AnalysisRun(models.Model):
    """Links a LangGraph thread to the user who started it.

    Only the owner of a run can approve or reject it.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="analysis_runs",
    )
    thread_id = models.CharField(max_length=64, unique=True)
    symbol = models.CharField(max_length=32)
    timeframe = models.CharField(max_length=8)
    decision = models.CharField(max_length=16, blank=True)
    approval_status = models.CharField(max_length=16, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.symbol} {self.timeframe} · {self.user} · {self.approval_status}"
