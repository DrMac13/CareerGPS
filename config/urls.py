from django.contrib import admin
from django.urls import path, include
from dashboard.views import (
    home_page,
    about_page,
    dashboard_page,
    login_page,
    opportunities_page,
    applications_page,
    register_page,
    saved_page,
    interview_history_page,
    interview_analytics_page,
    resources_page,
    profile_page,
    profile_summary_api,
    stories_page,
    contact_page,
    verify_email_page
    
)



urlpatterns = [

    path(
        "login/",
        login_page,
        name="login_page"
    ),

    path(
        "register/",
        register_page,
        name="register_page"
    ),

    path(
        "",
        home_page,
        name="home_page"
    ),

    path(
        "about/",
        about_page,
        name="about_page"
    ),
    
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

        path(
        "dashboard/resources/",
        resources_page,
        name="resources_page"
    ),

    path(
        "dashboard/profile/",
        profile_page,
        name="profile_page"
    ),

    path(
        "api/profile/summary/",
        profile_summary_api,
        name="profile_summary_api"
    ),

    path(
        "dashboard/saved/",
        saved_page,
        name="saved_page"
    ),

    path(
        "stories/",
        stories_page,
        name="stories_page"
    ),

    path(
        "contact/",
        contact_page,
        name="contact_page"
    ),

    path(
        "verify-email/",
        verify_email_page,
        name="verify_email_page"
    ),


    path("", include("interviews.urls")),
    path("api/", include("analytics.urls")),

    path("api/", include("recommendations.urls")),
    path("api/", include("bookmarks.urls")),
    path("api/", include("opportunities.urls")),
    path("api/", include("interviews.urls")),
    path("ingestion/",include("ingestion.urls")
),
]