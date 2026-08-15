import gradio as gr
import os
import io
import base64
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])



with gr.Blocks() as demo:
    gr.Markdown('''
        1. 請先上傳圖片
        2. 再詢問ai對於圖片的問題
    ''')
    with gr.Row():
        image = gr.Image(type='pil')
        text_box = gr.Textbox(placeholder="請輸入對圖片的說明:",submit_btn=True)
    answer = gr.Markdown(min_height=100,container=True)

    @text_box.submit(inputs=[image, text_box],outputs=[answer,answer])
    def image_to_text(image, text_box,progress=gr.Progress()):
        if not image:
            gr.Warning("沒有圖片")
            return gr.Markdown(container=False), ""

        if text_box=="":
            gr.Warning("請輸入文字")
            return gr.Markdown(container=False), ""
        progress(0.5, desc="請稍後")

        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                {"type": "text", "text": text_box},
                {"type": "image", "data": img_b64, "mime_type": "image/jpeg"}
            ]
        )
        progress(1, desc="完成")
        return gr.Markdown(container=True), (interaction.output_text or "")
    @image.upload(outputs=[answer,answer])
    def clear_answer():
        return gr.Markdown(container=False),""





demo.launch()
