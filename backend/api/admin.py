from django.contrib import admin

from .models import AnalysisRun


@admin.register(AnalysisRun)
class AnalysisRunAdmin(admin.ModelAdmin):
    list_display = ("symbol", "timeframe", "user", "decision", "approval_status", "created_at")
    list_filter = ("approval_status", "decision", "symbol")
    search_fields = ("thread_id", "user__username")
