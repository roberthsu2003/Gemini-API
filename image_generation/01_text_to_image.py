"""
01_text_to_image.py
Gemini 圖像生成核心教學：Imagen 3 基礎文字生成圖片 (Text-to-Image)
使用 imagen-3.0-generate-002 模型生成高品質圖片
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "一隻穿著太空衣的可愛橘貓漂浮在浩瀚星空中，身旁有發光的星雲與星球，8k 超高畫質電影感寫實風格。"
print(f"🎨 生圖提示詞：{prompt}\n")

# 調用 Imagen 3 模型
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="1:1",
        output_mime_type="image/png",
    ),
)

# 儲存並輸出圖片
output_filename = "space_cat.png"
for gen_image in response.generated_images:
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save(output_filename)
    print(f"✅ 圖片生成成功，已儲存至：{output_filename}")
