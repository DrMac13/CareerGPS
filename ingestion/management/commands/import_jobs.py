from django.core.management.base import BaseCommand

from ingestion.services.source_manager import (
    import_all_sources
)


class Command(BaseCommand):

    help = "Import opportunities from all configured sources"

    def handle(self, *args, **options):

        self.stdout.write(
            "Starting multi-source job import..."
        )

        result = import_all_sources()

        for source in result["sources"]:

            if source["success"]:

                self.stdout.write(
                    self.style.SUCCESS(
                        (
                            f"{source['source']}: "
                            f"Found {source['found']}, "
                            f"Imported {source['imported']}, "
                            f"Skipped {source['skipped']}"
                        )
                    )
                )

            else:

                self.stdout.write(
                    self.style.ERROR(
                        (
                            f"{source['source']} failed: "
                            f"{source['error']}"
                        )
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Import finished. "
                    f"Total found: {result['total_found']}, "
                    f"Total imported: {result['total_imported']}, "
                    f"Total skipped: {result['total_skipped']}"
                )
            )
        )