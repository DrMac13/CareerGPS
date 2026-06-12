from django.core.management.base import BaseCommand

from ingestion.services.scrapers.investec_scraper import (
    scrape_investec_jobs
)

from ingestion.services.feed_importer import (
    import_feed
)


class Command(BaseCommand):

    help = "Import real opportunities into CareerGPS"

    def handle(self, *args, **options):

        self.stdout.write(
            "Starting Investec job import..."
        )

        try:

            jobs = scrape_investec_jobs()

            result = import_feed(
                jobs
            )

            self.stdout.write(
                self.style.SUCCESS(
                    (
                        "Investec import complete. "
                        f"Found: {len(jobs)}, "
                        f"Imported: {result['imported_count']}, "
                        f"Skipped: {result['skipped_count']}"
                    )
                )
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"Import failed: {str(e)}"
                )
            )