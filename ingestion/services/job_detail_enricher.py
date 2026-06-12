import requests

from bs4 import BeautifulSoup


def extract_clean_text(soup):

    for tag in soup([
        "script",
        "style",
        "nav",
        "header",
        "footer"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    text = " ".join(
        text.split()
    )

    return text


def enrich_job_description(application_url):

    response = requests.get(
        application_url,
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

    full_text = extract_clean_text(
        soup
    )

    return full_text

def enrich_capitec_job(job):
    pass

def enrich_investec_job(job):
    pass