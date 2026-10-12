from datetime import datetime, timezone

import feedparser

from ..textutils import strip_html


def _to_iso(struct):
    if not struct:
        return None
    try:
        dt = datetime(*struct[:6], tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def collect_rss(client, source_name: str, feed_url: str, limit: int = 30):
    resp = client.get(feed_url)
    resp.raise_for_status()
    parsed = feedparser.parse(resp.content)
    items = []
    for entry in parsed.entries[:limit]:
        link = entry.get("link")
        title = entry.get("title")
        if not link or not title:
            continue
        published = _to_iso(entry.get("published_parsed") or entry.get("updated_parsed"))
        items.append(
            {
                "url": link.strip(),
                "title": strip_html(title),
                "raw_summary": strip_html(entry.get("summary") or entry.get("description") or "")[:2000],
                "published_at": published,
                "source": source_name,
                "source_type": "rss",
            }
        )
    return items
