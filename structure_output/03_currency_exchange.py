"""
03_currency_exchange.py
Gemini 結構化輸出核心教學：將非結構化匯率文字轉為精確數據清單
"""

import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class ExchangeRate(BaseModel):
    currency_code: str = Field(description="幣別代碼，例如 USD, JPY, EUR")
    currency_name: str = Field(description="幣別中文名稱")
    cash_buying: float = Field(description="本行現金買入匯率")
    cash_selling: float = Field(description="本行現金賣出匯率")


class ExchangeRateTable(BaseModel):
    date: str = Field(description="牌告匯率日期")
    rates: List[ExchangeRate] = Field(description="所有幣別匯率清單")


raw_text = """
臺灣銀行牌告匯率 查詢日期：2025/01/29
美金 (USD) 現金買入：32.45000 現金賣出：33.12000
日圓 (JPY) 現金買入：0.20800 現金賣出：0.21800
歐元 (EUR) 現金買入：33.80000 現金賣出：35.10000
"""

print("📄 原始文字內容：\n", raw_text)

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=[raw_text, "請將上述牌告匯率文字精確萃取為結構化資料。"],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ExchangeRateTable,
    )
)

print("✅ 結構化表格 JSON 輸出：")
print(response.text)
