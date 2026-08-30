"""
02_weather_assistant.py
Gemini 函式呼叫核心教學：即時天氣查詢工具整合
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_current_weather(city: str) -> dict:
    """查詢指定城市的即時天氣狀況與氣溫。

    Args:
        city: 欲查詢的城市名稱，例如 '台北', '東京', '舊金山'
    """
    print(f"⚡ [外部 API 查詢] 正在查詢城市：{city} 的即時氣象數據...")
    # 模擬外部氣象 API 回傳
    weather_data = {
        "台北": {"temperature": 28.5, "condition": "午後陣雨", "humidity": "80%"},
        "東京": {"temperature": 22.0, "condition": "晴時多雲", "humidity": "55%"},
        "紐約": {"temperature": 18.0, "condition": "晴朗", "humidity": "45%"}
    }
    return weather_data.get(city, {"temperature": 25.0, "condition": "舒適晴天", "humidity": "60%"})


prompt = "請問台北現在天氣如何？出門需要帶傘嗎？請使用繁體中文回答。"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
    ),
)

print("🤖 Gemini 工具整合回覆：")
print(response.text)
