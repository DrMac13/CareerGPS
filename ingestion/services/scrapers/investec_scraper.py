import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://careers.investec.co.za"
RESULTS_URL = (
    "https://careers.investec.co.za/jobs/vacancy/find/results/"
)


def get_grid_html():

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 CareerGPSBot/1.0"
    }

    page = session.get(
        RESULTS_URL,
        headers=headers,
        timeout=15
    )

    page.raise_for_status()

    html = page.text

    match = re.search(
        r"posbrowser_gridhandler/\?pagestamp=([^']+)",
        html
    )

    if not match:
        return ""

    grid_url = urljoin(
        BASE_URL,
        "/jobs/vacancy/find/results/ajaxaction/" + match.group(0)
    )

    grid_response = session.get(
        grid_url,
        headers={
            "User-Agent": "Mozilla/5.0 CareerGPSBot/1.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": RESULTS_URL,
        },
        timeout=15
    )

    grid_response.raise_for_status()

    return grid_response.text


def scrape_investec_jobs():

    html = get_grid_html()

    soup = BeautifulSoup(
        html,
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

        if "/jobs/vacancy/" not in href:
            continue

        if "/description/" not in href:
            continue

        application_url = urljoin(
            BASE_URL,
            href
        )

        location = "South Africa"

        href_parts = href.split("/")

        for part in href_parts:

            part_lower = part.lower()

            if "sandton" in part_lower:
                location = "Sandton"

            elif "pretoria" in part_lower:
                location = "Pretoria"

            elif "cape-town" in part_lower:
                location = "Cape Town"

            elif "johannesburg" in part_lower:
                location = "Johannesburg"

        opportunity_type = "Job"

        if "graduate" in title.lower() or "navigate" in title.lower():
            opportunity_type = "Graduate Programme"

        jobs.append({
            "title": title,
            "company_name": "Investec",
            "opportunity_type": opportunity_type,
            "location": location,
            "description": (
                f"Opportunity listed on Investec Careers: {title}"
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