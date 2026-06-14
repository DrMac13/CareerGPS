from django.urls import path

from . import views


urlpatterns = [
    path(
        "career-readiness/",
        views.career_readiness_api,
        name="career_readiness_api"
    ),
]