"""
01_math_solver.py
Gemini 程式碼執行核心教學：數學運算與演算法求解 (Code Execution)
啟用 code_execution 工具讓模型自主在 Google 沙盒中編寫並執行 Python 程式碼，徹底避免算術幻覺
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請問第 50 個質數是多少？請使用 Python 程式碼演算並驗證，最後輸出答案（使用繁體中文）。"
print(f"💬 提問：{prompt}\n")
print("⚡ 模型正在編寫並執行 Python 程式碼中...")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print("\n🤖 Gemini 運算結果：")
print(response.text)
