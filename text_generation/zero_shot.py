import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Zero-shot Text Generation") as demo:
    gr.Markdown("# Zero-shot Text Generation (Interactions API)")
    
    input_text = gr.Textbox(
        label="Prompt",
        placeholder="請輸入問題...",
        submit_btn=True
    )
    with gr.Accordion("**懶得輸入可以點選以下範例問題**", open=False):
        gr.Examples(
            examples=[
                "請問台灣的首都是哪裡？",
                "請用三句話簡介人工智慧的發展歷史。",
                "請給出五個適合初學者的 Python 學習建議。"
            ],
            label="問題範例",
            inputs=input_text
        )
    output_text = gr.Markdown()

    @input_text.submit(inputs=input_text, outputs=[input_text, output_text])
    def generate_text(input_str: str):
        if not input_str.strip():
            return None, ""
        
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=input_str
        )
        return None, f"## {input_str}\n\n" + (interaction.output_text or "")

if __name__ == "__main__":
    demo.launch()