import re

from selectolax.lexbor import LexborHTMLParser as HTMLParser


def _int(text: str, default: int = 0) -> int:
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else default


def parse_trending_html(html_text: str, limit: int = 25):
    tree = HTMLParser(html_text)
    items = []
    for node in tree.css("article.Box-row")[:limit]:
        link = node.css_first("h2 a")
        if link is None:
            continue
        href = (link.attributes.get("href") or "").strip()
        if not href.startswith("/"):
            continue
        desc = node.css_first("p")
        lang = node.css_first("[itemprop='programmingLanguage']")
        stars_today = 0
        for span in node.css("span"):
            text = span.text(strip=True)
            if "stars" in text and "today" in text:
                stars_today = _int(text)
                break
        items.append(
            {
                "url": "https://github.com" + href,
                "title": href.strip("/"),
                "raw_summary": desc.text(strip=True) if desc else "",
                "published_at": None,
                "source": "GitHub Trending",
                "source_type": "github_trending",
                "stars": stars_today,
                "language": lang.text(strip=True) if lang else None,
            }
        )
    return items


def collect_github_trending(client, limit: int = 25):
    resp = client.get("https://github.com/trending")
    resp.raise_for_status()
    return parse_trending_html(resp.text, limit=limit)
