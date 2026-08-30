"""
02_thinking_mode.py
Gemini 核心功能教學：思考模式與推理深度控制 (Thinking Mode)
Gemini 3 世代模型支援透過 thinking_level (minimal / low / medium / high) 調節思考深度
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

complex_prompt = """
一家公司有 A、B 兩位主管與 3 位工程師。
如果規定每個專案小組必須由 1 位主管與 2 位工程師組成，請問總共可以組成幾種不同的專案小組？
請列出完整推導與計算歷程。
"""

print(f"🧠 提問（邏輯排列組合問題）：{complex_prompt}")

# 設定 thinking_level 為 medium 進行深度推理思考
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=complex_prompt,
    generation_config={
        "thinking_level": "medium",  # 可選: "minimal", "low", "medium", "high"
        "temperature": 1.0           # 官方建議思考模式下維持預設 1.0
    }
)

print("🤖 Gemini 思考與解答結果：")
print(interaction.output_text)
