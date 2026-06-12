from opportunities.models import Company, Opportunity


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

    return opportunity, created