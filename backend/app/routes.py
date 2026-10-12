from fastapi import APIRouter, Query

from . import db

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/news")
def get_news(
    topic: str | None = None,
    days: int | None = Query(default=7, ge=1, le=365),
    source: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=60, ge=1, le=200),
):
    items, total = db.query_news(
        topic=None if topic == "全部" else topic,
        days=days,
        source=source or None,
        page=page,
        page_size=page_size,
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/topics")
def get_topics(days: int | None = Query(default=7, ge=1, le=365)):
    return db.topic_counts(days)


@router.get("/sources")
def get_sources():
    return {"sources": db.sources()}


@router.get("/meta")
def get_meta():
    return db.meta()


@router.get("/visit")
def visit():
    return {"visitors": db.increment_visitors()}
