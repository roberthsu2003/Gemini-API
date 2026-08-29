import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("=== 1. 使用 Files API 上傳 PDF 文件 ===")
uploaded_file = client.files.upload(
    file="說明書.pdf",
)
print(f"檔案上傳成功: {uploaded_file.name}")
print(f"URI: {uploaded_file.uri}")

# 檢查檔案狀態
file_info = client.files.get(name=uploaded_file.name)
while file_info.state == "PROCESSING":
    print("檔案處理中，等待 2 秒...")
    time.sleep(2)
    file_info = client.files.get(name=uploaded_file.name)

if file_info.state == "FAILED":
    raise RuntimeError("檔案處理失敗")

print("\n=== 2. 第一輪提問：文件總結 ===")
interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "uri": uploaded_file.uri,
            "mime_type": uploaded_file.mime_type,
        },
        {"type": "text", "text": "這台空調機有哪些主要功能？請條列式說明。"},
    ],
)
print(interaction1.output_text)

print("\n=== 3. 第二輪追問（伺服器端維持上下文） ===")
interaction2 = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction1.id,
    input="如何設定定時開關與睡眠節電模式？",
)
print(interaction2.output_text)
