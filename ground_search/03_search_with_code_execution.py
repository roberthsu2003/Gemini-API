"""
03_search_with_code_execution.py
Gemini 聯網搜尋核心教學：Google Search 聯網搜尋 + Python 程式碼執行混合工具
先聯網獲取最新即時數據，再由 Python 沙盒精確運算，徹底避免數值幻覺
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請查詢目前台積電 (TSMC, 2330.TW) 與輝達 (NVIDIA, NVDA) 的最新股價，並用 Python 計算如果各買進 10 股，總共需要多少新台幣（假設匯率 1 USD = 32.5 TWD）？"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(google_search=types.GoogleSearch()),
            types.Tool(code_execution=types.ToolCodeExecution()),
        ],
    ),
)

print("🤖 Gemini 混合工具運算回答：")
print(response.text)
