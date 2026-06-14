from django.http import JsonResponse

from analytics.services.career_intelligence_service import (
    get_career_readiness
)


def career_readiness_api(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "error": "Authentication required"
            },
            status=401
        )

    result = get_career_readiness(
        request.user
    )

    return JsonResponse(result)