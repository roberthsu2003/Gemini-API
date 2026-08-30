"""
04_multimodal_image.py
Gemini 核心功能教學：多模態圖文輸入與視覺分析 (Multimodal Understanding)
展示如何將本地圖片檔案 (PIL Image / Base64) 搭配文字提問傳入 Interactions API
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 取得目錄下的範例圖片
current_dir = Path(__file__).parent
image_path = current_dir / "bear.jpg"

if not image_path.exists():
    print(f"⚠️ 找不到範例圖片 {image_path}，請確認檔案路徑。")
    exit(1)

# 使用 PIL 載入圖片
image = Image.open(image_path)
prompt = "請詳細描述這張圖片的內容、動物特徵以及周圍的環境生態，請以繁體中文回答。"

print(f"🖼️ 載入圖片：{image_path.name}")
print(f"💬 提問：{prompt}\n")

# Interactions API 支援將 PIL Image 與字串放入 input 清單中
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[prompt, image]
)

print("🤖 Gemini 視覺分析結果：")
print(interaction.output_text)
