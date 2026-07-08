import fastapi
from fastapi.responses import StreamingResponse
import uvicorn
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
load_dotenv()

app = fastapi.FastAPI()
client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

@app.get("/stream/{query}")
async def stream_llm_response(query: str):
    stream = client.chat.completions.create(
        model = "deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "你是一个编程专家"},
            {"role": "user", "content": query}
        ],
        stream =True
    )
    async def generate():
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                #yield f"data: {json.dumps({'content': chunk.choices[0].delta.content}, ensure_ascii=False)}\n\n"
            if chunk.choices[0].finish_reason:
                # yield f"data: {json.dumps({'done': True})}\n\n"

                break
    return StreamingResponse(generate(),media_type="text/event-stream")


@app.get("/hello/{name}")
async def say_hello(name:str):
    return {"message": "Hello, "+name}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)