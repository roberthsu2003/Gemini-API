"""
01_pydantic_basic.py
Gemini 結構化輸出核心教學：Pydantic 基礎 Schema 資料萃取
使用 Pydantic 定義資料結構，強制模型輸出符合規範的 JSON 物件
"""

import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class Ingredient(BaseModel):
    name: str = Field(description="食材名稱")
    quantity: str = Field(description="所需份量或單位，例如 200g 或 2 顆")


class Recipe(BaseModel):
    recipe_name: str = Field(description="食譜名稱")
    cooking_time_minutes: int = Field(description="預估烹飪時間（分鐘）")
    difficulty: str = Field(description="難易度：簡單 / 中等 / 困難")
    ingredients: List[Ingredient] = Field(description="食材清單")
    steps: List[str] = Field(description="料理步驟列表")


user_request = "請提供一份正宗『義大利番茄肉醬麵（Bolognese）』的食譜，包含食材與做法。"
print(f"💬 提問：{user_request}\n")
print("🔍 正在透過 Gemini 生成結構化食譜資料...")

# 透過 response_schema 設定 Pydantic 模型
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=user_request,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Recipe,
        temperature=0.2
    )
)

print("\n✅ 結構化 JSON 輸出結果：")
print(response.text)
