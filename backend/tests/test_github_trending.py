from app.collectors.github_trending import parse_trending_html

HTML = """
<main>
<article class="Box-row">
  <h2 class="h3 lh-condensed"><a href="/openai/codex">openai / codex</a></h2>
  <p class="col-9">Lightweight coding agent that runs in your terminal.</p>
  <span itemprop="programmingLanguage">Python</span>
  <span class="d-inline-block float-sm-right">1,234 stars today</span>
</article>
</main>
"""


def test_parse_trending_html():
    items = parse_trending_html(HTML)
    assert len(items) == 1
    item = items[0]
    assert item["url"] == "https://github.com/openai/codex"
    assert item["title"] == "openai/codex"
    assert item["language"] == "Python"
    assert item["stars"] == 1234
