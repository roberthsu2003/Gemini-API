"""
07_stateless_chat.py
Gemini 核心功能教學：無狀態多輪對話 (Stateless Conversations)
若不使用伺服器端狀態，開發者可自行在客戶端維護對話歷史清單 (Message History) 並打包傳入
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 客戶端手動維護的對話歷史 (Message History)
conversation_history = []

def send_message_stateless(user_text: str) -> str:
    """將新訊息加入歷史紀錄，並呼叫 Gemini 生成回覆"""
    global conversation_history
    
    # 加入用戶訊息
    conversation_history.append({"role": "user", "content": user_text})
    
    # 打包完整對話歷史傳給模型
    # 在 Interactions API 中可將多輪訊息格式化或直接傳入 input
    prompt_with_history = "\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history]
    ) + "\nASSISTANT:"

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=prompt_with_history,
        system_instruction="你是一位專業的繁體中文 AI 助教。"
    )
    
    assistant_reply = interaction.output_text or ""
    # 加入助手回覆
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# 模擬多輪對話
print("💬 第一輪：")
reply1 = send_message_stateless("我想用 Python 寫一個簡易計數器類別。")
print("🤖 Gemini：", reply1[:150] + "...\n")

print("💬 第二輪（延續上一輪）：")
reply2 = send_message_stateless("請幫我在剛才的類別中加入 reset 重置功能與上限檢查。")
print("🤖 Gemini：", reply2[:150] + "...\n")
