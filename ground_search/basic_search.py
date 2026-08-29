import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請查詢今天台灣以及全球的最新科技要聞（包含 AI 最新進展），並條列式摘要。"

print("=== 正在透過 Google Search 聯網搜尋即時資訊 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
)

print("\n=== 模型回覆 ===")
print(interaction.output_text)
