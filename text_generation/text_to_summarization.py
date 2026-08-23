import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Text Summarization & Style Control") as demo:
    gr.Markdown("# Text To Summarization (文章總結與風格控制)")
    
    with gr.Row():
        style_radio = gr.Radio(
            ['學術', '商業', '專業', '口語化', '條列式'],
            label='風格設定',
            info="請選擇文章總結的語氣與風格",
            value='口語化'
        )
        temp_slider = gr.Slider(
            minimum=0.0,
            maximum=2.0,
            value=0.7,
            step=0.1,
            label="Temperature (創意度)",
            info="較低值更穩定精確，較高值更具創意"
        )

    input_text = gr.Textbox(
        label="請輸入文章內容",
        placeholder="貼上或輸入欲總結的長篇文章...",
        lines=8,
        submit_btn=True
    )
    output_md = gr.Markdown()

    @input_text.submit(inputs=[style_radio, temp_slider, input_text], outputs=[output_md])
    def generate_text(style: str, temperature: float, input_str: str):
        if not input_str.strip():
            gr.Warning("請輸入文章內容！")
            return ""

        style_prompts = {
            "口語化": "請使用輕鬆自然、通俗易懂的口語化風格。",
            "學術": "請使用嚴謹、精準且具學術分析感的語調。",
            "商業": "請使用精簡幹練、聚焦商業價值與行動建議的風格。",
            "專業": "請使用清晰、客觀且條理分明的專業語氣。",
            "條列式": "請將核心重點以結構化條列方式列出。"
        }
        style_guide = style_prompts.get(style, f"請使用{style}風格。")

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            system_instruction=f"""
            你是一位專業的文章總結專家，也是繁體中文的語言高手。
            請遵守以下規則：
            1. 將輸入的內容進行重點總結。
            2. 風格要求：{style_guide}
            3. 一律使用繁體中文輸出。
            """,
            input=input_str,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 1024
            }
        )

        return f"**【風格：{style}｜Temperature：{temperature}】**\n\n### 總結內容：\n" + (interaction.output_text or "")

if __name__ == "__main__":
    demo.launch()