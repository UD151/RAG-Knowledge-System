from openai import OpenAI
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
load_dotenv()
# 数据
documents =[
"国际足联世界杯（FIFA World Cup ），简称“世界杯”，是一项国家级男子足球队之间的国际比赛，由法国人朱勒斯·雷米特于1930年发起创办，并由世界足坛最高管理机构国际足球联合会(FIFA)每4年举办一次，由国际足球联合会旗下会员协会球队参加，是世界足坛规模最大、水平最高的赛事。世界杯奖杯在1930年至1970年为“雷米特杯”，1974年后为“大力神杯”。",
"1930年第一届世界杯在乌拉圭举行，共有13个国家参赛。2026年世界杯起，决赛圈扩军至48支球队参加。",
"世界杯与奥运会并称为全球体育两大最顶级赛事，是影响力和转播覆盖率超过奥运会的全球最大体育盛事。在经历了多年的商业化演进后，世界杯作为举世瞩目的体育IP，撬动了一条从特许经营、赞助商广告、酒店机票到转播版权完整的赛事产业链，带来巨大的商业价值。"
]

# 初始化向量模型和LLM客户端
def init_model():
    global model,client
    #加载M3E模型 先检查本地是否存在
    local_model_path = "local_m3e_model"
    if os.path.exists(local_model_path):
        print(f"加载本地模型: {local_model_path}")
        model = SentenceTransformer(local_model_path)
    else:
        print(f"本地模型不存在，从Hugging Face下载...")
        model = SentenceTransformer("moka-ai/m3e-base")
        print(f"模型下载完成，保存到: {local_model_path}")
        model.save_pretrained(local_model_path)
    
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

# 初始化索引
def init_index(documents_embedding):
    global index
    #使用faiss创建向量索引 先检查本地是否存在
    local_index_path = "local_index"
    if os.path.exists(local_index_path):
        print(f"加载本地索引: {local_index_path}")
        index = faiss.read_index(local_index_path)
    else:
        print(f"本地索引不存在，创建新的索引...")
        index = faiss.IndexFlatL2(documents_embedding.shape[1])
        index.add(documents_embedding)
        print(f"索引创建完成，保存到: {local_index_path}")
        faiss.write_index(index,local_index_path)


# 获取向量(支持文档或字符串)
def get_embedding(text):
    if isinstance(text,list):
        return model.encode(text,convert_to_numpy=True)
    else:
        return model.encode([text],convert_to_numpy=True)

# 请求LLM
def generate_response(context,query):
    prompt = f"请根据以下内容回答问题：{context}\n问题：{query}"
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "你是一个专业的知识库问答助手。严格回答问题，不知道就回答不知道。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    init_model()
    init_index(get_embedding(documents))

    query = "世界杯奖杯叫什么？"
    query_embedding = get_embedding(query)
    distances,indices = index.search(query_embedding,k=3)
    # indices: [[2 1 0]]
    context = documents[indices[0][0]]
    print("context:"+str(context))
    answer = generate_response(context,query)
    return answer

if __name__ == "__main__":
    answer = main()
    print(answer)