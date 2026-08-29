import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "2024 年奧運男子百米金牌得主是誰？成績是多少？請提供出處與相關新聞來源。"

print("=== 正在透過 Google Search 進行事實查核與來源溯源 ===")
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
)

print("\n=== 回答內容 ===")
print(interaction.output_text)

print("\n=== 搜尋歷程與參考來源 (Search Steps & Grounding) ===")
for i, step in enumerate(interaction.steps, 1):
    print(f"\n[步驟 {i}] 類型: {step.type}")
    # 檢查是否有搜尋呼叫或網頁檢索資訊
    if hasattr(step, "grounding_metadata") and step.grounding_metadata:
        print("Grounding Metadata:", step.grounding_metadata)
    elif hasattr(step, "arguments") and step.arguments:
        print("引數資訊:", step.arguments)
