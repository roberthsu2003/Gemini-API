"""
app_gradio.py
實務應用整合：Gradio 智慧家庭與工具調用控制台
功能：整合天氣查詢、智慧設備開關等多工具自動路由與回覆
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

logs = []


def query_flight_info(flight_number: str) -> dict:
    """查詢航班最新狀態。"""
    return {"flight": flight_number, "status": "準點 On Time", "gate": "B7", "departure": "14:20"}


def control_air_conditioner(temp: int, mode: str) -> dict:
    """設定冷氣溫度與模式。"""
    return {"status": "success", "temperature": f"{temp}°C", "mode": mode}


def execute_agent_chat(message: str):
    if not message.strip():
        return "請輸入指令！"

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=message + "\n（請使用繁體中文親切說明執行的結果）",
        config=types.GenerateContentConfig(
            tools=[query_flight_info, control_air_conditioner],
        ),
    )

    return response.text or "執行完畢"


with gr.Blocks(title="Function Calling 智慧控制台", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛠️ Gemini 函式呼叫與工具自動路由 (Function Calling)")
    gr.Markdown("輸入自然語言指令，Gemini 自動識別意圖、提取結構化參數並調用對應的 Python 函式。")

    with gr.Row():
        cmd_input = gr.Textbox(
            label="請輸入您的需求或指令",
            placeholder="例如：請幫我查詢長榮 BR198 航班的最新動態，並將客廳冷氣設定為 25 度冷氣模式...",
            lines=3
        )

    exec_btn = gr.Button("🚀 送出指令", variant="primary")
    reply_output = gr.Markdown(label="Gemini 執行結果與回覆")

    exec_btn.click(fn=execute_agent_chat, inputs=[cmd_input], outputs=[reply_output])

if __name__ == "__main__":
    demo.launch()
