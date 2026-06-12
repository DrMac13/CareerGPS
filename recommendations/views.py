from django.http import JsonResponse
from recommendations.services.matcher import generate_recommendations_for_user
from collections import Counter


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



def recommendation_analytics(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    recommendations = generate_recommendations_for_user(
        request.user
    )

    if not recommendations:
        return JsonResponse({
            "success": True,
            "analytics": {
                "total_recommendations": 0
            }
        })

    scores = [
        item["score"]
        for item in recommendations
    ]

    score_distribution = {
    "0-20": 0,
    "21-40": 0,
    "41-60": 0,
    "61-80": 0,
    "81-100": 0,
}

    for score in scores:

        if score <= 20:
            score_distribution["0-20"] += 1

        elif score <= 40:
            score_distribution["21-40"] += 1

        elif score <= 60:
            score_distribution["41-60"] += 1

        elif score <= 80:
            score_distribution["61-80"] += 1

        else:
            score_distribution["81-100"] += 1

    opportunity_types = [
        item["opportunity"].opportunity_type
        for item in recommendations
    ]

    locations = [
        item["opportunity"].location
        for item in recommendations
    ]

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    top_type = Counter(
        opportunity_types
    ).most_common(1)[0][0]

    top_location = Counter(
        locations
    ).most_common(1)[0][0]

    return JsonResponse({
        "success": True,
        "analytics": {
            "total_recommendations": len(recommendations),
            "average_match_score": average_score,
            "highest_match_score": max(scores),
            "lowest_match_score": min(scores),
            "top_opportunity_type": top_type,
            "top_location": top_location,
            "score_distribution": score_distribution,
        }
    })