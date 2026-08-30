"""
04_search_structured_output.py
Gemini 聯網搜尋核心教學：Google Search 聯網搜尋 + Pydantic 結構化資料提取
聯網獲取即時資訊並自動轉化為強型別 JSON
"""

import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class NewsArticle(BaseModel):
    headline: str = Field(description="新聞標題")
    source_media: str = Field(description="報導媒體或機構")
    summary: str = Field(description="重點摘要（約 50 字）")


class TechNewsReport(BaseModel):
    query_topic: str = Field(description="搜尋主題")
    articles: List[NewsArticle] = Field(description="新聞列表")


prompt = "請聯網搜尋今天關於『AI 人工智慧與大語言模型』的三則最新重大新聞，並以繁體中文整理為結構化報告。"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        response_mime_type="application/json",
        response_schema=TechNewsReport,
    ),
)

print("✅ 聯網結構化 JSON 輸出：")
print(response.text)
