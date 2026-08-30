"""
02_aspect_ratio.py
Gemini 圖像生成核心教學：長寬比例與格式控制 (Aspect Ratio Control)
支援 1:1, 16:9, 9:16, 4:3, 3:4 多元比例輸出
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "未來科技城市的賽博龐克夜景，飛行汽車在霓虹大樓之間穿梭，雨夜倒影，超寬螢幕電影感畫面。"
ratio = "16:9"
print(f"🎨 生圖提示詞：{prompt}")
print(f"📐 設定長寬比：{ratio}\n")

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio=ratio,
        output_mime_type="image/jpeg",
    ),
)

output_filename = "cyberpunk_city_16_9.jpg"
for gen_image in response.generated_images:
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save(output_filename)
    print(f"✅ 圖片生成成功，已儲存至：{output_filename}")
