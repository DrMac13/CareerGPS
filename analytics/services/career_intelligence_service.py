from django.db.models import Count, Avg

from profiles.models import (
    UserProfile,
    UserSkill
)

from opportunities.models import (
    OpportunitySkill,
    Opportunity
)


def calculate_profile_completion(profile, user_skills):

    checks = [
        bool(profile.institution),
        bool(profile.degree_program),
        bool(profile.location),
        bool(profile.bio),
        user_skills.exists(),
    ]

    return int(
        sum(checks) / len(checks) * 100
    )


def get_user_skill_names(profile):

    return set(
        UserSkill.objects.filter(
            profile=profile
        ).select_related(
            "skill"
        ).values_list(
            "skill__name",
            flat=True
        )
    )


def get_market_skills():

    return list(
        OpportunitySkill.objects
        .values(
            "skill__name",
            "skill__category"
        )
        .annotate(
            market_count=Count("id")
        )
        .order_by(
            "-market_count",
            "skill__name"
        )[:10]
    )


def calculate_recommendation_strength(user):

    opportunities = Opportunity.objects.filter(
        is_active=True
    )

    if not opportunities.exists():
        return 0

    # Temporary baseline until we connect this directly
    # to the recommendation scoring service.
    return 50


def get_career_readiness(user):

    try:
        profile = UserProfile.objects.select_related(
            "institution",
            "degree_program"
        ).get(
            user=user
        )

    except UserProfile.DoesNotExist:
        return {
            "success": True,
            "readiness_score": 0,
            "career_direction": "Not enough profile data",
            "skills_you_have": [],
            "missing_high_impact_skills": [],
            "recommended_next_skill": None,
            "profile_completion": 0,
            "skill_coverage": 0,
            "recommendation_strength": 0,
        }

    user_skills = UserSkill.objects.filter(
        profile=profile
    ).select_related(
        "skill"
    )

    profile_completion = calculate_profile_completion(
        profile,
        user_skills
    )

    user_skill_names = get_user_skill_names(
        profile
    )

    market_skills = get_market_skills()

    skills_you_have = []
    missing_high_impact_skills = []

    for item in market_skills:

        skill_name = item["skill__name"]

        skill_data = {
            "name": skill_name,
            "category": item["skill__category"],
            "market_count": item["market_count"]
        }

        if skill_name in user_skill_names:
            skills_you_have.append(skill_data)

        else:
            missing_high_impact_skills.append({
                **skill_data,
                "reason": (
                    "This skill appears frequently across imported "
                    "opportunities and can improve your career readiness."
                )
            })

    if market_skills:
        skill_coverage = int(
            len(skills_you_have) / len(market_skills) * 100
        )
    else:
        skill_coverage = 0

    recommendation_strength = calculate_recommendation_strength(
        user
    )

    readiness_score = int(
        (skill_coverage * 0.40) +
        (recommendation_strength * 0.35) +
        (profile_completion * 0.25)
    )

    career_direction = "General Career Readiness"

    if profile.degree_program:
        career_direction = profile.degree_program.name

    recommended_next_skill = (
        missing_high_impact_skills[0]
        if missing_high_impact_skills
        else None
    )

    return {
        "success": True,
        "readiness_score": readiness_score,
        "career_direction": career_direction,
        "skills_you_have": skills_you_have,
        "missing_high_impact_skills": missing_high_impact_skills,
        "recommended_next_skill": recommended_next_skill,
        "profile_completion": profile_completion,
        "skill_coverage": skill_coverage,
        "recommendation_strength": recommendation_strength,
    }