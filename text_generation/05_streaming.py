"""
05_streaming.py
Gemini 核心功能教學：即時打字機串流輸出 (Streaming Responses)
使用 stream=True 啟用 SSE 事件監聽，即時在終端機印出模型生成的字詞 (Tokens)
"""

import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請寫一首關於『清晨山嵐與雲海』的優美現代散文詩（約 200 字），使用繁體中文。"
print(f"💬 提問：{prompt}\n")
print("🤖 Gemini 即時打字機串流輸出：\n" + "-" * 50)

# 設定 stream=True 取得迭代器 (Generator)
stream = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    stream=True
)

# 監聽 SSE 事件並即時輸出到終端機
for event in stream:
    if event.event_type == "step.delta" and event.delta.type == "text":
        sys.stdout.write(event.delta.text)
        sys.stdout.flush()

print("\n" + "-" * 50)
print("✅ 串流生成完畢！")
