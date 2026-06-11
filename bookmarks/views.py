import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from opportunities.models import Opportunity, Bookmark


@csrf_exempt
def toggle_bookmark(request):

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

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            opportunity=opportunity
        )

        if not created:
            bookmark.delete()
            return JsonResponse({
                "success": True,
                "bookmarked": False,
                "message": "Bookmark removed"
            })

        return JsonResponse({
            "success": True,
            "bookmarked": True,
            "message": "Opportunity bookmarked"
        })

    except Opportunity.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Opportunity not found"},
            status=404
        )


def saved_opportunities(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related("opportunity", "opportunity__company")

    data = []

    for bookmark in bookmarks:
        opportunity = bookmark.opportunity

        data.append({
            "id": opportunity.id,
            "title": opportunity.title,
            "company": opportunity.company.name,
            "location": opportunity.location,
            "opportunity_type": opportunity.opportunity_type,
            "application_url": opportunity.application_url,
            "saved_at": bookmark.created_at.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse({
        "success": True,
        "saved_opportunities": data
    })