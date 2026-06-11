import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg, Max, Min

from .models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
    InterviewFeedback
)

from .services.question_bank import get_questions_for_role
from .services.scorer import evaluate_response


def interview_page(request):
    return render(request, "interviews/interview.html")


@csrf_exempt
def start_interview(request):

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

        role = data.get("role")

        if not role:
            return JsonResponse(
                {"success": False, "error": "Role is required"},
                status=400
            )

        session = InterviewSession.objects.create(
            user=request.user,
            role=role
        )

        questions = get_questions_for_role(role)

        created_questions = []

        for index, question_text in enumerate(questions, start=1):
            question = InterviewQuestion.objects.create(
                session=session,
                question_text=question_text,
                question_order=index
            )

            created_questions.append({
                "id": question.id,
                "question_text": question.question_text,
                "question_order": question.question_order
            })

        return JsonResponse({
            "success": True,
            "session_id": session.id,
            "role": session.role,
            "questions": created_questions
        })

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )


@csrf_exempt
def submit_response(request):

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

        session_id = data.get("session_id")
        question_id = data.get("question_id")
        response_text = data.get("response_text", "")
        duration_seconds = data.get("duration_seconds", 0)

        session = InterviewSession.objects.get(
            id=session_id,
            user=request.user
        )

        question = InterviewQuestion.objects.get(
            id=question_id,
            session=session
        )

        response = InterviewResponse.objects.create(
            session=session,
            question=question,
            response_text=response_text,
            duration_seconds=duration_seconds
        )

        evaluation = evaluate_response(
            role=session.role,
            question=question.question_text,
            response_text=response_text
        )

        feedback = InterviewFeedback.objects.create(
            response=response,
            confidence_score=evaluation["confidence_score"],
            eye_contact_score=None,
            star_score=evaluation["star_score"],
            speaking_pace=None,
            overall_score=evaluation["overall_score"],
            strengths="\n".join(evaluation["strengths"]),
            improvements="\n".join(evaluation["improvements"])
        )

        return JsonResponse({
            "success": True,
            "response_id": response.id,
            "feedback": {
                "overall_score": feedback.overall_score,
                "confidence_score": feedback.confidence_score,
                "star_score": feedback.star_score,
                "strengths": feedback.strengths,
                "improvements": feedback.improvements
            }
        })

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500
        )
    

def interview_report(request, session_id):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    try:
        session = InterviewSession.objects.get(
            id=session_id,
            user=request.user
        )

        responses = InterviewResponse.objects.filter(
            session=session
        ).select_related("question")

        if not responses.exists():
            return JsonResponse({
                "success": False,
                "error": "No responses submitted yet"
            }, status=400)

        question_results = []
        total_score = 0
        total_confidence = 0
        total_star = 0
        count = 0

        strengths = []
        improvements = []

        for response in responses:
            feedback = InterviewFeedback.objects.get(
                response=response
            )

            total_score += feedback.overall_score or 0
            total_confidence += feedback.confidence_score or 0
            total_star += feedback.star_score or 0
            count += 1

            if feedback.strengths:
                strengths.append(feedback.strengths)

            if feedback.improvements:
                improvements.append(feedback.improvements)

            question_results.append({
                "question": response.question.question_text,
                "answer": response.response_text,
                "overall_score": feedback.overall_score,
                "confidence_score": feedback.confidence_score,
                "star_score": feedback.star_score,
                "strengths": feedback.strengths,
                "improvements": feedback.improvements,
            })

        average_score = round(total_score / count, 2)
        average_confidence = round(total_confidence / count, 2)
        average_star = round(total_star / count, 2)

        session.overall_score = average_score
        session.completed_at = timezone.now()
        session.save()

        return JsonResponse({
            "success": True,
            "session_id": session.id,
            "role": session.role,
            "overall_score": average_score,
            "confidence_score": average_confidence,
            "star_score": average_star,
            "questions_answered": count,
            "question_results": question_results,
            "summary": {
                "strengths": strengths[:5],
                "improvements": improvements[:5],
            }
        })

    except InterviewSession.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Interview session not found"},
            status=404
        )
    

def interview_history(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "error": "Authentication required"},
            status=401
        )

    sessions = InterviewSession.objects.filter(
        user=request.user
    ).order_by("-started_at")

    data = []

    for session in sessions:
        responses_count = InterviewResponse.objects.filter(
            session=session
        ).count()

        data.append({
            "id": session.id,
            "role": session.role,
            "started_at": session.started_at.strftime("%Y-%m-%d %H:%M"),
            "completed_at": (
                session.completed_at.strftime("%Y-%m-%d %H:%M")
                if session.completed_at
                else None
            ),
            "overall_score": session.overall_score,
            "responses_count": responses_count,
        })

    return JsonResponse({
        "success": True,
        "history": data
    })


def interview_analytics(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False},
            status=401
        )

    sessions = InterviewSession.objects.filter(
        user=request.user,
        overall_score__isnull=False
    )

    if not sessions.exists():

        return JsonResponse({
            "success": True,
            "analytics": {
                "total_interviews": 0
            }
        })

    total_interviews = sessions.count()

    average_score = round(
        sessions.aggregate(
            Avg("overall_score")
        )["overall_score__avg"],
        2
    )

    highest_score = sessions.aggregate(
        Max("overall_score")
    )["overall_score__max"]

    lowest_score = sessions.aggregate(
        Min("overall_score")
    )["overall_score__min"]

    role_scores = {}

    for session in sessions:

        role_scores.setdefault(
            session.role,
            []
        )

        role_scores[
            session.role
        ].append(
            session.overall_score
        )

    role_averages = {}

    for role, scores in role_scores.items():

        role_averages[role] = (
            sum(scores) / len(scores)
        )

    strongest_role = max(
        role_averages,
        key=role_averages.get
    )

    weakest_role = min(
        role_averages,
        key=role_averages.get
    )

    return JsonResponse({

        "success": True,

        "analytics": {

            "total_interviews":
                total_interviews,

            "average_score":
                average_score,

            "highest_score":
                highest_score,

            "lowest_score":
                lowest_score,

            "strongest_role":
                strongest_role,

            "weakest_role":
                weakest_role,
        }
    })