"""
02_search_citations.py
Gemini 聯網搜尋核心教學：解析搜尋來源與引用網址 (Sources & Citations)
從 grounding_metadata 中提取搜尋查詢字詞、來源網頁標題與 URL
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "最近一週台灣有什麼重要的天文現象或天氣變化預報？請以繁體中文說明。"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
    ),
)

print("🤖 Gemini 回覆：")
print(response.text)

# 提取 Grounding 中繼資料與來源引用
print("\n" + "=" * 50)
print("🔗 引用來源與搜尋歷程 (Grounding Metadata)：")
if response.candidates and response.candidates[0].grounding_metadata:
    meta = response.candidates[0].grounding_metadata
    if meta.web_search_queries:
        print(f"🔍 搜尋查詢關鍵字：{meta.web_search_queries}")

    if meta.grounding_chunks:
        print("\n📚 參考網頁來源清單：")
        for i, chunk in enumerate(meta.grounding_chunks, 1):
            if chunk.web:
                print(f"{i}. [{chunk.web.title}]({chunk.web.uri})")
