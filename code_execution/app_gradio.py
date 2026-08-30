"""
app_gradio.py
實務應用整合：Gradio Python 運算與繪圖沙盒工作台
功能：輸入數學/運算任務，自動編寫並執行 Python，展示程式碼與輸出文字
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def execute_code_query(prompt: str):
    if not prompt.strip():
        return "請輸入問題！"

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt + "\n（請使用 Python 程式碼執行，一律使用繁體中文解釋）",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution())],
        ),
    )

    return response.text or "運算完成"


with gr.Blocks(title="Python 沙盒運算工作台", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⚡ Gemini Python 程式碼執行沙盒 (Code Execution)")
    gr.Markdown("模型自主編寫並在安全沙盒中執行 Python 程式碼，解決數學、演算法、統計與字串處理任務。")

    with gr.Row():
        prompt_in = gr.Textbox(
            label="運算或問題描述",
            placeholder="例如：請計算 1 到 1000 之間所有同時能被 3 與 7 整除的數字總和...",
            lines=3
        )

    run_btn = gr.Button("🚀 執行 Python 沙盒運算", variant="primary")
    result_out = gr.Markdown(label="運算過程與解答")

    run_btn.click(fn=execute_code_query, inputs=[prompt_in], outputs=[result_out])

if __name__ == "__main__":
    demo.launch()
