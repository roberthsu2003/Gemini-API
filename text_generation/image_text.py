import os
import io
import base64
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Multimodal Image & Text Analysis") as demo:
    gr.Markdown("# Multimodal Image & Text (多模態圖文問答)")
    gr.Markdown("1. 請先上傳圖片\n2. 輸入針對該圖片的提問或任務需求")
    
    with gr.Row():
        image_input = gr.Image(type="pil", label="上傳圖片")
        with gr.Column():
            text_box = gr.Textbox(
                label="提問內容",
                placeholder="例如：請詳細描述圖片中的內容，或辨識圖中的重點文字...",
                lines=4,
                submit_btn=True
            )
            quick_btns = gr.Examples(
                examples=[
                    "請詳細描述這張圖片的內容與場景。",
                    "請辨識並列出圖片中的所有主要物件。",
                    "這張圖片給人什麼樣的氛圍或感受？"
                ],
                inputs=text_box,
                label="快捷提問範例"
            )

    answer = gr.Markdown(min_height=120, label="分析結果")

    @text_box.submit(inputs=[image_input, text_box], outputs=[answer])
    def analyze_image_and_text(image, prompt, progress=gr.Progress()):
        if image is None:
            gr.Warning("請先上傳圖片！")
            return ""

        if not prompt.strip():
            gr.Warning("請輸入提問內容！")
            return ""

        progress(0.3, desc="處理圖片中...")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        progress(0.7, desc="Gemini 分析中...")
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                {"type": "text", "text": prompt + "\n（請使用繁體中文回答）"},
                {"type": "image", "data": img_b64, "mime_type": "image/jpeg"}
            ]
        )
        progress(1.0, desc="完成！")
        return interaction.output_text or ""

    @image_input.upload(outputs=[answer])
    def clear_previous_answer():
        return ""

if __name__ == "__main__":
    demo.launch()
