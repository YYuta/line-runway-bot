import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from generate_video import generate_video_from_prompt  # 自作モジュールを読み込み

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = FastAPI()
load_dotenv()

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    try:
        handler.handle(body.decode("utf-8"), signature)
    except Exception as e:
        print("Webhook error:", e)
        return JSONResponse(content={"message": "Error"}, status_code=400)

    return JSONResponse(content={"message": "OK"}, status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if "動画" in user_message:
        prompt = user_message.replace("動画", "").strip() or "猫が走る"  # 空なら猫にする
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="動画を生成中です…少々お待ちください🐾")
        )

        # 非同期処理で Runway API にリクエストを飛ばす
        import asyncio
        asyncio.create_task(process_video_reply(event.reply_token, prompt))

    else:
        # デフォルトの返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="申し訳ありませんが、このアカウントでは個別のお問い合わせを受け付けておりません。\n次の配信までお待ちください☺️")
        )

# 動画生成→返信を非同期に
async def process_video_reply(reply_token, prompt):
    try:
        video_url = await generate_video_from_prompt(prompt)
        if video_url:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=f"動画が生成できました！\n👉 {video_url}")
            )
        else:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text="動画生成に失敗しました…💦")
            )
    except Exception as e:
        print("Video generation error:", e)
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text="動画生成中にエラーが発生しました。時間をおいて再度お試しください。")
        )
