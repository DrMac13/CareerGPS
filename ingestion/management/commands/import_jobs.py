from django.core.management.base import BaseCommand

from ingestion.services.mock_importer import (
    import_mock_jobs
)


class Command(BaseCommand):

    help = "Import opportunities from external feeds"

    def handle(self, *args, **kwargs):

        result = import_mock_jobs()

        if result["success"]:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported {result['jobs_imported']} jobs"
                )
            )

        else:

            self.stdout.write(
                self.style.ERROR(
                    result["error"]
                )
            )