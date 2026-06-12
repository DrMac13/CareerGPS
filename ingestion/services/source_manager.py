from ingestion.models import ImportRun

from ingestion.services.scrapers.investec_scraper import (
    scrape_investec_jobs
)

from ingestion.services.scrapers.capitec_scraper import (
    scrape_capitec_jobs
)

from ingestion.services.feed_importer import (
    import_feed
)


SOURCES = [
    {
        "name": "Investec Careers",
        "scraper": scrape_investec_jobs
    },
    {
        "name": "Capitec Careers",
        "scraper": scrape_capitec_jobs
    },
]


def import_all_sources():

    results = []

    total_found = 0
    total_imported = 0
    total_skipped = 0

    for source in SOURCES:

        source_name = source["name"]
        scraper = source["scraper"]

        try:

            jobs = scraper()

            result = import_feed(
                jobs
            )

            found_count = len(jobs)
            imported_count = result["imported_count"]
            skipped_count = result["skipped_count"]

            total_found += found_count
            total_imported += imported_count
            total_skipped += skipped_count

            ImportRun.objects.create(
                source_name=source_name,
                found_count=found_count,
                imported_count=imported_count,
                skipped_count=skipped_count,
                success=True
            )

            results.append({
                "source": source_name,
                "success": True,
                "found": found_count,
                "imported": imported_count,
                "skipped": skipped_count,
                "error": None
            })

        except Exception as e:

            error_message = str(e)

            ImportRun.objects.create(
                source_name=source_name,
                found_count=0,
                imported_count=0,
                skipped_count=0,
                success=False,
                error_message=error_message
            )

            results.append({
                "source": source_name,
                "success": False,
                "found": 0,
                "imported": 0,
                "skipped": 0,
                "error": error_message
            })

    return {
        "success": True,
        "total_found": total_found,
        "total_imported": total_imported,
        "total_skipped": total_skipped,
        "sources": results
    }