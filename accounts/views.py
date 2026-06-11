from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from profiles.models import (
    UserProfile,
    Institution,
    DegreeProgram,
    Skill,
    Interest,
    UserSkill,
    UserInterest
)
from django.shortcuts import render
import random
from django.utils import timezone

from django.core.mail import send_mail
from .models import EmailVerification
from django.contrib.auth import authenticate, login, logout


import json


def register_page(request):
    return render(request, 'accounts/register.html')

@csrf_exempt
def register_user(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request"},
            status=400
        )

    try:

        data = json.loads(request.body)

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        if not all([
            first_name,
            last_name,
            email,
            password
        ]):
            return JsonResponse(
                {
                    "success": False,
                    "error": "All fields are required"
                },
                status=400
            )

        if User.objects.filter(
            username=email
        ).exists():

            return JsonResponse(
                {
                    "success": False,
                    "error": "Email already registered"
                },
                status=400
            )

        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),
            is_active=True
        )

        UserProfile.objects.create(
            user=user

        )
        
        
        verification_code = str(
            random.randint(100000, 999999)
        )

        EmailVerification.objects.create(
            email=email,
            code=verification_code
        )

        send_mail(
            subject="CareerGPS Verification Code",
            message=f"Your verification code is: {verification_code}",
            from_email="noreply@careergps.com",
            recipient_list=[email],
            fail_silently=False,
        )



        return JsonResponse(
            {
                "success": True,
                "message": "Registration successful"
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )
    
@csrf_exempt
def verify_email(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid request"
            },
            status=400
        )

    try:

        data = json.loads(request.body)

        email = data.get("email")
        code = data.get("code")

        verification = EmailVerification.objects.filter(
            email=email,
            code=code,
            is_used=False
        ).first()

        if not verification:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid verification code"
                },
                status=400
            )

        verification.is_used = True
        verification.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Email verified successfully"
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )

@csrf_exempt
def complete_profile(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Invalid request"},
            status=400
        )

    try:
        data = json.loads(request.body)

        email = data.get("email")
        institution_id = data.get("institution_id")
        degree_program_id = data.get("degree_program_id")
        location = data.get("location")
        skill_ids = data.get("skills", [])
        interest_ids = data.get("interests", [])

        user = User.objects.get(email=email)
        profile = UserProfile.objects.get(user=user)

        if institution_id:
            profile.institution = Institution.objects.get(id=institution_id)

        if degree_program_id:
            profile.degree_program = DegreeProgram.objects.get(id=degree_program_id)

        profile.location = location or ""
        profile.save()

        UserSkill.objects.filter(profile=profile).delete()
        UserInterest.objects.filter(profile=profile).delete()

        for skill_id in skill_ids:
            skill = Skill.objects.get(id=skill_id)
            UserSkill.objects.create(
                profile=profile,
                skill=skill,
                proficiency_level="Beginner",
                years_experience=0
            )

        for interest_id in interest_ids:
            interest = Interest.objects.get(id=interest_id)
            UserInterest.objects.create(
                profile=profile,
                interest=interest
            )

        return JsonResponse({
            "success": True,
            "message": "Profile completed successfully"
        })

    except User.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "User not found"},
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )

@csrf_exempt
def login_user(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Invalid request"},
            status=400
        )

    try:
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is None:
            return JsonResponse(
                {"success": False, "error": "Invalid email or password"},
                status=401
            )

        login(request, user)

        return JsonResponse({
            "success": True,
            "message": "Login successful"
        })

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )


def logout_user(request):
    logout(request)

    return JsonResponse({
        "success": True,
        "message": "Logged out successfully"
    })