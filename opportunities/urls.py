from django.urls import path
from . import views

urlpatterns = [
    path("opportunities/", views.opportunity_list, name="opportunity_list"),

    path(
        "opportunities/apply/",
        views.apply_to_opportunity,
        name="apply_to_opportunity"
    ),

    path(
        "applications/",
        views.my_applications,
        name="my_applications"
    ),

    path(
        "applications/update-status/",
        views.update_application_status,
        name="update_application_status"
    ),

    path(
        "market-skills/",
        views.market_skills_analytics,
        name="market_skills_analytics"
    ),
]