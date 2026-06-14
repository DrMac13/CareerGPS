from django.shortcuts import render
from django.http import JsonResponse

from profiles.models import (
    UserProfile,
    UserSkill,
    UserInterest,
    UserEducation
)

def login_page(request):
    return render(
        request,
        "public/login.html"
    )

def register_page(request):
    return render(
        request,
        "public/register.html"
    )

def home_page(request):
    return render(
        request,
        "public/home.html"
    )

def about_page(request):
    return render(
        request,
        "public/about.html"
    )

def dashboard_page(request):
    return render(request, "dashboard/dashboard.html", {
        "active_page": "dashboard"
    })


def opportunities_page(request):
    return render(request, "dashboard/opportunities.html", {
        "active_page": "opportunities"
    })

def applications_page(request):
    return render(request, "dashboard/applications.html", {
        "active_page": "applications"
    })


def interview_history_page(request):
    return render(request, "dashboard/interview_history.html", {
        "active_page": "interview_history"
    })


def interview_analytics_page(request):
    return render(request, "dashboard/interview_analytics.html", {
        "active_page": "interview_analytics"
    })

def resources_page(request):
    return render(request, "dashboard/resources.html", {
        "active_page": "resources"
    })


def profile_page(request):
    return render(request, "dashboard/profile.html", {
        "active_page": "profile"
    })

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

    education_entries = UserEducation.objects.filter(
        profile=profile
    ).order_by(
        "-end_year",
        "-start_year"
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

        "cv": {
            "uploaded": bool(profile.cv_file),
            "file_name": profile.cv_file.name if profile.cv_file else None,
            "text_length": len(profile.cv_text or ""),
        },

        "education": [
            {
                "institution_name": item.institution_name,
                "qualification_name": item.qualification_name,
                "field_of_study": item.field_of_study,
                "start_year": item.start_year,
                "end_year": item.end_year,
                "source": item.source,
            }
            for item in education_entries
        ],


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

def saved_page(request):
    return render(request, "dashboard/saved.html", {
        "active_page": "saved"
    })

def stories_page(request):
    return render(
        request,
        "public/stories.html"
    )

def contact_page(request):
    return render(
        request,
        "public/contact.html"
    )

def verify_email_page(request):
    return render(
        request,
        "public/verify_email.html"
    )