from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LINE Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Received from LINE:", data)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

    print("✅ main.py loaded")
