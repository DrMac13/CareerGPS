from profiles.models import (
    UserProfile,
    UserSkill,
    UserInterest
)

from opportunities.models import (
    Opportunity,
    OpportunitySkill,
    Application
)

from interviews.models import InterviewSession


def calculate_match_score(user, opportunity):

    score = 0
    reasons = []

    try:
        profile = UserProfile.objects.get(user=user)

    except UserProfile.DoesNotExist:

        return 0, "No profile found"


    user_skill_ids = set(
        UserSkill.objects.filter(
            profile=profile
        ).values_list(
            "skill_id",
            flat=True
        )
    )

    opportunity_skill_ids = set(
        OpportunitySkill.objects.filter(
            opportunity=opportunity
        ).values_list(
            "skill_id",
            flat=True
        )
    )

    if opportunity_skill_ids:

        matched_skills = user_skill_ids.intersection(
            opportunity_skill_ids
        )

        skill_score = int(
            (
                len(matched_skills) /
                len(opportunity_skill_ids)
            ) * 50
        )

        score += skill_score

        if matched_skills:

            reasons.append(
                f"Matched {len(matched_skills)} required skill(s)"
            )



    user_interests = UserInterest.objects.filter(
        profile=profile
    ).select_related(
        "interest"
    )

    for user_interest in user_interests:

        interest_name = user_interest.interest.name.lower()

        if (
            interest_name in opportunity.title.lower()
            or interest_name in opportunity.description.lower()
            or interest_name in opportunity.opportunity_type.lower()
            or interest_name in opportunity.company.industry.lower()
        ):

            score += 20

            reasons.append(
                f"Matches your interest in {user_interest.interest.name}"
            )

            break



    if profile.location and opportunity.location:

        profile_location = profile.location.lower()
        opportunity_location = opportunity.location.lower()

        if (
            profile_location in opportunity_location
            or opportunity_location in profile_location
            or "remote" in opportunity_location
        ):

            score += 10

            reasons.append(
                "Location matches your profile"
            )


    if opportunity.experience_level == "Entry":

        score += 10

        reasons.append(
            "Suitable for entry-level candidates"
        )

    elif opportunity.experience_level == "Junior":

        score += 7

        reasons.append(
            "Suitable for junior-level candidates"
        )


    has_applied_to_company = Application.objects.filter(
        user=user,
        opportunity__company=opportunity.company
    ).exists()

    if has_applied_to_company:

        score += 5

        reasons.append(
            f"You have previously shown interest in {opportunity.company.name}"
        )


    best_interview = InterviewSession.objects.filter(
        user=user,
        overall_score__isnull=False
    ).order_by(
        "-overall_score"
    ).first()

    if best_interview and best_interview.overall_score >= 70:

        score += 5

        reasons.append(
            "Strong interview performance improves your match"
        )


    score = min(
        score,
        100
    )

    if not reasons:

        reasons.append(
            "Low match based on current profile data"
        )

    recommendation_summary = []

    if score >= 80:

        recommendation_summary.append(
            "Excellent match for your profile"
        )

    elif score >= 60:

        recommendation_summary.append(
            "Strong match for your profile"
        )

    elif score >= 40:

        recommendation_summary.append(
            "Moderate match for your profile"
        )

    else:

        recommendation_summary.append(
            "Potential opportunity worth exploring"
        )

    recommendation_summary.extend(
        reasons
    )

    return score, " • ".join(
        recommendation_summary
    )


def generate_recommendations_for_user(user):

    active_opportunities = Opportunity.objects.filter(
        is_active=True
    ).select_related(
        "company"
    )

    recommendations = []

    for opportunity in active_opportunities:

        score, reasons = calculate_match_score(
            user,
            opportunity
        )

        if score > 0:

            recommendations.append({
                "opportunity": opportunity,
                "score": score,
                "reasons": reasons
            })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations