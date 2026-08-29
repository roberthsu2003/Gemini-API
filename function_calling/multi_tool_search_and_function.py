import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 自訂天氣工具
get_weather_declaration = {
    "type": "function",
    "name": "get_weather",
    "description": "取得特定地點的即時氣溫。",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市與地區名稱，例如：Utqiaġvik, Alaska",
            }
        },
        "required": ["city"],
    },
}

# 同時結合 Google 內建搜尋工具與自訂函式
tools = [{"type": "google_search"}, get_weather_declaration]

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "美國最北端的城市是哪裡？那裡今天的天氣如何？"

print("=== 正在透過 Google Search 搜尋並分析函式呼叫需求 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=tools,
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"模型要求執行自訂函式: {step.name} (ID: {step.id})")
        print(f"參數: {step.arguments}")

        # 模擬天氣查詢回傳
        weather_result = {
            "temperature": "-5°C (23°F)",
            "condition": "暴風雪注意報",
        }

        interaction_2 = client.interactions.create(
            model="gemini-3.7-flash",
            previous_interaction_id=interaction.id,
            tools=tools,
            input=[
                {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(weather_result)}],
                }
            ],
        )

        print("\n=== 模型整合聯網搜尋與天氣函式後的最終回覆 ===")
        print(interaction_2.output_text)
