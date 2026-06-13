from django.contrib import admin
from django.urls import path, include
from dashboard.views import (
    dashboard_page,
    opportunities_page
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("", include("dashboard.urls")),
    path("dashboard/", dashboard_page, name="dashboard"),
    path("dashboard/opportunities/", opportunities_page, name="opportunities_page"),
    path("", include("interviews.urls")),

    path("api/", include("recommendations.urls")),
    path("api/", include("bookmarks.urls")),
    path("api/", include("opportunities.urls")),
    path("api/", include("interviews.urls")),
    path("ingestion/",include("ingestion.urls")
),
]