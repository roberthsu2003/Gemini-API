"""
app_streamlit.py
實務應用整合：Streamlit 互動式 Web 儀表板
整合 Gemini 3.7 Flash Interactions API
功能：
1. 側邊欄動態調整思考層級 (Thinking Level) 與 Temperature
2. st.chat_message 與 st.chat_input 構建完整對話介面
3. 伺服器端狀態化多輪對話 (previous_interaction_id)
4. 一鍵重置會話記憶

執行方式：
streamlit run text_generation/app_streamlit.py
"""

import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

# 頁面配置
st.set_page_config(
    page_title="Gemini 3.7 Flash 智慧助理",
    page_icon="✨",
    layout="wide"
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ 未偵測到 GEMINI_API_KEY，請在專案根目錄 `.env` 中設定！")
    st.stop()

client = genai.Client(api_key=api_key)

# 側邊欄設定
with st.sidebar:
    st.title("⚙️ 模型參數配置")
    model_name = st.selectbox(
        "選擇模型",
        ["gemini-3.7-flash", "gemini-3.5-flash-lite", "gemini-3.1-pro-preview"],
        index=0
    )
    thinking_level = st.select_slider(
        "思考推理深度 (Thinking Level)",
        options=["minimal", "low", "medium", "high"],
        value="medium"
    )
    temperature = st.slider("Temperature (創意度)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

    st.divider()
    if st.button("🗑️ 清空對話歷史與上下文", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_interaction_id = None
        st.rerun()

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_interaction_id" not in st.session_state:
    st.session_state.last_interaction_id = None

# 主畫面標題
st.title("✨ Gemini 3.7 Flash 智慧助理 (Streamlit 整合)")
st.caption("基於 Google 官方推薦的 Interactions API 構建，支援思考深度調節與伺服器端對話上下文管理。")

# 顯示歷史訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 接收用戶輸入
if prompt := st.chat_input("請輸入您的問題或需求..."):
    # 顯示用戶訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 呼叫 Gemini API 串流生成
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.interactions.create(
                model=model_name,
                input=prompt,
                previous_interaction_id=st.session_state.last_interaction_id,
                generation_config={
                    "thinking_level": thinking_level,
                    "temperature": temperature
                },
                system_instruction="你是一位專業的繁體中文 AI 助理，請使用排版優雅的 Markdown 給出回答。",
                stream=True
            )

            for event in stream:
                if hasattr(event, "interaction_id") and event.interaction_id:
                    st.session_state.last_interaction_id = event.interaction_id
                elif hasattr(event, "id") and event.id:
                    st.session_state.last_interaction_id = event.id

                if event.event_type == "step.delta" and event.delta.type == "text":
                    full_response += event.delta.text
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"生成失敗：{str(e)}")
