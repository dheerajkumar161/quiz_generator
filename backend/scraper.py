import requests
from bs4 import BeautifulSoup
import re

def scrape_wikipedia(url):
    resp = requests.get(url)
    if not resp.ok:
        raise ValueError("Unable to fetch the article.")

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("h1", {"id": "firstHeading"}).text.strip() if soup.find("h1", {"id": "firstHeading"}) else "Wikipedia Article"
    content_div = soup.find("div", {"id": "mw-content-text"})
    if content_div is None:
        raise ValueError("Could not parse Wikipedia content.")

    # Remove tables, references, spans, images, lists, etc.
    for el in content_div.find_all(["table", "sup", "span", "img", "ul", "ol", "nav", "style", "script"], recursive=True):
        try:
            el.decompose()
        except Exception:
            pass
    text = content_div.get_text(separator="\n", strip=True)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\n+', '\n', text)

    # Summary (first 2 paragraphs only)
    paragraphs = content_div.find_all("p", recursive=False)
    summary = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()][:2]).replace('\n', ' ')
    # Section names
    sections = [h.text.strip() for h in content_div.find_all(["h2", "h3", "h4", "h5"])]

    return {
        "title": title,
        "text": text.strip(),
        "sections": sections,
        "summary": summary,
        "raw_html": resp.text
    }
