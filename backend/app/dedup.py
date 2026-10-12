import hashlib
import re
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "ref", "ref_src", "ref_url", "fbclid", "gclid", "igshid", "mkt_tok", "spm",
}


def normalize_url(url: str) -> str:
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return ""
    if not parts.netloc:
        return ""
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = urlencode(
        [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
         if k.lower() not in _TRACKING_PARAMS]
    )
    path = parts.path.rstrip("/")
    return urlunsplit((parts.scheme.lower() or "https", host, path, query, ""))


def url_fingerprint(url: str) -> str:
    normalized = normalize_url(url)
    if not normalized:
        return ""
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def is_duplicate_title(title: str, existing_titles, threshold: float = 0.85) -> bool:
    t = re.sub(r"\s+", "", title).lower()
    if not t:
        return False
    for other in existing_titles:
        o = re.sub(r"\s+", "", other).lower()
        if SequenceMatcher(None, t, o).ratio() >= threshold:
            return True
    return False
