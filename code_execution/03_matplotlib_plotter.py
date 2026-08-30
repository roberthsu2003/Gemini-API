"""
03_matplotlib_plotter.py
Gemini 程式碼執行核心教學：Matplotlib 動態資料視覺化圖表生成
模型自主在沙盒中執行 Python 程式碼並將生成的圖表輸出
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
請使用 Python 與 matplotlib 繪製一張包含正弦波 (sin) 與餘弦波 (cos) 的折線圖 (0 到 2*pi)。
請設定圖表標題、座標軸標籤、圖例與網格。
請使用繁體中文解釋程式碼邏輯。
"""

print(f"💬 提問：{prompt}\n")
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print("🤖 Gemini 程式碼執行繪圖輸出：")
print(response.text)
