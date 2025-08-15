from google import genai
import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Zero-shot Text Generation")
    
    input_text = gr.Textbox(
        label="prompt",
        placeholder="請輸入問題",
        submit_btn=True
        )
    with gr.Accordion("**懶的輸入可以點選以下問題**",open=False):
        gr.Examples(
            examples=["請問台灣的首都是哪裡？", "請問台灣的國土面積有多大？", "請問台灣的人口有多少？"], 
            label="問題範例",
            inputs=input_text)
    output_text = gr.Markdown()

    @input_text.submit(inputs=input_text, outputs=[input_text,output_text])
    def generate_text(input_str:str):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=input_str
        )
        return (None, f"## {input_str}\n" + response.text)

demo.launch()