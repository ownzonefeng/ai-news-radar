_AI_KEYWORDS = (
    "ai", "llm", "gpt", "machine learning", "deep learning", "neural",
    "openai", "anthropic", "transformer", "diffusion", "generative",
    "chatbot", "agent", "rag", "embedding",
)


def collect_hackernews(client, limit: int = 80):
    resp = client.get(
        "https://hn.algolia.com/api/v1/search_by_date",
        params={"query": "AI", "tags": "story", "hitsPerPage": limit,
                "numericFilters": "points>10"},
    )
    resp.raise_for_status()
    hits = resp.json().get("hits", [])
    items = []
    for h in hits:
        title = h.get("title")
        if not title:
            continue
        lowered = title.lower()
        if not any(k in lowered for k in _AI_KEYWORDS):
            continue
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        items.append(
            {
                "url": url,
                "title": title,
                "raw_summary": (h.get("story_text") or "")[:2000],
                "published_at": h.get("created_at"),
                "source": "Hacker News",
                "source_type": "hackernews",
                "stars": h.get("points"),
            }
        )
    return items
