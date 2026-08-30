"""
04_image_zoom_inspection.py
Gemini 程式碼執行核心教學：圖片局部裁切縮放與視覺程式碼檢驗
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 載入專案素材
image_path = Path(__file__).parent.parent / "text_generation" / "bear.jpg"

if not image_path.exists():
    print(f"找不到圖片 {image_path}")
    exit(1)

image = Image.open(image_path)
prompt = "請用 Python 程式碼將這張圖片中棕熊頭部區域裁切並放大 2 倍，檢查棕熊眼神與毛髮細節，使用繁體中文說明。"

print("🔍 傳入圖片並啟用程式碼執行進行視覺局部檢測...")
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=[image, prompt],
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print("🤖 Gemini 視覺檢測分析結果：")
print(response.text)
