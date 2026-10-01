from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
from .models import DiscoveredLink

def normalize_url(base: str, href: str) -> str | None:
    if not href or href.startswith(("mailto:", "javascript:", "tel:", "#")):
        return None
    absolute = urljoin(base, href)
    absolute, _ = urldefrag(absolute)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    return absolute

def is_allowed(url: str, allowed_hosts: list[str], prefixes: list[str]) -> bool:
    p = urlparse(url)
    return p.hostname in allowed_hosts and any(p.path.startswith(x) for x in prefixes)

def looks_like_document(url: str, extensions: list[str]) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext.lower()) for ext in extensions)

def extract_links(html: str, source_url: str, depth: int, extensions: list[str]) -> list[DiscoveredLink]:
    soup = BeautifulSoup(html, "lxml")
    results = []
    for tag in soup.find_all("a", href=True):
        url = normalize_url(source_url, tag["href"])
        if not url:
            continue
        text = " ".join(tag.get_text(" ", strip=True).split())
        results.append(DiscoveredLink(url=url, source_url=source_url, anchor_text=text, depth=depth, is_document=looks_like_document(url, extensions)))
    return results

def page_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return soup.title.get_text(" ", strip=True) if soup.title else ""

def infer_module(html: str, source_url: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    crumbs = soup.select(".breadcrumb li, nav.breadcrumb li")
    if len(crumbs) >= 2:
        values = [x.get_text(" ", strip=True) for x in crumbs]
        return values[1]
    parts = [x for x in Path(urlparse(source_url).path).parts if x not in {"/", "e-sidif"}]
    return parts[-1].replace("-", " ").title() if parts else "e-SIDIF"
