import logging

import httpx

from . import db
from .config import FETCH_TIMEOUT, FETCH_USER_AGENT, RSS_SOURCES
from .dedup import is_duplicate_title, url_fingerprint
from .collectors.rss import collect_rss
from .collectors.hackernews import collect_hackernews
from .collectors.github_trending import collect_github_trending
from .llm import process_batch
from .config import LLM_BATCH_SIZE, LLM_MAX_ATTEMPTS

log = logging.getLogger("ai_news.jobs")


def insert_items(items):
    inserted = 0
    recent = db.recent_titles(days=3)
    for it in items:
        fingerprint = url_fingerprint(it["url"])
        if not fingerprint:
            continue
        if is_duplicate_title(it["title"], recent):
            continue
        if db.insert_article(it, fingerprint):
            inserted += 1
            recent.append(it["title"])
    return inserted


def collect_all():
    total_new = 0
    with httpx.Client(
        timeout=FETCH_TIMEOUT,
        headers={"User-Agent": FETCH_USER_AGENT},
        follow_redirects=True,
    ) as client:
        for name, url in RSS_SOURCES:
            try:
                total_new += insert_items(collect_rss(client, name, url))
            except Exception as exc:
                log.warning("RSS 采集失败 %s: %s", name, exc)
        try:
            total_new += insert_items(collect_hackernews(client))
        except Exception as exc:
            log.warning("Hacker News 采集失败: %s", exc)
    log.info("collect_all 新增 %s 条", total_new)
    return total_new


def collect_github():
    with httpx.Client(
        timeout=FETCH_TIMEOUT,
        headers={"User-Agent": FETCH_USER_AGENT},
        follow_redirects=True,
    ) as client:
        try:
            n = insert_items(collect_github_trending(client))
            log.info("GitHub Trending 新增 %s 条", n)
        except Exception as exc:
            log.warning("GitHub Trending 采集失败: %s", exc)


def process_queue():
    pending = db.pending_articles(LLM_BATCH_SIZE, LLM_MAX_ATTEMPTS)
    if not pending:
        return
    log.info("LLM 队列处理 %s 条", len(pending))
    process_batch(pending)
