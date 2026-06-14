from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from profiles.models import UserProfile
from profiles.services.cv_extraction_service import (
    process_cv_upload
)


@csrf_exempt
def upload_cv(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "error": "Authentication required"
            },
            status=401
        )

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid request"
            },
            status=400
        )

    uploaded_file = request.FILES.get("cv_file")
    print("FILES:", request.FILES)
    print("UPLOADED FILE:", uploaded_file)

    if not uploaded_file:
        return JsonResponse(
            {
                "success": False,
                "error": "No CV file uploaded"
            },
            status=400
        )

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    result = process_cv_upload(
        profile,
        uploaded_file
    )

    return JsonResponse({
        "success": True,
        "message": "CV uploaded and processed",
        "result": result
    })