import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

user_concept = "雨夜中的咖啡館"

# 步驟 1: 利用 Gemini 3.7 Flash 將簡單概念擴寫為高品質圖像提示詞
print(f"=== 步驟 1: 由 Gemini 將「{user_concept}」擴寫為生圖專業 Prompt ===")
enhancer_instruction = """
你是一位頂尖的 AI 圖像提示詞工程師。
請將使用者輸入的簡短概念擴寫為一段適合 Imagen 3 生成高畫質圖片的詳細英文 Prompt（包含光影、視角、藝術風格、細節描述與氛圍），直接輸出英文提示詞即可，不要包含其他說明文字。
"""

enhance_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=user_concept,
    system_instruction=enhancer_instruction,
)
expanded_prompt = enhance_interaction.output_text.strip()
print(f"擴寫後英文 Prompt:\n「{expanded_prompt}」")

# 步驟 2: 傳入 Imagen 3 生成圖片
print("\n=== 步驟 2: 調用 Imagen 3 生成圖片 ===")
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=expanded_prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
    ),
)

for i, gen_image in enumerate(response.generated_images):
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    output_filename = "enhanced_cafe.png"
    image.save(output_filename)
    print(f"圖片生成成功並儲存為: {output_filename}")
