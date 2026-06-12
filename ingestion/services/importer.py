from profiles.models import Skill
from opportunities.models import (
    Company,
    Opportunity,
    OpportunitySkill
)


def attach_skills_to_opportunity(opportunity):

    text = (
        f"{opportunity.title} "
        f"{opportunity.description}"
    ).lower()

    matched_count = 0

    skills = Skill.objects.all()

    for skill in skills:

        skill_name = skill.name.lower()

        if skill_name in text:

            _, created = OpportunitySkill.objects.get_or_create(
                opportunity=opportunity,
                skill=skill
            )

            if created:
                matched_count += 1

    return matched_count


def import_opportunity(
    title,
    company_name,
    opportunity_type,
    location,
    description,
    application_url
):

    company, _ = Company.objects.get_or_create(
        name=company_name,
        defaults={
            "industry": "Unknown"
        }
    )

    opportunity, created = Opportunity.objects.get_or_create(
        title=title,
        company=company,
        defaults={
            "opportunity_type": opportunity_type,
            "experience_level": "Entry",
            "description": description,
            "location": location,
            "application_url": application_url,
            "source": "CareerGPS Import",
            "is_active": True,
        }
    )

    attached_skills = attach_skills_to_opportunity(
        opportunity
    )

    return opportunity, created