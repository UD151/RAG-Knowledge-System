import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# 数据
documents =[
"国际足联世界杯（FIFA World Cup ），简称“世界杯”，是一项国家级男子足球队之间的国际比赛，由法国人朱勒斯·雷米特于1930年发起创办，并由世界足坛最高管理机构国际足球联合会(FIFA)每4年举办一次，由国际足球联合会旗下会员协会球队参加，是世界足坛规模最大、水平最高的赛事。世界杯奖杯在1930年至1970年为“雷米特杯”，1974年后为“大力神杯”。",
"1930年第一届世界杯在乌拉圭举行，共有13个国家参赛。2026年世界杯起，决赛圈扩军至48支球队参加。",
"世界杯与奥运会并称为全球体育两大最顶级赛事，是影响力和转播覆盖率超过奥运会的全球最大体育盛事。在经历了多年的商业化演进后，世界杯作为举世瞩目的体育IP，撬动了一条从特许经营、赞助商广告、酒店机票到转播版权完整的赛事产业链，带来巨大的商业价值。"
]

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

print("模型加载完成")

#文档转换为向量
embeddings = model.encode(documents,convert_to_numpy=True)

#使用faiss创建向量索引
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

#查询
query = "世界杯有什么盈利模式？"
query_embedding = model.encode([query],convert_to_numpy=True)
distances,indices = index.search(query_embedding,k=3)
print(distances)
print(indices)