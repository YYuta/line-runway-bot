from fastapi import FastAPI, Request
import uvicorn
import os
import requests
from generate_video import generate_video

app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.get("/")
def root():
    return {"message": "LINE Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    # LINEからのメッセージテキスト取得
    try:
        user_message = body["events"][0]["message"]["text"]
        reply_token = body["events"][0]["replyToken"]
    except Exception as e:
        print("Invalid LINE message format:", e)
        return {"status": "error"}

    # Runway APIで動画生成
    result = generate_video(user_message)

    if result and "output" in result:
        video_url = result["output"]["url"]  # 実際のキー名はモデルによって変わる
        rep
