from django.urls import path
from . import views

urlpatterns = [
    path(
        "recommendations/",
        views.user_recommendations,
        name="user_recommendations"
    ),
]