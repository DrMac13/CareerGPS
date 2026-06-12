import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://careers.capitecbank.co.za"

SEARCH_URL = (
    "https://careers.capitecbank.co.za/search/"
    "?q=&sortColumn=referencedate&sortDirection=desc"
)


def detect_location(title, href):

    text = f"{title} {href}".lower()

    if "stellenbosch" in text:
        return "Stellenbosch"

    if "johannesburg" in text:
        return "Johannesburg"

    if "cape-town" in text or "cape town" in text:
        return "Cape Town"

    if "sandton" in text:
        return "Sandton"

    return "South Africa"


def detect_opportunity_type(title):

    title_lower = title.lower()

    if "intern" in title_lower:
        return "Internship"

    if "graduate" in title_lower:
        return "Graduate Programme"

    if "learnership" in title_lower:
        return "Learnership"

    return "Job"


def scrape_capitec_jobs():

    response = requests.get(
        SEARCH_URL,
        headers={
            "User-Agent": "Mozilla/5.0 CareerGPSBot/1.0"
        },
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    jobs = []

    links = soup.find_all(
        "a",
        href=True
    )

    for link in links:

        title = link.get_text(
            " ",
            strip=True
        )

        href = link.get(
            "href"
        )

        if not title or not href:
            continue

        if "/job/" not in href:
            continue

        application_url = urljoin(
            BASE_URL,
            href
        )

        jobs.append({
            "title": title,
            "company_name": "Capitec",
            "opportunity_type": detect_opportunity_type(
                title
            ),
            "location": detect_location(
                title,
                href
            ),
            "description": (
                f"Opportunity listed on Capitec Careers: {title}"
            ),
            "application_url": application_url
        })

    unique_jobs = []
    seen_urls = set()

    for job in jobs:

        if job["application_url"] in seen_urls:
            continue

        seen_urls.add(
            job["application_url"]
        )

        unique_jobs.append(
            job
        )

    return unique_jobs