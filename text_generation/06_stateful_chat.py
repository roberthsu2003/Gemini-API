"""
06_stateful_chat.py
Gemini 核心功能教學：伺服器端狀態化多輪對話 (Stateful Multi-turn Conversations)
Google Interactions API 透過 previous_interaction_id 自動在 Google 伺服器端維持上下文狀態
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("💬 ===== 第一輪對話 =====")
user_msg_1 = "你好！我預計下週去日本京都旅遊 3 天，喜歡歷史古蹟與抹茶甜點。"
print(f"👤 使用者：{user_msg_1}\n")

# 第一輪：建立全新互動
interaction_1 = client.interactions.create(
    model="gemini-3.7-flash",
    input=user_msg_1
)
print("🤖 Gemini 回覆：")
print(interaction_1.output_text)
print(f"\n🔑 取得 Interaction ID: {interaction_1.id}\n")

print("💬 ===== 第二輪對話（接續上一輪對話）=====")
user_msg_2 = "針對剛才推薦的景點，請幫我規劃第 2 天的詳細時間行程表（包含早中晚餐推薦）。"
print(f"👤 使用者：{user_msg_2}\n")

# 第二輪：傳入 previous_interaction_id，模型會自動繼承前一輪的上下文記憶
interaction_2 = client.interactions.create(
    model="gemini-3.7-flash",
    input=user_msg_2,
    previous_interaction_id=interaction_1.id
)
print("🤖 Gemini 回覆：")
print(interaction_2.output_text)
print(f"\n🔑 第二輪 Interaction ID: {interaction_2.id}")
