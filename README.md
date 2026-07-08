# RAG Knowledge System

一个基于 **FastAPI + LangChain + Chroma + DeepSeek** 的轻量级 RAG（Retrieval-Augmented Generation）知识库问答系统。

支持文档上传、向量检索、多轮会话管理以及流式回答，采用模块化架构，方便后续扩展更多文档格式和模型。

---

## 功能特性

- 文档知识库管理
  - 支持 `.txt`、`.docx` 文档上传
  - 自动文本切分
  - 自动向量化
  - 删除文档时同步清理向量数据

- RAG 检索问答
  - Chroma 向量数据库
  - m3e-base Embedding
  - Top-K 相似度检索
  - DeepSeek 大模型生成回答

- 流式输出
  - Server Sent Events (SSE)
  - 实时生成回答

- 多会话管理
  - 新建会话
  - 查看历史聊天
  - 删除会话
  - SQLite 持久化存储

- 前后端分离
  - FastAPI REST API
  - Vue3 前端页面

---

## 技术栈

### Backend

- FastAPI
- LangChain
- Chroma
- HuggingFace Embeddings
- DeepSeek API
- SQLite

### Frontend

- Vue3
- HTML
- CSS
- JavaScript

---

## 项目结构

```
RAG-Knowledge-System
│
├── app
│   ├── api                 # 所有接口
│   │     ├── chat.py
│   │     ├── docs.py
│   │     └── sessions.py
│   │
│   ├── core                # RAG核心组件
│   │     ├── llm.py
│   │     └── vectorstore.py
│   │
│   ├── db                  # SQLite操作
│   │     └── db_manager.py
│   │
│   ├── services            # 文档处理
│   │     ├── doc_loader.py
│   │     └── init_docs.py
│   │
│   └── main.py
│
├── docs                    # 本地知识库
├── chroma_db               # 向量数据库
├── static                  # 前端页面
├── chat_history.db
├── experiments             # 历史代码
└── requirements.txt
```

---

## 工作流程

```
上传文档
      │
      ▼
读取文本
      │
      ▼
文本切分
      │
      ▼
Embedding
      │
      ▼
Chroma向量库
      │
      ▼
用户提问
      │
      ▼
相似度检索
      │
      ▼
Prompt构建
      │
      ▼
DeepSeek
      │
      ▼
流式返回答案
```

---

## 安装

### 克隆项目

```bash
git clone https://github.com/UD151/RAG-Knowledge-System.git

cd RAG-Knowledge-System
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

项目根目录下新建 `.env`

```
DEEPSEEK_API_KEY= "your_api_key"

DEEPSEEK_BASE_URL= "https://api.deepseek.com"
```
也可以使用其他支持OpenAI API 格式的模型

### 启动

```bash
uvicorn app.main:app --reload
```

浏览器访问

```
http://127.0.0.1:8000/static/index.html
```

---

## 支持的文档格式

目前支持：

- txt
- docx

> 注：旧版 `.doc` 文件请先转换为 `.docx` 后再上传。

---

## 主要功能展示

- 新建聊天会话
- 历史会话管理
- 文档上传
- 文档删除
- 自动向量化
- RAG 检索
- 流式回答
- SQLite 持久化

---

## 后续计划

- [ ] PDF 文档支持
- [ ] Markdown 文档支持
- [ ] 历史对话上下文增强
- [ ] 多模型切换
- [ ] 联网搜索
- [ ] Docker 部署

---
## 开发历史
`experiments/` 目录保留了开发过程中使用的原型与验证脚本——基于 FAISS + m3e 的早期 RAG 原型

## License

MIT
