from django.urls import path
from . import views

urlpatterns = [
    path(
        "bookmarks/toggle/",
        views.toggle_bookmark,
        name="toggle_bookmark"
    ),

    path(
        "bookmarks/",
        views.saved_opportunities,
        name="saved_opportunities"
    ),
]