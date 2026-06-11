from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("", include("dashboard.urls")),
    path("", include("interviews.urls")),

    path("api/", include("recommendations.urls")),
    path("api/", include("bookmarks.urls")),
    path("api/", include("opportunities.urls")),
    path("api/", include("interviews.urls")),
]