from app.collectors.rss import collect_rss


class FakeResponse:
    content = (
        b"<?xml version='1.0'?><rss version='2.0'><channel><title>t</title>"
        b"<item><title>Hello &amp; AI</title><link>https://example.com/a</link>"
        b"<description>&lt;p&gt;body&lt;/p&gt;</description>"
        b"<pubDate>Tue, 01 Jul 2025 08:00:00 GMT</pubDate></item>"
        b"</channel></rss>"
    )

    def raise_for_status(self):
        pass


class FakeClient:
    def get(self, url):
        return FakeResponse()


def test_collect_rss():
    items = collect_rss(FakeClient(), "test", "https://example.com/feed")
    assert len(items) == 1
    assert items[0]["title"] == "Hello & AI"
    assert items[0]["raw_summary"] == "body"
    assert items[0]["published_at"] == "2025-07-01T08:00:00Z"
