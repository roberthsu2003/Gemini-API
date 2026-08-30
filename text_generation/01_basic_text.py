"""
01_basic_text.py
Gemini 核心功能教學：基礎文字生成 (Zero-shot)
使用 Interactions API (client.interactions.create)
"""

import os
from dotenv import load_dotenv
from google import genai

# 載入環境變數中的 GEMINI_API_KEY
load_dotenv()

# 初始化 Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 準備提示詞 (Prompt)
prompt = "請用繁體中文以三點簡要說明什麼是 AI Agent（人工智慧代理）？"
print(f"💬 提問：{prompt}\n")

# 調用 Interactions API 進行單輪文字生成
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt
)

# 使用便利屬性 output_text 取得模型最終輸出文字
print("🤖 Gemini 回覆：")
print(interaction.output_text)
print("-" * 50)
print(f"📊 互動 ID: {interaction.id}")
