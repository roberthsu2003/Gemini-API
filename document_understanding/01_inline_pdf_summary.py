"""
01_inline_pdf_summary.py
Gemini 文件理解核心教學：Inline PDF 重點摘要 (小型 PDF 文件 < 20MB)
使用 Interactions API 直接傳送 PDF 二進位資料進行分析
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

pdf_path = Path(__file__).parent / "說明書.pdf"
if not pdf_path.exists():
    print("找不到說明書.pdf，請確認檔案路徑。")
    exit(1)

print(f"📄 讀取 PDF：{pdf_path.name}")
pdf_bytes = pdf_path.read_bytes()

# 調用 Interactions API 傳入 Inline PDF
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "請針對這份冷氣壁掛式說明書，用繁體中文以五個重點條列出重要的安全注意事項與日常保養方法。"
    ]
)

print("\n🤖 Gemini PDF 重點摘要結果：")
print(interaction.output_text)
