import gradio as gr
import PIL
import google.generativeai as genai
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-2.0-flash-exp")



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
            return None            
            
        if text_box=="":
            gr.Warning("請輸入文字")
            return None
        progress(0.5, desc="請稍後")
        response = model.generate_content([text_box, image])
        progress(1, desc="完成")
        return gr.Markdown(container=True),response.text
    @image.upload(outputs=[answer,answer])
    def clear_answer():
        return gr.Markdown(container=False),""
            

            
    

demo.launch()