import base64
import os
from typing import List, Optional
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


# 定義從說明書或規格書中提取的結構化模型
class ProductSpec(BaseModel):
    product_name: str = Field(description="產品名稱與品牌型號")
    category: str = Field(description="產品類別，例如：壁掛式空調機")
    safety_warnings: List[str] = Field(description="重要安全警告清單")
    maintenance_tips: List[str] = Field(description="定期保養與清潔要點")
    customer_support_phone: Optional[str] = Field(
        description="客戶服務或維修聯絡電話"
    )


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open("說明書.pdf", "rb") as f:
    pdf_bytes = f.read()

prompt = "請詳細閱讀這份說明書 PDF，並將關鍵產品資訊、安全注意事項與維護重點提取為結構化資料。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_bytes).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {"type": "text", "text": prompt},
    ],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ProductSpec.model_json_schema(),
    },
)

# 使用 Pydantic 進行型別安全解析
spec = ProductSpec.model_validate_json(interaction.output_text)
print("=== 成功提取結構化產品規格 ===")
print(spec.model_dump_json(indent=2))
