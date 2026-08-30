"""
01_basic_search.py
Gemini 聯網搜尋核心教學：Google Search Grounding 基礎接地搜尋
啟用 tools=[{"google_search": {}}] 讓模型自主聯網獲取最新即時新聞與事實資料
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請查詢並告訴我今天最新的重要國際科技新聞頭條三則（包含發生時間與簡要說明），使用繁體中文。"
print(f"💬 提問：{prompt}\n")
print("🌐 Gemini 正在自主聯網搜尋最新資料中...")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
    ),
)

print("\n🤖 Gemini 聯網搜尋回答：")
print(response.text)
