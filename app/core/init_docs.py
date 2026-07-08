import os

from langchain_core.documents import Document as LangchainDoc

from app.config.settings import settings
from app.core.vectorstore import vectorstore, splitter
from app.services.doc_loader import load_document


ALLOWED_EXTENSIONS = (".txt", ".docx")


def init_local_docs():
    docs_dir = settings.DOCS_DIR

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print("docs 目录已创建")
        return

    # 避免重复加载
    if vectorstore._collection.count() > 0:
        print("向量库已有数据，跳过初始化")
        return

    all_docs = []

    for root, _, files in os.walk(docs_dir):
        for filename in files:

            if not filename.lower().endswith(ALLOWED_EXTENSIONS):
                continue

            file_path = os.path.join(root, filename)

            docs = load_document(file_path)

            for d in docs:
                d.metadata["source"] = file_path

            all_docs.extend(docs)

            print("加载:", filename)

    if not all_docs:
        print("没有文档")
        return

    chunks = splitter.split_documents(all_docs)
    vectorstore.add_documents(chunks)

    print(f"初始化完成 chunks={len(chunks)}")