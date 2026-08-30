"""
app_gradio.py
實務應用整合：Gradio 互動式 Web 介面
整合 Gemini 3.7 Flash Interactions API
功能：
1. 思考模式深度選擇 (minimal / low / medium / high)
2. 即時打字機串流回應 (Streaming)
3. 伺服器端狀態化多輪對話 (previous_interaction_id)
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 伺服器端維持各會話的 interaction_id
session_interaction_map = {}


def stream_chat(message: str, history: list, thinking_level: str, session_id: str):
    """多輪對話與串流回覆"""
    if not message.strip():
        return

    # 取得前一輪 interaction_id
    last_id = session_interaction_map.get(session_id)

    stream = client.interactions.create(
        model="gemini-3.7-flash",
        input=message,
        previous_interaction_id=last_id,
        generation_config={
            "thinking_level": thinking_level,
            "temperature": 1.0
        },
        system_instruction="你是一位專業的繁體中文 AI 助理，請給出條理清晰的解答。",
        stream=True
    )

    accumulated = ""
    for event in stream:
        if hasattr(event, "interaction_id") and event.interaction_id:
            session_interaction_map[session_id] = event.interaction_id
        elif hasattr(event, "id") and event.id:
            session_interaction_map[session_id] = event.id

        if event.event_type == "step.delta" and event.delta.type == "text":
            accumulated += event.delta.text
            yield accumulated


with gr.Blocks(title="Gemini 3.7 Flash AI 助理", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Gemini 3.7 Flash 互動式 Web 助理")
    gr.Markdown("展示如何將 Gemini **Interactions API** 串接至 Gradio，支援思考深度調節與伺服器端狀態對話。")

    session_id_state = gr.State(value="default_session")

    with gr.Sidebar():
        gr.Markdown("### ⚙️ 參數設定")
        thinking_radio = gr.Radio(
            choices=["minimal", "low", "medium", "high"],
            value="medium",
            label="思考模式深度 (Thinking Level)",
            info="調節 Gemini 3.7 的內部推理深度"
        )
        clear_btn = gr.Button("🗑️ 清除對話記憶")

    chatbot = gr.Chatbot(label="對話視窗", type="messages", height=550)
    msg_input = gr.Textbox(placeholder="請輸入訊息或問題，按 Enter 送出...", label="輸入訊息")

    with gr.Accordion("💡 快捷問題範例", open=False):
        gr.Examples(
            examples=[
                "請用 Python 實作一個支援過期時間 (TTL) 的記憶體快取 (Cache) 類別。",
                "請分析微服務架構 (Microservices) 與單體架構 (Monolith) 的優劣比較與遷移時機。",
                "請解釋什麼是 Retrieval-Augmented Generation (RAG) 技術？"
            ],
            inputs=msg_input
        )

    def user_submit(user_msg, chat_history):
        return "", chat_history + [{"role": "user", "content": user_msg}]

    def bot_respond(chat_history, thinking_lvl, sess_id):
        user_message = chat_history[-1]["content"]
        chat_history.append({"role": "assistant", "content": ""})
        for partial_text in stream_chat(user_message, chat_history[:-1], thinking_lvl, sess_id):
            chat_history[-1]["content"] = partial_text
            yield chat_history

    def reset_session(sess_id):
        session_interaction_map.pop(sess_id, None)
        return []

    msg_input.submit(
        user_submit, [msg_input, chatbot], [msg_input, chatbot]
    ).then(
        bot_respond, [chatbot, thinking_radio, session_id_state], chatbot
    )

    clear_btn.click(reset_session, [session_id_state], chatbot)

if __name__ == "__main__":
    demo.launch()
