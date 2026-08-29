import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("=== 1. 上傳大型 PDF 並建立 Context Cache ===")
uploaded_doc = client.files.upload(file="說明書.pdf")

# 建立快取（預設保留時間為 1 小時，可省下高達 75% 的 Token 費用）
cache = client.caches.create(
    model="gemini-3.7-flash",
    config=types.CreateCachedContentConfig(
        system_instruction="你是一位專業的家電工程顧問與說明書專家。",
        contents=[uploaded_doc],
        ttl="3600s",
    ),
)
print(f"快取建立成功！快取名稱: {cache.name}")
print(f"快取過期時間: {cache.expire_time}")

print("\n=== 2. 使用快取進行第一次查詢 ===")
response1 = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="這台機器在什麼情況下必須立即停止運轉並拔掉電源？",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print(response1.text)
if response1.usage_metadata:
    print(f"\n[Token 統計] 快取命中 Token 數: {response1.usage_metadata.cached_content_token_count}")
    print(f"[Token 統計] 本次計費輸入 Token 數: {response1.usage_metadata.prompt_token_count}")

print("\n=== 3. 使用快取進行第二次查詢 ===")
response2 = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="如何正確清洗空氣過濾網與更換除臭網？",
    config=types.GenerateContentConfig(cached_content=cache.name),
)
print(response2.text)
