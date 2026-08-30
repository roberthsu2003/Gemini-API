"""
04_prompt_enhancer.py
Gemini 圖像生成核心教學：Gemini 擴寫提示詞 ➔ Imagen 3 智慧生圖工作流
展示如何利用 LLM 的創意能力擴寫 Prompt，自動傳給 Imagen 3 生成高畫質藝術作品
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

user_idea = "一間在雨林深處的未來樹屋實驗室"
print(f"💡 使用者原始概念：{user_idea}\n")

# 步驟 1：使用 Gemini 3.7 Flash 進行提示詞擴寫
print("🪄 步驟 1：Gemini 智慧擴寫中...")
enhance_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    system_instruction="你是一位頂尖的 AI 藝術指導。請將使用者的簡短概念擴寫為一段英文生圖 Prompt（包含光影、視角、材質、氛圍細節），只輸出最終 Prompt 本身。",
    input=user_idea
)

enhanced_prompt = enhance_interaction.output_text.strip()
print(f"✨ 擴寫後的專業 Prompt：\n{enhanced_prompt}\n")

# 步驟 2：調用 Imagen 3 生成圖片
print("🎨 步驟 2：調用 Imagen 3 生成圖片...")
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=enhanced_prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        output_mime_type="image/jpeg",
    ),
)

output_filename = "enhanced_treehouse.jpg"
for gen_image in response.generated_images:
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save(output_filename)
    print(f"✅ 圖片生成成功，已儲存至：{output_filename}")
