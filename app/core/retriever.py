from app.core.vectorstore import vectorstore


def retrieve_docs(query: str, k: int = 3):
    docs = vectorstore.similarity_search(query, k=k)
    chunks = [d.page_content for d in docs]
    return chunks, docs