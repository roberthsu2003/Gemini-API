"""
app_streamlit.py
實務應用整合：Streamlit PDF 知識庫問答儀表板
功能：檔案上傳、重點規格萃取與 Chat 對話歷史管理
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(page_title="PDF 知識庫助理", page_icon="📄", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 中設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("📄 Gemini PDF 知識庫問答儀表板")
st.caption("支援長篇技術手冊、財報與規格書分析")

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📤 文件上傳")
    uploaded_file = st.file_uploader("上傳 PDF 文件", type=["pdf"])
    if uploaded_file is not None:
        st.session_state.pdf_bytes = uploaded_file.read()
        st.success(f"已載入：{uploaded_file.name}")
    if st.button("🗑️ 清空對話記錄"):
        st.session_state.messages = []
        st.rerun()

# 顯示對話歷史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("請輸入針對該 PDF 文件的問題..."):
    if st.session_state.pdf_bytes is None:
        st.warning("⚠️ 請先在側邊欄上傳 PDF 文件！")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Gemini 正在深入研讀文件內容..."):
                try:
                    interaction = client.interactions.create(
                        model="gemini-3.7-flash",
                        input=[
                            types.Part.from_bytes(data=st.session_state.pdf_bytes, mime_type="application/pdf"),
                            f"使用者提問：{prompt}\n請使用繁體中文，依據文件回答。"
                        ]
                    )
                    reply = interaction.output_text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"回答失敗：{str(e)}")
