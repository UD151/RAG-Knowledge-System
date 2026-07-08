import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from app.db.db_manager import (
    save_message_to_db,
)
from app.core.retriever import retrieve_docs
from app.core.llm import chain


router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: str


# =========================
# SSE 流式接口
# =========================
@router.post("/api/stream")
async def stream(req: ChatRequest):

    query = req.query
    session_id = req.session_id

    # 保存用户消息
    save_message_to_db(session_id, "user", query)

    # 检索
    chunks, _ = retrieve_docs(query)
    context_text = "\n".join(chunks)

    async def generator():
        full = ""

        async for chunk in chain.astream({
            "context": context_text,
            "query": query
        }):
            if chunk.content:
                full += chunk.content

                yield f"data: {json.dumps({'content': chunk.content}, ensure_ascii=False)}\n\n"

        save_message_to_db(session_id, "assistant", full)

        yield "data: [DONE]\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")