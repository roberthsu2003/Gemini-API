import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "一隻站在木樁上的翠鳥，背景是波光粼粼的水面，微距攝影，羽毛細節清晰可辨。"

print("=== 使用 gemini-2.5-flash-image 多模態圖像生成 ===")
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        image = Image.open(io.BytesIO(part.inline_data.data))
        output_filename = "kingfisher_gemini.png"
        image.save(output_filename)
        print(f"多模態生成圖片已儲存為: {output_filename}")
