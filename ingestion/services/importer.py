from profiles.models import (
    Skill,
    Interest
)

from opportunities.models import (
    Company,
    Opportunity,
    OpportunitySkill
)

from ingestion.services.job_detail_enricher import (
    enrich_job_description
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


def get_matched_interests(opportunity):

    text = (
        f"{opportunity.title} "
        f"{opportunity.description} "
        f"{opportunity.opportunity_type} "
        f"{opportunity.company.industry}"
    ).lower()

    matched_interests = []

    interests = Interest.objects.all()

    for interest in interests:

        interest_name = interest.name.lower()

        if interest_name in text:
            matched_interests.append(
                interest.name
            )

    return matched_interests


def enrich_opportunity_description(opportunity):

    try:

        enriched_description = enrich_job_description(
            opportunity.application_url
        )

        if (
            enriched_description
            and len(enriched_description) > len(opportunity.description)
        ):

            opportunity.description = enriched_description
            opportunity.save()

    except Exception:
        pass


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

    enrich_opportunity_description(
        opportunity
    )

    attach_skills_to_opportunity(
        opportunity
    )

    return opportunity, created