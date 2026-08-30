"""
06_pdf_context_caching.py
Gemini 文件理解核心教學：Context Caching 長篇文件快取機制
針對頻繁查詢的大型 PDF 建立伺服器端快取，節省 75% 成本並大幅降低延遲
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

pdf_path = Path(__file__).parent / "說明書.pdf"
print(f"📤 上傳 PDF 到 Files API：{pdf_path.name}...")
uploaded_file = client.files.upload(file=str(pdf_path))

# 建立 10 分鐘 TTL 的快取 (Context Cache)
print("⚡ 正在建立 Context Cache 快取...")
cache = client.caches.create(
    model="gemini-2.5-flash",  # 快取功能支援 gemini-2.5-flash 等模型
    config=types.CreateCachedContentConfig(
        contents=[uploaded_file],
        system_instruction="你是一位冷氣設備技術客服專家，所有回答必須嚴格基於說明書內容，並使用繁體中文回答。",
        ttl="600s",
    ),
)
print(f"✅ 快取建立成功！快取名稱: {cache.name}\n")

# 使用快取進行極速問答
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="請問冷氣遙控器上的除濕模式與冷氣模式在運轉機制上有何不同？",
    config=types.GenerateContentConfig(
        cached_content=cache.name,
    ),
)

print("🤖 基於快取的極速問答結果：")
print(response.text)
