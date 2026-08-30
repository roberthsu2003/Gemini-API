"""
01_meeting_scheduler.py
Gemini 函式呼叫核心教學：會議預約外部動作執行 (標準 4 步驟流程)
展示如何定義 Python 函式並交由 Gemini 決定何時調用與提取參數
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# 定義外部工具函式
def schedule_meeting(topic: str, date: str, participants_count: int) -> dict:
    """在行事曆中預約新會議。

    Args:
        topic: 會議主題
        date: 會議日期 (YYYY-MM-DD)
        participants_count: 預計參與人數
    """
    print(f"\n⚡ [本地執行 Python 函式] schedule_meeting(topic='{topic}', date='{date}', participants_count={participants_count})")
    return {
        "status": "success",
        "meeting_id": "MEET-2026-9988",
        "topic": topic,
        "date": date,
        "room": "101 會議室 (大會議廳)"
    }


# 用戶自然語言需求
user_prompt = "請幫我預約下週三 2026-09-02 的『Q4 產品策略規劃會議』，預計有 8 個人參加。"
print(f"💬 用戶請求：{user_prompt}\n")

# 步驟 1 & 2：將 Python 函式傳入 tools，Gemini 自動決定是否觸發
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[schedule_meeting],
    ),
)

print("🤖 Gemini 自動呼叫工具並完成整合回應：")
print(response.text)
