"""
03_system_and_params.py
Gemini 核心功能教學：系統指示詞與生成參數配置 (System Instructions & Generation Config)
展示如何透過角色設定、溫度與最大輸出 Token 控制回應風格
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 1. 系統指示詞（定義模型的人設、輸出規範與限制）
system_instruction = """
你是一位擁有 20 年經驗的資深 Python 架構師與精簡主義者。
規則：
1. 一律使用繁體中文回答。
2. 解釋請直切核心、條理分明，避免冗贅的客套話。
3. 程式範例必須符合現代 Python 3.10+ 的最佳實踐（型別標註、清晰命名）。
"""

# 2. 用戶提問
user_input = "在 Python 中，什麼時候該用 dataclass，什麼時候該用 Pydantic？"

print("⚙️ 系統指示詞：資深 Python 架構師 (精簡風格)")
print(f"💬 用戶提問：{user_input}\n")

# 3. 呼叫 Interactions API 並傳入參數
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    system_instruction=system_instruction,
    input=user_input,
    generation_config={
        "temperature": 0.3,          # 較低溫度適合精確、嚴謹的技術架構建議
        "max_output_tokens": 800     # 限制最大輸出長度
    }
)

print("🤖 Gemini 回覆：")
print(interaction.output_text)
