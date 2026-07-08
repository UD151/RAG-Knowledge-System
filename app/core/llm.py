import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# Prompt
prompt = ChatPromptTemplate.from_template(
    "相关信息如下：{context}\n\n"
    "你是一个知识库助手，请根据所给信息严格回答问题。"
    "不要编造内容，如果没有相关信息请回答："
    "知识库中未找到相关信息。\n\n"
    "问题：{query}"
)

# LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    streaming=True,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

# LCEL chain
chain = prompt | llm