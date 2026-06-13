from django.contrib import admin
from django.urls import path, include
from dashboard.views import (
    dashboard_page,
    opportunities_page
)
from dashboard.views import (
    dashboard_page,
    opportunities_page,
    applications_page
)
from dashboard.views import (
    dashboard_page,
    opportunities_page,
    applications_page,
    interview_history_page,
    interview_analytics_page
)



urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("", include("dashboard.urls")),
    path("dashboard/", dashboard_page, name="dashboard"),
    path("dashboard/opportunities/", opportunities_page, name="opportunities_page"),
    path(
        "dashboard/applications/",
        applications_page,
        name="applications_page"
    ),

    path(
        "dashboard/interviews/history/",
        interview_history_page,
        name="interview_history_page"
    ),

    path(
        "dashboard/interviews/analytics/",
        interview_analytics_page,
        name="interview_analytics_page"
    ),

    path("", include("interviews.urls")),

    path("api/", include("recommendations.urls")),
    path("api/", include("bookmarks.urls")),
    path("api/", include("opportunities.urls")),
    path("api/", include("interviews.urls")),
    path("ingestion/",include("ingestion.urls")
),
]