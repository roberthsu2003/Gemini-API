"""
app_streamlit.py
實務應用整合：Streamlit AI 智慧管家工具儀表板
功能：結合天氣查詢、行事曆預約與資料庫寫入的對話管家
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(page_title="AI 智慧管家 (Function Calling)", page_icon="🛠️", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🛠️ Gemini 函式呼叫智慧管家 (Streamlit)")
st.caption("支援自然語言多工具自動調用與執行")


def search_hotel(location: str, budget: int) -> dict:
    """查詢飯店推薦與空房。"""
    return {"location": location, "recommendation": "台北大直萬豪酒店", "price": f"每晚 NT${budget}", "available": True}


def book_ticket(movie_name: str, seats: int) -> dict:
    """訂購電影票。"""
    return {"status": "success", "movie": movie_name, "seats_count": seats, "booking_id": "TKT-2026-7788"}


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("請輸入您的需求（如：幫我查台北預算 5000 的飯店，並訂 2 張沙丘電影票）..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini 正在分析意圖並調用工具中..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.7-flash",
                    contents=prompt + "\n（請使用繁體中文回答）",
                    config=types.GenerateContentConfig(
                        tools=[search_hotel, book_ticket],
                    ),
                )
                reply = response.text or "處理完成"
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"執行失敗：{str(e)}")
