import json
import logging
import re

from openai import OpenAI

from . import db
from .config import LLM_API_KEY, LLM_BASE_URL, LLM_MAX_ATTEMPTS, LLM_MODEL, LLM_TIMEOUT, TOPICS

log = logging.getLogger("ai_news.llm")

SYSTEM_PROMPT = """你是一名中文科技媒体编辑。根据给定的新闻信息，输出一个严格的 JSON 对象，不要输出任何其他文字，字段如下：
- "title_zh": 中文标题，保留必要的英文专有名词，不超过 40 个字
- "summary": 中文转述，300 到 500 个字，朴实严谨，只保留事实和观点，不要华丽辞藻，不要浮夸表述，面向想快速了解内容的读者
- "topic": 从下面的话题列表中选择一个最匹配的：模型与产品发布 / 开源项目 / 研究前沿 / 行业与融资 / 工程实践 / 政策与监管
- "tags": 3 到 5 个关键词标签（字符串数组）
- "is_ai": 布尔值。只有当内容与人工智能明显无关时才设为 false；模型、产品、政策、研究、机器人、无人机、自动驾驶、AI 芯片、具身智能等及其直接应用都算相关；只要可能相关、无法确定或边界模糊，都设为 true
输出示例：{"title_zh": "OpenAI 发布 GPT-5", "summary": "……", "topic": "模型与产品发布", "tags": ["OpenAI", "GPT-5", "发布"], "is_ai": true}
"""


def _parse_json(text: str):
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _normalize_is_ai(value) -> int:
    if value is False or value == 0 or value == "0" or value == "false":
        return 0
    return 1


def process_batch(articles):
    client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY, timeout=LLM_TIMEOUT)
    for article in articles:
        payload = {
            "title": article["title"],
            "summary": (article["raw_summary"] or "")[:1500],
            "source": article["source"],
        }
        if article["language"]:
            payload["language"] = article["language"]
        try:
            stream = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                ],
                temperature=0.2,
                max_tokens=5000,
                extra_body={"thinking": {"type": "disabled"}},
                stream=True,
            )
            content_parts = []
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content_parts.append(chunk.choices[0].delta.content)
            data = _parse_json("".join(content_parts))
            if not data or not data.get("title_zh"):
                raise ValueError("LLM 返回内容无法解析")
            topic = data.get("topic")
            if topic not in TOPICS:
                topic = None
            tags = data.get("tags") or []
            if not isinstance(tags, list):
                tags = []
            db.update_result(
                article["id"],
                title_zh=str(data["title_zh"])[:80],
                summary=str(data.get("summary") or ""),
                topic=topic,
                tags=[str(t) for t in tags][:6],
                is_ai=_normalize_is_ai(data.get("is_ai")),
            )
        except Exception as exc:
            log.warning("LLM 处理失败 id=%s: %s", article["id"], exc)
            db.mark_failed(article["id"], LLM_MAX_ATTEMPTS)
