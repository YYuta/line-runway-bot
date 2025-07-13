import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

@app.get("/")
def root():
    return {"message": "LINE Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("👀 LINEから受信したデータ：", data)

    # テキストメッセージを抽出
    text = data["events"][0]["message"]["text"]

    # Runway APIを叩く（サンプルエンドポイント／あとで本物と差し替える）
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": text,
        "num_frames": 48,  # 例：2秒間の動画（24fps × 2）
        "fps": 24
    }

    response = requests.post("https://api.runwayml.com/v1/your-endpoint", json=payload, headers=headers)
    print("🎬 Runwayからのレスポンス：", response.json())

    return JSONResponse(content={"status": "Runway request sent!"})
