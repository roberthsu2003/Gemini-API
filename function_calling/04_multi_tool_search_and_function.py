"""
04_multi_tool_search_and_function.py
Gemini 函式呼叫核心教學：Google Search 聯網 + 自訂 Python 函式混合調用
展示模型如何根據需求自動在「自訂工具」與「聯網搜尋」之間智慧路由
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def book_restaurant(restaurant_name: str, party_size: int, time_slot: str) -> dict:
    """預訂餐廳席位。

    Args:
        restaurant_name: 餐廳名稱
        party_size: 人數
        time_slot: 預訂時間，如 '18:30'
    """
    print(f"⚡ [執行預約函式] 餐廳: {restaurant_name}, 人數: {party_size}, 時間: {time_slot}")
    return {"status": "confirmed", "reservation_id": "RES-8899", "restaurant": restaurant_name}


prompt = "請幫我聯網查詢台北信義區目前評分最高的義大利餐廳是哪一家？並幫我預訂今天晚上 19:00 兩位用餐。"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[
            book_restaurant,
            types.Tool(google_search=types.GoogleSearch()),
        ],
    ),
)

print("🤖 Gemini 混合工具智慧決策回答：")
print(response.text)
