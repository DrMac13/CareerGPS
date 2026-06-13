from django.shortcuts import render
from django.http import JsonResponse

from profiles.models import (
    UserProfile,
    UserSkill,
    UserInterest
)


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

def profile_page(request):
    return render(
        request,
        "dashboard/profile.html"
    )


def profile_summary_api(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "error": "Authentication required"
            },
            status=401
        )

    try:
        profile = UserProfile.objects.select_related(
            "institution",
            "degree_program"
        ).get(
            user=request.user
        )

    except UserProfile.DoesNotExist:
        return JsonResponse({
            "success": True,
            "profile": None,
            "completion": 0,
            "skills": [],
            "interests": []
        })

    skills = UserSkill.objects.filter(
        profile=profile
    ).select_related(
        "skill"
    )

    interests = UserInterest.objects.filter(
        profile=profile
    ).select_related(
        "interest"
    )

    checks = [
        bool(profile.institution),
        bool(profile.degree_program),
        bool(profile.location),
        bool(profile.bio),
        skills.exists(),
        interests.exists(),
    ]

    completion = int(
        sum(checks) / len(checks) * 100
    )

    return JsonResponse({
        "success": True,
        "profile": {
            "username": request.user.username,
            "email": request.user.email,
            "institution": profile.institution.name if profile.institution else "Not added",
            "degree_program": profile.degree_program.name if profile.degree_program else "Not added",
            "faculty": profile.degree_program.faculty if profile.degree_program else "Not added",
            "location": profile.location or "Not added",
            "bio": profile.bio or "Not added",
            "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
            "created_at": profile.created_at.strftime("%Y-%m-%d"),
            "updated_at": profile.updated_at.strftime("%Y-%m-%d"),
        },
        "completion": completion,
        "skills": [
            {
                "name": item.skill.name,
                "category": item.skill.category,
                "proficiency_level": item.proficiency_level,
                "years_experience": item.years_experience,
            }
            for item in skills
        ],
        "interests": [
            item.interest.name
            for item in interests
        ]
    })