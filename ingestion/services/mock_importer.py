from django.utils import timezone

from ingestion.models import JobSource, ScrapeRun, ImportedOpportunity
from opportunities.models import Company, Opportunity


MOCK_JOBS = [
    {
        "external_id": "google-se-intern-001",
        "title": "Software Engineering Intern",
        "company": "Google",
        "industry": "Technology",
        "location": "Johannesburg",
        "opportunity_type": "Internship",
        "experience_level": "Entry",
        "description": "Work with engineering teams to build scalable software products.",
        "application_url": "https://example.com/google-se-intern",
        "source_url": "https://example.com/google-se-intern",
        "salary": "Market related",
        "source": "Mock Graduate Feed",
    },
    {
        "external_id": "standardbank-data-001",
        "title": "Junior Data Analyst",
        "company": "Standard Bank",
        "industry": "Banking",
        "location": "Johannesburg",
        "opportunity_type": "Job",
        "experience_level": "Entry",
        "description": "Analyze business data and support reporting teams with insights.",
        "application_url": "https://example.com/standardbank-data",
        "source_url": "https://example.com/standardbank-data",
        "salary": "Market related",
        "source": "Mock Graduate Feed",
    },
]


def import_mock_jobs():
    source, _ = JobSource.objects.get_or_create(
        name="Mock Graduate Feed",
        defaults={
            "website": "https://example.com",
            "is_active": True,
        }
    )

    scrape_run = ScrapeRun.objects.create(
        source=source,
        status="Started"
    )

    imported_count = 0

    try:
        current_external_ids = []

        for job in MOCK_JOBS:
            current_external_ids.append(job["external_id"])

            company, _ = Company.objects.get_or_create(
                name=job["company"],
                defaults={
                    "industry": job["industry"],
                    "website": "",
                    "description": "",
                }
            )

            opportunity, _ = Opportunity.objects.update_or_create(
                title=job["title"],
                company=company,
                defaults={
                    "opportunity_type": job["opportunity_type"],
                    "experience_level": job["experience_level"],
                    "description": job["description"],
                    "location": job["location"],
                    "salary": job["salary"],
                    "application_url": job["application_url"],
                    "source": job["source"],
                    "is_active": True,
                }
            )

            ImportedOpportunity.objects.update_or_create(
                source=source,
                external_id=job["external_id"],
                defaults={
                    "opportunity": opportunity,
                    "title": job["title"],
                    "company_name": job["company"],
                    "source_url": job["source_url"],
                    "is_currently_available": True,
                }
            )

            imported_count += 1

        ImportedOpportunity.objects.filter(
            source=source
        ).exclude(
            external_id__in=current_external_ids
        ).update(
            is_currently_available=False
        )

        scrape_run.status = "Completed"
        scrape_run.jobs_found = imported_count
        scrape_run.completed_at = timezone.now()
        scrape_run.save()

        return {
            "success": True,
            "jobs_imported": imported_count
        }

    except Exception as e:
        scrape_run.status = "Failed"
        scrape_run.error_message = str(e)
        scrape_run.completed_at = timezone.now()
        scrape_run.save()

        return {
            "success": False,
            "error": str(e)
        }