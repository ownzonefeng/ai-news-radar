import logging
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import db
from .jobs import collect_all, collect_github, process_queue
from .routes import router
from .scheduler import start_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("ai_news")


def _initial_run():
    try:
        collect_all()
        collect_github()
        process_queue()
    except Exception:
        log.exception("首次采集运行失败")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_db()
    sched = start_scheduler()
    threading.Thread(target=_initial_run, daemon=True).start()
    yield
    sched.shutdown(wait=False)


app = FastAPI(title="AI News Radar", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

_static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static")
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
