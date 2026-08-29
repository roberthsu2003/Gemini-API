import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 定義取得天氣資料的宣告
weather_function_declaration = {
    "type": "function",
    "name": "get_current_weather",
    "description": "取得指定城市的即時天氣狀況與氣溫。",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "城市名稱，例如：台北、東京、倫敦 (London)",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "溫度單位，預設為攝氏 celsius",
            },
        },
        "required": ["location"],
    },
}


# 模擬即時天氣 API
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    weather_db = {
        "台北": {"temperature": 26, "condition": "多雲時晴", "humidity": 75},
        "東京": {"temperature": 18, "condition": "晴朗", "humidity": 50},
        "倫敦": {"temperature": 14, "condition": "小雨", "humidity": 88},
    }
    data = weather_db.get(
        location, {"temperature": 22, "condition": "晴", "humidity": 60}
    )
    return {
        "location": location,
        "unit": unit,
        "temperature": data["temperature"],
        "condition": data["condition"],
        "humidity": f"{data['humidity']}%",
    }


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請問台北現在天氣如何？出門需要帶傘嗎？"

# Turn 1
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[weather_function_declaration],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"模型要求呼叫: {step.name}，參數: {step.arguments}")
        result = get_current_weather(**step.arguments)

        # Turn 2
        final_interaction = client.interactions.create(
            model="gemini-3.7-flash",
            previous_interaction_id=interaction.id,
            tools=[weather_function_declaration],
            input=[
                {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}],
                }
            ],
        )

        print("\n=== 模型最終回答 ===")
        print(final_interaction.output_text)
