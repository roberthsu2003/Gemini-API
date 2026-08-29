import base64
import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 下載範例樂器圖片或使用本機圖片
image_url = "https://goo.gle/instrument-img"
image_bytes = requests.get(image_url).content
b64_image = base64.b64encode(image_bytes).decode("utf-8")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請放大並檢查這張管風琴下方的踏板 (Expression pedals)，數數看一共有幾個踏板？請編寫並執行 Python 程式碼進行局部裁剪與檢驗。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {"type": "image", "data": b64_image, "mime_type": "image/jpeg"},
        {"type": "text", "text": prompt},
    ],
    tools=[{"type": "code_execution"}],
)

print("=== Gemini 3 圖片 Code Execution 縮放分析 ===")
for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- [模型自主編寫的影像處理程式碼] ---")
        code = step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code
        print(code)
    elif step.type == "code_execution_result":
        print("\n--- [影像處理執行結果] ---")
        print(step.result)

print("\n=== 模型最終視覺分析答案 ===")
print(interaction.output_text)
