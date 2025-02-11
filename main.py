from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests as rq
from models import init_db


# будет синхронизировать нашу БД, срабатывается при запуске приложения
@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Bot is ready")
    yield


app = FastAPI(title="To Do App")

# вызываются до обработки каког-то события
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)


@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_tasks_count = await rq.get_completed_tasks_count(user.id)
    return {"completedTasks": completed_tasks_count}
