"""
05_pdf_structured_extraction.py
Gemini 文件理解核心教學：PDF 結構化資訊萃取 (Pydantic / JSON Schema)
結合 Pydantic 從說明書中提取精確的型號、規格與故障代碼
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class ErrorCodeInfo(BaseModel):
    code: str = Field(description="故障代碼或燈號現象")
    possible_cause: str = Field(description="可能原因")
    solution: str = Field(description="建議處置方式")

class ProductManualInfo(BaseModel):
    product_name: str = Field(description="產品名稱或機型")
    maintenance_interval: str = Field(description="濾網建議保養清洗週期")
    safety_warnings: List[str] = Field(description="核心安全警告事項清單")
    troubleshooting: List[ErrorCodeInfo] = Field(description="常見故障排除代碼與處理")

pdf_path = Path(__file__).parent / "說明書.pdf"
pdf_bytes = pdf_path.read_bytes()

print("🔍 正在從 PDF 中提取結構化規格資訊...")
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "請從說明書中提取產品型號、保養週期、安全注意事項與常見故障排除資訊，一律使用繁體中文。"
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ProductManualInfo,
    )
)

print("✅ 結構化 JSON 輸出：")
print(response.text)
