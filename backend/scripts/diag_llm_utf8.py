import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
resp = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[
        {"role": "system", "content": "输出JSON"},
        {"role": "user", "content": '{"title": "OpenAI 发布 GPT-5", "summary": "OpenAI 今日发布 GPT-5 模型，性能显著提升。", "source": "TechCrunch"}'},
    ],
    temperature=0.2,
    max_tokens=3000,
    extra_body={"thinking": {"type": "disabled"}},
)
msg = resp.choices[0].message
content = msg.content or ""
print("content repr:", repr(content[:200]))
print("content bytes:", content.encode("utf-8")[:200])
