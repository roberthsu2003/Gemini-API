import base64
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 模擬載入兩份不同的 PDF（此處示範可載入兩份不同本地文件或 Files API URI）
pdf_path = "說明書.pdf"
with open(pdf_path, "rb") as f:
    pdf_data_1 = f.read()

# 透過 Interactions API 一次傳入多個 document part
prompt = (
    "這是一份產品說明書。請分析其中的「安全注意事項」與「日常保養清潔」兩個章節，"
    "將兩者的核心要求、操作禁忌與建議頻率整理為一張清楚的 Markdown 比較表格。"
)

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_data_1).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {"type": "text", "text": prompt},
    ],
)

print("=== 跨章節/跨文件比較輸出 ===")
print(interaction.output_text)
