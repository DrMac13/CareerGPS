from profiles.models import UserProfile, UserSkill, UserInterest
from opportunities.models import Opportunity, OpportunitySkill


def calculate_match_score(user, opportunity):
    score = 0
    reasons = []

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return 0, "No profile found"

    user_skill_ids = set(
        UserSkill.objects.filter(profile=profile)
        .values_list("skill_id", flat=True)
    )

    opportunity_skill_ids = set(
        OpportunitySkill.objects.filter(opportunity=opportunity)
        .values_list("skill_id", flat=True)
    )

    if opportunity_skill_ids:
        matched_skills = user_skill_ids.intersection(opportunity_skill_ids)

        skill_score = int(
            (len(matched_skills) / len(opportunity_skill_ids)) * 60
        )

        score += skill_score

        if matched_skills:
            reasons.append(
                f"Matched {len(matched_skills)} required skill(s)"
            )

    if profile.location and opportunity.location:
        if profile.location.lower() in opportunity.location.lower() or opportunity.location.lower() in profile.location.lower():
            score += 20
            reasons.append("Location matches your profile")

    user_interests = UserInterest.objects.filter(
        profile=profile
    ).select_related("interest")

    for user_interest in user_interests:
        interest_name = user_interest.interest.name.lower()

        if (
            interest_name in opportunity.title.lower()
            or interest_name in opportunity.description.lower()
            or interest_name in opportunity.opportunity_type.lower()
        ):
            score += 20
            reasons.append(f"Matches your interest in {user_interest.interest.name}")
            break

    score = min(score, 100)

    if not reasons:
        reasons.append("Low match based on current profile data")

    return score, " • ".join(reasons)


def generate_recommendations_for_user(user):
    active_opportunities = Opportunity.objects.filter(is_active=True)

    recommendations = []

    for opportunity in active_opportunities:
        score, reasons = calculate_match_score(user, opportunity)

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