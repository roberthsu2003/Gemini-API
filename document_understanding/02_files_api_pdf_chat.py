"""
02_files_api_pdf_chat.py
Gemini 文件理解核心教學：Files API 上傳大型 PDF 並進行多輪對話 (最大支援 1000 頁 / 50MB)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

pdf_path = Path(__file__).parent / "說明書.pdf"
print(f"📤 上傳 PDF 到 Google Files API：{pdf_path.name}...")
uploaded_file = client.files.upload(file=str(pdf_path))
print(f"✅ 上傳成功，URI: {uploaded_file.uri}\n")

# 第一輪：針對文件提問
print("💬 第一輪提問：這台機器的濾網應該如何清潔？清洗週期是多久？")
turn_1 = client.interactions.create(
    model="gemini-3.7-flash",
    input=[uploaded_file, "這台機器的濾網應該如何清潔？清洗週期是多久？請以繁體中文回答。"]
)
print("🤖 Gemini 回覆：")
print(turn_1.output_text)

# 第二輪：延續對話
print("\n💬 第二輪提問：如果運轉時出現異常異音，可能的原因有哪些？")
turn_2 = client.interactions.create(
    model="gemini-3.7-flash",
    input="如果運轉時出現異常異音，可能的原因有哪些？",
    previous_interaction_id=turn_1.id
)
print("🤖 Gemini 回覆：")
print(turn_2.output_text)
