import os
import requests

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
API_URL = "https://api.runwayml.com/v1/image_to_video"  # あとで実際のモデル名に書き換えてね

def generate_video(prompt: str):
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "prompt": prompt,
            "seed": 42  # 任意、変えてもOK
        }
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data  # 中に task_id や url が含まれてるはず
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
