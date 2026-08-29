import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = (
    "請搜尋 2024 年全球票房前 3 名的電影名稱與票房數字（美元），"
    "然後編寫並執行 Python 程式碼，計算它們的總票房以及若換算為新台幣（以 1:32.5 匯率計算）是多少億元。"
)

print("=== 正在結合 Google Search 搜尋即時數據 + Python 程式碼精準運算 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[
        {"type": "google_search"},
        {"type": "code_execution"},
    ],
)

print("\n=== 最終結果 ===")
print(interaction.output_text)
