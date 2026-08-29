import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "一隻穿著太空衣的可愛橘貓漂浮在浩瀚星空中，身旁有發光的星雲與星球，8k 超高畫質電影感寫實風格。"

print("=== 正在使用 Imagen 3 (imagen-3.0-generate-002) 生成高品質圖片 ===")
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="1:1",
        output_mime_type="image/png",
    ),
)

for i, gen_image in enumerate(response.generated_images):
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    output_filename = f"space_cat_{i+1}.png"
    image.save(output_filename)
    print(f"圖片已儲存為: {output_filename}")
