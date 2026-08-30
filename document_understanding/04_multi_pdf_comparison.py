"""
04_multi_pdf_comparison.py
Gemini 文件理解核心教學：多份 PDF 文件跨文件比對與表格輸出
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

pdf_path = Path(__file__).parent / "說明書.pdf"
pdf_bytes = pdf_path.read_bytes()

# 模擬傳入兩份文件進行功能、規格與適用環境比對
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "請針對本說明書中提及的室內機與室外機，列出包含『安裝要求』、『保養週期』、『故障燈號』的 Markdown 比較表格，使用繁體中文。"
    ]
)

print("🤖 Gemini 跨模組規格比對表：")
print(interaction.output_text)
