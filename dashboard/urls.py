from django.urls import path
from dashboard.views import (
    dashboard_page,
    opportunities_page
)

urlpatterns = [
    path("dashboard/", dashboard_page, name="dashboard"),
    path("dashboard/opportunities/", opportunities_page, name="opportunities_page"),
    ]
