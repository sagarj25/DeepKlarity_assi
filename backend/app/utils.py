import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_wikipedia_url(url: str) -> bool:
    parsed = urlparse(url)
    return "wikipedia.org" in parsed.netloc


def fetch_html(url: str, timeout: int = 10) -> str:
    resp = httpx.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_wikipedia_content(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_tag = soup.find(id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Summary (first paragraph)
    content_div = soup.find(id="mw-content-text")
    summary = ""
    if content_div:
        for p in content_div.find_all("p", recursive=False):
            text = p.get_text(strip=True)
            if text:
                summary = text
                break

    # Sections (h2, h3)
    sections = []
    if content_div:
        for header in content_div.find_all(["h2", "h3"]):
            txt = header.get_text(" ", strip=True)
            if txt:
                sections.append(txt)

    # Full cleaned text for LLM
    paragraphs = []
    if content_div:
        for p in content_div.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)

    full_text = "\n".join(paragraphs)

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "full_text": full_text
    }
