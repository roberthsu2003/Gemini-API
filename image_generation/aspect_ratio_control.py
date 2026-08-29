import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "未來科技城市的賽博龐克夜景，飛行汽車在霓虹大樓之間穿梭，雨夜倒影，超寬螢幕電影感畫面。"

# 支援的長寬比例: "1:1", "3:4", "4:3", "9:16", "16:9"
aspect_ratio = "16:9"

print(f"=== 正在生成比例為 {aspect_ratio} 的寬螢幕圖片 ===")
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio=aspect_ratio,
        output_mime_type="image/jpeg",
    ),
)

for i, gen_image in enumerate(response.generated_images):
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    output_filename = f"cyberpunk_city_16_9.jpg"
    image.save(output_filename)
    print(f"圖片已儲存為: {output_filename} (尺寸: {image.size})")
