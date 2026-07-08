import os
from dotenv import load_dotenv

load_dotenv()

# HuggingFace 国内镜像 + SSL关闭（解决下载卡顿、证书报错）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"

class Settings:
    # LLM
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

    # 路径配置
    DOCS_DIR = "./docs"
    CHROMA_DIR = "./chroma_db"
    DB_PATH = "chat_history.db"

    # RAG 参数
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50


settings = Settings()