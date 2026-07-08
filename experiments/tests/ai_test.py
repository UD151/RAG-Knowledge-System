from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_response(query):
    prompt = f"请根据以下文档回答问题：{documents}\n问题：{query}"
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "你是一个专业的知识库问答助手。严格回答问题，不知道就回答不知道。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

documents = "国际足联世界杯（FIFA World Cup ），简称“世界杯”，是一项国家级男子足球队之间的国际比赛，由法国人朱勒斯·雷米特于1930年发起创办，并由世界足坛最高管理机构国际足球联合会(FIFA)每4年举办一次，由国际足球联合会旗下会员协会球队参加，是世界足坛规模最大、水平最高的赛事。世界杯奖杯在1930年至1970年为“雷米特杯”，1974年后为“大力神杯”。"
query = "世界杯奖杯叫什么？"

answer = generate_response(query)
print(answer)
