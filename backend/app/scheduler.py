import logging
import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler

from .config import GITHUB_COLLECT_HOUR, LLM_SCAN_INTERVAL_SECONDS, NEWS_COLLECT_INTERVAL_MINUTES
from .jobs import collect_all, collect_github, process_queue

log = logging.getLogger("ai_news.scheduler")


def start_scheduler():
    sched = BackgroundScheduler(timezone="Asia/Shanghai")
    sched.add_job(collect_all, "interval", minutes=NEWS_COLLECT_INTERVAL_MINUTES,
                  id="collect_news", max_instances=1, coalesce=True)
    sched.add_job(collect_github, "cron", hour=GITHUB_COLLECT_HOUR, minute=10,
                  id="collect_github", max_instances=1, coalesce=True)
    sched.start()

    def llm_worker():
        while True:
            try:
                process_queue()
            except Exception:
                log.exception("LLM 队列处理失败")
            time.sleep(LLM_SCAN_INTERVAL_SECONDS)

    threading.Thread(target=llm_worker, daemon=True, name="llm-worker").start()
    return sched
