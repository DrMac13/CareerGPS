from profiles.models import (
    UserProfile,
    UserSkill
)

from opportunities.models import (
    OpportunitySkill
)


def calculate_skill_gap(user, opportunity):

    profile = UserProfile.objects.get(
        user=user
    )

    user_skill_ids = set(
        UserSkill.objects.filter(
            profile=profile
        ).values_list(
            "skill_id",
            flat=True
        )
    )

    opportunity_skills = OpportunitySkill.objects.filter(
        opportunity=opportunity
    ).select_related(
        "skill"
    )

    matched_skills = []
    missing_skills = []

    for opportunity_skill in opportunity_skills:

        if opportunity_skill.skill_id in user_skill_ids:

            matched_skills.append(
                opportunity_skill.skill.name
            )

        else:

            missing_skills.append(
                opportunity_skill.skill.name
            )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }