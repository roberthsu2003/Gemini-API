"""
02_currency_calculator.py
Gemini 程式碼執行核心教學：載入 CSV 數據進行 Python 換匯試算
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

csv_path = Path(__file__).parent / "2025_01_29.csv"
csv_content = csv_path.read_text(encoding="utf-8")

prompt = f"""
以下是 2025/01/29 的牌告匯率 CSV 內容：
```csv
{csv_content}
```

請使用 Python 程式碼讀取上述數據，計算以下問題：
我有 50,000 元新台幣 (TWD)，如果想要換成日圓 (JPY) 現金，依照『本行賣出』匯率可以換得多少日圓？
請附上 Python 執行運算歷程與最終結論，一律使用繁體中文。
"""

print("📊 傳入匯率 CSV 進行 Python 沙盒精確運算...\n")
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print("🤖 Gemini 程式碼執行試算結果：")
print(response.text)
