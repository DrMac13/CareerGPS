import csv

from ingestion.services.importer import import_opportunity


def import_opportunities_from_csv(file_path):

    imported_count = 0
    skipped_count = 0
    errors = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):

            try:
                title = row.get("title")
                company_name = row.get("company_name")
                opportunity_type = row.get("opportunity_type")
                location = row.get("location")
                description = row.get("description")
                application_url = row.get("application_url")

                if not all([
                    title,
                    company_name,
                    opportunity_type,
                    location,
                    description,
                    application_url
                ]):
                    skipped_count += 1
                    errors.append(
                        f"Row {row_number}: Missing required fields"
                    )
                    continue

                opportunity, created = import_opportunity(
                    title=title,
                    company_name=company_name,
                    opportunity_type=opportunity_type,
                    location=location,
                    description=description,
                    application_url=application_url
                )

                if created:
                    imported_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                skipped_count += 1
                errors.append(
                    f"Row {row_number}: {str(e)}"
                )

    return {
        "imported_count": imported_count,
        "skipped_count": skipped_count,
        "errors": errors
    }