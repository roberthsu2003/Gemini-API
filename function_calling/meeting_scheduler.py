import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 定義會議排程函式的 JSON Schema 宣告
schedule_meeting_function = {
    "type": "function",
    "name": "schedule_meeting",
    "description": "在指定的日期與時間，為指定的與會人員安排會議。",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "與會人員姓名清單，例如：['Bob', 'Alice']",
            },
            "date": {
                "type": "string",
                "description": "會議日期，格式為 YYYY-MM-DD，例如 '2025-03-14'",
            },
            "time": {
                "type": "string",
                "description": "會議時間，格式為 HH:MM，例如 '10:00'",
            },
            "topic": {"type": "string", "description": "會議主題或討論事項"},
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}


# 模擬後端會議建立函式
def schedule_meeting(attendees: list[str], date: str, time: str, topic: str) -> dict:
    print(f"\n[系統執行] 正在日曆中建立會議...")
    print(f"  主題: {topic}")
    print(f"  時間: {date} {time}")
    print(f"  與會者: {', '.join(attendees)}")
    return {
        "status": "success",
        "meeting_id": "mtg-20250314-001",
        "message": f"成功建立「{topic}」會議，已發送邀請郵件給 {len(attendees)} 位與會者。",
    }


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請幫我和 Bob、Alice 安排一場 2025-03-14 上午 10:00 的會議，討論 Q3 產品規劃。"

# Turn 1: 傳送提示詞與工具宣告給模型
print("=== Turn 1: 模型決策中 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[schedule_meeting_function],
)

# 檢查模型是否發出 function_call
fc_step = next((s for s in interaction.steps if s.type == "function_call"), None)

if fc_step:
    print(f"模型要求呼叫函式: {fc_step.name} (Call ID: {fc_step.id})")
    print(f"參數: {fc_step.arguments}")

    # 執行本地端函式
    if fc_step.name == "schedule_meeting":
        result = schedule_meeting(**fc_step.arguments)

        # Turn 2: 將函式執行結果回傳給模型
        print("\n=== Turn 2: 回傳結果給模型產生最終回覆 ===")
        final_interaction = client.interactions.create(
            model="gemini-3.7-flash",
            previous_interaction_id=interaction.id,
            tools=[schedule_meeting_function],
            input=[
                {
                    "type": "function_result",
                    "name": fc_step.name,
                    "call_id": fc_step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}],
                }
            ],
        )

        print("\n=== 最終模型回覆 ===")
        print(final_interaction.output_text)
else:
    print("模型直接回覆:", interaction.output_text)
