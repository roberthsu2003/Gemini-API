"""
app_gradio.py
實務應用整合：Gradio AI 藝術生圖工作台
功能：
1. 支援 Imagen 3 與長寬比例設定 (1:1, 16:9, 9:16)
2. 整合 Gemini 提示詞智慧擴寫
3. 使用 gr.Gallery 展示產出圖檔
"""

import io
import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def generate_art(prompt: str, aspect_ratio: str, auto_enhance: bool, num_images: int):
    if not prompt.strip():
        gr.Warning("請輸入提示詞！")
        return [], "請先輸入提示詞"

    final_prompt = prompt
    status_msg = f"使用原始 Prompt: {prompt}"

    # 智慧擴寫
    if auto_enhance:
        enhancer = client.interactions.create(
            model="gemini-3.7-flash",
            system_instruction="你是一位專業 AI 藝術提示詞工程師，請將用戶輸入的概念擴寫為高品質英文生圖提示詞，直接輸出英文提示詞內容即可。",
            input=prompt
        )
        final_prompt = enhancer.output_text.strip()
        status_msg = f"✨ 擴寫後的 Prompt: {final_prompt}"

    # 調用 Imagen 3
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=final_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=int(num_images),
            aspect_ratio=aspect_ratio,
            output_mime_type="image/png",
        ),
    )

    output_images = []
    for gen_image in response.generated_images:
        img = Image.open(io.BytesIO(gen_image.image.image_bytes))
        output_images.append(img)

    return output_images, status_msg


with gr.Blocks(title="Imagen 3 藝術生圖工作台", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎨 Google Imagen 3 圖像生成工作台")
    gr.Markdown("輸入創意概念，可選用 Gemini 智慧擴寫，並自訂畫幅比例與張數。")

    with gr.Row():
        with gr.Column(scale=4):
            prompt_input = gr.Textbox(
                label="生圖提示詞 (Prompt)",
                placeholder="例如：一隻在雨林中彈吉他的可愛樹懶，宮崎駿動畫風格...",
                lines=4
            )
            with gr.Row():
                ratio_select = gr.Dropdown(
                    choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
                    value="1:1",
                    label="長寬比例"
                )
                num_slider = gr.Slider(minimum=1, maximum=4, value=1, step=1, label="生成張數")
            enhance_check = gr.Checkbox(label="啟用 Gemini 提示詞智慧擴寫", value=True)
            submit_btn = gr.Button("🚀 開始生成圖片", variant="primary")

        with gr.Column(scale=6):
            gallery_output = gr.Gallery(label="生成結果畫廊", columns=2, height="auto")
            status_output = gr.Markdown(label="狀態資訊")

    submit_btn.click(
        fn=generate_art,
        inputs=[prompt_input, ratio_select, enhance_check, num_slider],
        outputs=[gallery_output, status_output]
    )

if __name__ == "__main__":
    demo.launch()
