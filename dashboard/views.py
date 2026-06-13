from django.shortcuts import render


def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")


def opportunities_page(request):
    return render(
        request,
        "dashboard/opportunities.html"
    )

def applications_page(request):
    return render(
        request,
        "dashboard/applications.html"
    )


def interview_history_page(request):
    return render(
        request,
        "dashboard/interview_history.html"
    )


def interview_analytics_page(request):
    return render(
        request,
        "dashboard/interview_analytics.html"
    )

def resources_page(request):
    return render(
        request,
        "dashboard/resources.html"
    )

def profile_page(request):
    return render(
    request,
    "dashboard/profile.html"
)
