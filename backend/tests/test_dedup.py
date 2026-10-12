from app.dedup import is_duplicate_title, url_fingerprint


def test_url_fingerprint_ignores_tracking_params():
    a = url_fingerprint("https://example.com/post/?utm_source=weixin")
    b = url_fingerprint("https://www.example.com/post")
    assert a == b


def test_url_fingerprint_distinguishes_pages():
    assert url_fingerprint("https://example.com/a") != url_fingerprint("https://example.com/b")


def test_title_similarity():
    assert is_duplicate_title("OpenAI 发布 GPT-5", ["OpenAI 发布 GPT-5 模型"])
    assert not is_duplicate_title("OpenAI 发布 GPT-5", ["Anthropic 发布 Claude 4"])
