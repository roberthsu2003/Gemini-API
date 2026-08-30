"""
03_remote_pdf_analysis.py
Gemini 文件理解核心教學：遠端 URL PDF 下載與研讀
從網路下載公開論文或報告，直接交由 Gemini 進行深度解析
"""

import io
import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 範例：Google Attention Is All You Need 論文
pdf_url = "https://arxiv.org/pdf/1706.03762"
print(f"🌐 從遠端下載 PDF：{pdf_url} ...")

try:
    resp = requests.get(pdf_url, timeout=30)
    pdf_bytes = resp.content
    print(f"✅ 下載完成，檔案大小：{len(pdf_bytes) / 1024:.2f} KB\n")

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            "請閱讀這篇論文，以繁體中文總結：1. 核心創新機制（Transformer 架構） 2. 相比 RNN / CNN 的具體優勢 3. 在機器翻譯任務上的主要成果。"
        ]
    )

    print("🤖 Gemini 論文研讀報告：")
    print(interaction.output_text)

except Exception as e:
    print(f"❌ 遠端下載或分析失敗：{e}")
