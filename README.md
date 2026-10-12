# AI News Radar (AI 新闻雷达)

> **AI-assisted / Codex-assisted project**: This project was developed with the assistance of [Codex](https://openai.com/codex), OpenAI's coding agent. Code generation, refactoring, deployment automation, and documentation were produced collaboratively with the agent under human direction.

定时抓取国内外主流 AI 媒体与 GitHub Trending，调用 OpenAI 兼容的 LLM 接口生成中文标题、摘要与话题分类，Web 端按话题和时间浏览。

线上地址：<https://info.azcore.top>

## 功能

- **多源采集**：机器之心、量子位、AI科技评论、人民网、中国新闻网、TechCrunch AI、VentureBeat AI、The Verge、Ars Technica、MIT Technology Review（RSS）+ Hacker News Algolia API + GitHub Trending（HTML 解析）。
- **LLM 处理管线**：每条新闻经 LLM 生成中文摘要（300-500 字，朴实严谨风格）与话题分类，URL 指纹 + 标题相似度双重去重。
- **AI 相关性过滤**：LLM 二分类判定新闻与人工智能（含机器人、无人机等衍生领域）的相关性，明显无关的内容在前端隐藏，数据仍保留在库中以便复核。
- **话题浏览**：模型与产品发布 / 开源项目 / 研究前沿 / 行业与融资 / 工程实践 / 政策与监管，支持时间范围与来源筛选。
- **持久化与幂等**：LLM 处理结果全部落库（status 字段跟踪 0=待处理 / 1=完成 / 2=失败），失败自动重试，避免重复调用浪费 token。
- **访客统计**：MySQL 持久化的累计访客计数，页面顶部显示“你是该网站第 N 位访客”。
- **深浅双主题**：React + Tailwind CSS 构建的前端，跟随系统或手动切换。

## 架构

```
浏览器 ──HTTPS 443──> ai-news 容器 (FastAPI + uvicorn + TLS)
                        ├── /api/*        REST API
                        ├── /*           React 静态产物
                        ├── APScheduler  定时任务
                        │     ├── 新闻抓取（每 30 分钟）
                        │     ├── GitHub Trending（每日 02:10）
                        │     └── LLM 队列（每 5 分钟）
                        └── MySQL 5.7 容器（数据卷持久化）
                                └── one-api 容器（LLM 中转，宿主机网络）
```

| 层 | 技术 |
|---|---|
| 后端 | Python 3.11 · FastAPI · APScheduler · httpx · feedparser · selectolax · PyMySQL |
| 数据库 | MySQL 5.7（utf8mb4），数据卷挂载宿主机磁盘 |
| 前端 | React 18 · Vite · Tailwind CSS · lucide-react |
| 部署 | Docker Compose 单机，端口 443，Let's Encrypt 证书（acme.sh 自动续期） |
| LLM | OpenAI 兼容接口，关闭 thinking 模式，`max_tokens=5000` |

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/news` | 新闻列表，支持 `topic` / `days` / `source` / `page` / `page_size` |
| GET | `/api/topics` | 话题计数，支持 `days` |
| GET | `/api/sources` | 来源列表 |
| GET | `/api/meta` | 最近一次采集时间（北京时间 UTC+8） |
| POST | `/api/visit` | 访客计数递增 |
| GET | `/api/health` | 健康检查 |

## 服务器部署

```bash
ssh ubuntu@124.220.172.20
cd /opt/ai-news

# 填写 LLM 接口配置（OpenAI 兼容格式，文件权限 600，不入 git）
cp .env.example .env
vim .env

docker compose up -d --build
```

`.env` 存放 `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`，仅存在于服务器本地，git 忽略。

## 测试

```bash
docker compose run --rm --entrypoint "" ai-news \
  sh -c "pip install -q pytest && python -m pytest backend/tests -q"
```

覆盖：URL 去重、RSS 解析、GitHub Trending HTML 解析、话题分类。

## 安全

- 所有密钥（LLM API key、SSH 私钥）只存在于服务器 `.env`（权限 600）或本地工作区，均被 `.gitignore` 排除，不会进入仓库历史。
- 数据库凭据通过容器环境变量注入，不硬编码。
- 仓库中不包含任何真实 API key。
