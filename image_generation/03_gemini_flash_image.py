"""
03_gemini_flash_image.py
Gemini 圖像生成核心教學：Gemini 2.5 Flash Image 多模態生圖
使用 Gemini 內建的圖像生成能力
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "一隻站在雪地上的可愛企鵝，戴著紅色毛線帽與圍巾，溫暖色調插畫風格。"
print(f"🎨 生圖提示詞：{prompt}\n")

# 使用 interactions API 或 models API
interaction = client.interactions.create(
    model="gemini-2.5-flash-image",
    input=prompt
)

if hasattr(interaction, "output_image") and interaction.output_image:
    interaction.output_image.save("penguin.png")
    print("✅ 成功透過 output_image 取得並儲存圖片：penguin.png")
else:
    print("🤖 模型回應文字：", interaction.output_text)
