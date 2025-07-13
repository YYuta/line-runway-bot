from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# .env からトークンを読み込む方法（環境変数で管理してるなら）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.get("/")
def root():
    return {"message": "LINE Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print("✅ LINEからのリクエストを受信！")
    print(body)

    # イベントが含まれているかチェック
    if "events" not in body:
        return {"status": "no events"}

    for event in body["events"]:
        # メッセージタイプかどうか確認
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_text = event["message"]["text"]
            reply_token = event["replyToken"]

            # とりあえずオウム返ししてみる！
            reply_message = {
                "type": "text",
                "text": f"あなたはこう言いました：{user_text}"
            }

            # LINE Messaging API に返信
            headers = {
                "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "replyToken": reply_token,
                "messages": [reply_message]
            }

            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://api.line.me/v2/bot/message/reply",
                    headers=headers,
                    json=payload
                )

    return {"status": "ok"}
