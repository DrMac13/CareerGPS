from django.http import JsonResponse
from django.db.models import Q

from .models import Opportunity
import json
from django.views.decorators.csrf import csrf_exempt

from .models import Opportunity, Application
from django.db.models import Count
from opportunities.models import OpportunitySkill


def opportunity_list(request):

    opportunities = Opportunity.objects.filter(
        is_active=True
    ).select_related("company")

    search = request.GET.get("search")
    location = request.GET.get("location")
    opportunity_type = request.GET.get("type")
    experience = request.GET.get("experience")
    company = request.GET.get("company")

    if search:
        opportunities = opportunities.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(company__name__icontains=search)
        )

    if location:
        opportunities = opportunities.filter(
            location__icontains=location
        )

    if opportunity_type:
        opportunities = opportunities.filter(
            opportunity_type=opportunity_type
        )

    if experience:
        opportunities = opportunities.filter(
            experience_level=experience
        )

    if company:
        opportunities = opportunities.filter(
            company__name__icontains=company
        )

    data = []

    for opportunity in opportunities:
        data.append({
            "id": opportunity.id,
            "title": opportunity.title,
            "company": opportunity.company.name,
            "location": opportunity.location,
            "opportunity_type": opportunity.opportunity_type,
            "experience_level": opportunity.experience_level,
            "salary": opportunity.salary,
            "application_url": opportunity.application_url,
            "source": opportunity.source,
            "closing_date": (
                opportunity.closing_date.strftime("%Y-%m-%d")
                if opportunity.closing_date
                else None
            ),
        })

    return JsonResponse({
        "success": True,
        "count": len(data),
        "opportunities": data
    })


@csrf_exempt
def apply_to_opportunity(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Invalid request"},
            status=400
        )

    try:
        data = json.loads(request.body)
        opportunity_id = data.get("opportunity_id")

        opportunity = Opportunity.objects.get(id=opportunity_id)

        application, created = Application.objects.get_or_create(
            user=request.user,
            opportunity=opportunity,
            defaults={
                "status": "Applied"
            }
        )

        if not created:
            return JsonResponse({
                "success": True,
                "message": "You already applied",
                "status": application.status
            })

        return JsonResponse({
            "success": True,
            "message": "Application recorded",
            "status": application.status
        })

    except Opportunity.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Opportunity not found"},
            status=404
        )


def my_applications(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    applications = Application.objects.filter(
        user=request.user
    ).select_related("opportunity", "opportunity__company")

    data = []

    for app in applications:
        opp = app.opportunity

        data.append({
            "id": app.id,
            "opportunity_id": opp.id,
            "title": opp.title,
            "company": opp.company.name,
            "location": opp.location,
            "status": app.status,
            "notes": app.notes,
            "applied_at": app.applied_at.strftime("%Y-%m-%d %H:%M"),
            "application_url": opp.application_url,
        })

    return JsonResponse({
        "success": True,
        "applications": data
    })


@csrf_exempt
def update_application_status(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Invalid request"},
            status=400
        )

    try:
        data = json.loads(request.body)

        application_id = data.get("application_id")
        status = data.get("status")
        notes = data.get("notes", "")

        valid_statuses = [
            choice[0]
            for choice in Application.STATUS_CHOICES
        ]

        if status not in valid_statuses:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid application status"
                },
                status=400
            )

        application = Application.objects.get(
            id=application_id,
            user=request.user
        )

        application.status = status

        if notes:
            application.notes = notes

        application.save()

        return JsonResponse({
            "success": True,
            "message": "Application status updated",
            "application": {
                "id": application.id,
                "status": application.status,
                "notes": application.notes
            }
        })

    except Application.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Application not found"},
            status=404
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )
    

def market_skills_analytics(request):

        top_skills = (
            OpportunitySkill.objects
            .values(
                "skill__name",
                "skill__category"
            )
            .annotate(
                demand_count=Count("id")
            )
            .order_by(
                "-demand_count",
                "skill__name"
            )[:10]
        )

        return JsonResponse({
            "success": True,
            "skills": [
                {
                    "name": item["skill__name"],
                    "category": item["skill__category"],
                    "demand_count": item["demand_count"]
                }
                for item in top_skills
            ]
        })