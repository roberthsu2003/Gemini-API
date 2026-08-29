import base64
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 讀取本地說明書 PDF 檔案
pdf_path = "說明書.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# 使用 Interactions API 以 Inline Document 方式傳入
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_bytes).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {
            "type": "text",
            "text": "請簡要摘要這份使用說明書的重點，並列出三大安全注意事項與日常保養方式。",
        },
    ],
)

print("=== Gemini 3 PDF 文件視覺理解摘要 ===")
print(interaction.output_text)
