from django.http import JsonResponse
from recommendations.services.matcher import generate_recommendations_for_user


def user_recommendations(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    recommendations = generate_recommendations_for_user(request.user)

    data = []

    for item in recommendations:
        opportunity = item["opportunity"]

        data.append({
            "id": opportunity.id,
            "title": opportunity.title,
            "company": opportunity.company.name,
            "location": opportunity.location,
            "opportunity_type": opportunity.opportunity_type,
            "experience_level": opportunity.experience_level,
            "application_url": opportunity.application_url,
            "match_score": item["score"],
            "reasons": item["reasons"],
        })

    return JsonResponse({
        "success": True,
        "recommendations": data
    })