import os
from typing import List, Optional
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


class StockInfo(BaseModel):
    company_name: str = Field(description="公司名稱")
    stock_symbol: str = Field(description="股票代號")
    current_price: float = Field(description="最新股價 (USD)")
    price_change: str = Field(description="今日漲跌幅")
    recent_key_news: List[str] = Field(description="近期 2~3 則關鍵新聞摘要")


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請搜尋 Apple (AAPL) 的最新即時股價與今日重要財經要聞，並整理為結構化資料。"

print("=== 正在聯網搜尋並提取為型別安全的 Pydantic 結構化資料 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": StockInfo.model_json_schema(),
    },
)

stock = StockInfo.model_validate_json(interaction.output_text)
print(stock.model_dump_json(indent=2))
