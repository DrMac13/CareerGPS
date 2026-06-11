from django.urls import path
from . import views

urlpatterns = [
    path(
        "interview/",
        views.interview_page,
        name="interview_page"
    ),

    path(
        "interviews/start/",
        views.start_interview,
        name="start_interview"
    ),

    path(
        "interviews/respond/",
        views.submit_response,
        name="submit_response"
    ),
    path(
    "interviews/report/<int:session_id>/",
    views.interview_report,
    name="interview_report"
    ),
    path(
    "interviews/history/",
    views.interview_history,
    name="interview_history"
    ),
    path(
    "interviews/analytics/",
    views.interview_analytics,
    name="interview_analytics"
    ),
]
