import base64
import io
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = (
    "請使用 Python 的 Matplotlib 繪製一張包含常態分佈 (Normal Distribution) 與指數分佈 (Exponential Distribution) 的比較圖表，"
    "加入標題、圖例與格線，並執行程式碼產生圖片。"
)

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "code_execution"}],
)

for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- 產生的繪圖程式碼 ---")
        code = step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code
        print(code)
    elif step.type == "model_output":
        for block in step.content:
            if hasattr(block, "text") and block.text:
                print(block.text)
            elif hasattr(block, "image") and block.image:
                print("\n[收到回傳的圖表圖片！]")
                img_data = base64.b64decode(block.image.data)
                img = Image.open(io.BytesIO(img_data))
                img.save("generated_distribution_plot.png")
                print("圖表已成功儲存為 generated_distribution_plot.png")
