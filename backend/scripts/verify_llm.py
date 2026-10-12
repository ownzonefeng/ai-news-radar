import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=30,
)
stream = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[{"role": "user", "content": "只回复OK"}],
    max_tokens=20,
    temperature=0,
    extra_body={"thinking": {"type": "disabled"}},
    stream=True,
)
parts = []
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        parts.append(chunk.choices[0].delta.content)
print("LLM_OK", "".join(parts))
