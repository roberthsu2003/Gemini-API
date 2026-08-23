import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Streaming Text Summarization") as demo:
    gr.Markdown("# Text Streaming Summarization (即時串流總結)")
    
    style_radio = gr.Radio(
        ['口語化', '條列式', '學術', '商業', '專業'],
        label='風格選擇',
        info="請選擇欲生成的風格",
        value='口語化'
    )
    input_text = gr.Textbox(
        label="請輸入文章內容",
        placeholder="貼上或輸入欲總結的長篇文章...",
        lines=8,
        submit_btn=True
    )
    output_md = gr.Markdown(label="即時產出")

    @input_text.submit(inputs=[style_radio, input_text], outputs=[output_md])
    def generate_streaming_text(style: str, input_str: str):
        if not input_str.strip():
            gr.Warning("請輸入內容！")
            return

        stream = client.interactions.create(
            model="gemini-3.7-flash",
            system_instruction=f"""
            你是一位文章總結專家，請將使用者輸入的內容進行【{style}】風格的重點總結，並一律使用繁體中文。
            """,
            input=input_str,
            stream=True
        )

        result_text = ""
        header = f"**【風格：{style}（串流生成中...）】**\n\n### 總結內容：\n"
        for event in stream:
            if event.event_type == "step.delta" and event.delta.type == "text":
                result_text += event.delta.text
                yield header + result_text

if __name__ == "__main__":
    demo.launch()
