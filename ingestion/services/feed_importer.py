from ingestion.services.importer import (
    import_opportunity
)


def import_feed(feed_data):

    imported_count = 0
    skipped_count = 0

    for item in feed_data:

        _, created = import_opportunity(

            title=item["title"],

            company_name=item["company_name"],

            opportunity_type=item["opportunity_type"],

            location=item["location"],

            description=item["description"],

            application_url=item["application_url"]
        )

        if created:
            imported_count += 1
        else:
            skipped_count += 1

    return {
        "imported_count": imported_count,
        "skipped_count": skipped_count
    }