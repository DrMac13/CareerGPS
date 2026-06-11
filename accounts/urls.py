from django.urls import path
from . import views
from .views import (
    register_user,
    verify_email
)
from .views import register_user, verify_email, complete_profile

urlpatterns = [

    # HTML page
    path(
        "register/",
        views.register_page,
        name="register"
    ),

    # API endpoint
    path(
        "api/register/",
        views.register_user,
        name="api_register"
    ),
    path(
    "api/verify-email/",
    verify_email,
    name="verify_email"
    ),
    path(
    "api/complete-profile/",
    complete_profile,
    name="complete_profile"
    ),
    path("api/login/", views.login_user, name="api_login"),
    path("api/logout/", views.logout_user, name="api_logout"),
]