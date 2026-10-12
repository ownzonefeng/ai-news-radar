import os

DB_PATH = os.getenv("DB_PATH", "/data/ai_news.db")

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:8000/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "EMPTY")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "90"))
LLM_BATCH_SIZE = int(os.getenv("LLM_BATCH_SIZE", "20"))
LLM_MAX_ATTEMPTS = int(os.getenv("LLM_MAX_ATTEMPTS", "3"))

NEWS_COLLECT_INTERVAL_MINUTES = int(os.getenv("NEWS_COLLECT_INTERVAL_MINUTES", "30"))
GITHUB_COLLECT_HOUR = int(os.getenv("GITHUB_COLLECT_HOUR", "2"))
LLM_SCAN_INTERVAL_SECONDS = int(os.getenv("LLM_SCAN_INTERVAL_SECONDS", "5"))

FETCH_TIMEOUT = float(os.getenv("FETCH_TIMEOUT", "25"))
FETCH_USER_AGENT = os.getenv(
    "FETCH_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
)

TOPICS = [
    "模型与产品发布",
    "开源项目",
    "研究前沿",
    "行业与融资",
    "工程实践",
    "政策与监管",
]

RSS_SOURCES = [
    ("机器之心", "https://www.jiqizhixin.com/rss"),
    ("量子位", "https://www.qbitai.com/feed"),
    ("AI科技评论", "https://www.leiphone.com/feed"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("人民网", "http://www.people.com.cn/rss/politics.xml"),
    ("中国新闻网", "https://www.chinanews.com.cn/rss/scroll-news.xml"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
]
