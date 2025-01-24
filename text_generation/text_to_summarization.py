import google.generativeai as genai
import os
import gradio as gr

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction = """
    你是一位文章的總結專家,也是一位繁體中文的高手。
    你的任務是:
    1. 請將內容`總結`
    2. 總結的內容口語化
    """
)

with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Text To Summarization(總結)")
    
    input_text = gr.Textbox(
        label="請輸入文章",
        lines=10,
        submit_btn=True
        )
    output_md = gr.Markdown()

    @input_text.submit(inputs=input_text, outputs=[input_text,output_md])
    def generate_text(input_str:str):
        response = model.generate_content(input_str)
        return (None, f"{input_str}\n\n### 總結內容如下:\n" + response.text)

demo.launch()