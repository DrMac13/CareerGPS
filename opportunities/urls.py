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
]