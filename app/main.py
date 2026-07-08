from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.db import db_manager
from app.core.init_docs import init_local_docs

from app.api.chat import router as chat_router
from app.api.docs import router as docs_router
from app.api.sessions import router as sessions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.init_db()
    init_local_docs()
    print("系统启动完成")
    yield
    print("系统关闭")


app = FastAPI(lifespan=lifespan)

# 静态页面
app.mount("/static", StaticFiles(directory="static"), name="static")

# 路由注册
app.include_router(chat_router)
app.include_router(docs_router)
app.include_router(sessions_router)