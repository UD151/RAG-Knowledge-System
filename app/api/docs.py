import os
import shutil
import time

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config.settings import settings
from app.core.vectorstore import vectorstore, splitter
from app.services.doc_loader import load_document

router = APIRouter(prefix="/api/docs")


ALLOWED = (".txt", ".docx")


# ========================
# 文档列表
# ========================
@router.get("")
def list_docs():
    if not os.path.exists(settings.DOCS_DIR):
        return []

    files = []

    for f in os.listdir(settings.DOCS_DIR):
        if not f.lower().endswith(ALLOWED):
            continue

        path = os.path.join(settings.DOCS_DIR, f)
        stat = os.stat(path)

        files.append({
            "name": f,
            "size_kb": round(stat.st_size / 1024, 2),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
        })

    return files


# ========================
# 上传
# ========================
@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(ALLOWED):
        raise HTTPException(400, "仅支持 txt / docx")

    path = os.path.join(settings.DOCS_DIR, file.filename)

    os.makedirs(settings.DOCS_DIR, exist_ok=True)

    # 保存文件
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file.file.close()

    # 如果已存在，删除旧向量
    vectorstore._collection.delete(where={"source": path})

    docs = load_document(path)

    for d in docs:
        d.metadata["source"] = path

    chunks = splitter.split_documents(docs)
    vectorstore.add_documents(chunks)

    return {
        "msg": "ok",
        "chunks": len(chunks)
    }


# ========================
# 删除文档
# ========================
@router.delete("/{filename}")
def delete_doc(filename: str):

    path = os.path.join(settings.DOCS_DIR, filename)

    if os.path.exists(path):
        os.remove(path)

    # 清理向量
    collection = vectorstore._collection
    data = collection.get(include=["metadatas"])

    ids = [
        doc_id
        for doc_id, meta in zip(data["ids"], data["metadatas"])
        if meta.get("source", "").endswith(filename)
    ]

    if ids:
        collection.delete(ids=ids)

    return {"msg": "deleted"}