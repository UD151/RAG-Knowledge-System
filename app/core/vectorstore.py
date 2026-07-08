from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import settings

# Embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name="moka-ai/m3e-base",
    cache_folder="./local_m3e_model"
)

# 向量库
vectorstore = Chroma(
    persist_directory=settings.CHROMA_DIR,
    embedding_function=embeddings
)

# 文本切分器
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP
)