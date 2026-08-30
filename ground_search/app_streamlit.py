"""
app_streamlit.py
實務應用整合：Streamlit 即時情報與聯網搜尋儀表板
功能：動態開關聯網搜尋、即時事實查核與來源清單卡片
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(page_title="即時聯網情報儀表板", page_icon="🌐", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🌐 Gemini Google Search 聯網情報儀表板")
st.caption("即時突破知識庫截止時間限制，取得最新真實世界數據")

with st.sidebar:
    st.header("⚙️ 搜尋配置")
    enable_grounding = st.toggle("啟用 Google Search 聯網接地", value=True)
    enable_code = st.toggle("啟用 Python 運算沙盒 (混合模式)", value=False)

query = st.text_input("輸入您欲查詢的時事或問題：", value="請查詢目前美國聯準會最新公佈的利率決策與市場反應。")

if st.button("🚀 執行搜尋分析", type="primary"):
    with st.spinner("Gemini 正在搜尋最新網路資訊並彙整..."):
        tools = []
        if enable_grounding:
            tools.append(types.Tool(google_search=types.GoogleSearch()))
        if enable_code:
            tools.append(types.Tool(code_execution=types.ToolCodeExecution()))

        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=query + "\n（請使用繁體中文回答）",
                config=types.GenerateContentConfig(tools=tools if tools else None),
            )

            col1, col2 = st.columns([7, 3])
            with col1:
                st.markdown("### 🤖 彙整分析")
                st.markdown(response.text)

            with col2:
                st.markdown("### 📚 引用來源 (Citations)")
                if response.candidates and response.candidates[0].grounding_metadata:
                    meta = response.candidates[0].grounding_metadata
                    if meta.grounding_chunks:
                        for idx, chunk in enumerate(meta.grounding_chunks, 1):
                            if chunk.web:
                                st.markdown(f"**{idx}. [{chunk.web.title}]({chunk.web.uri})**")
                    else:
                        st.info("模型利用內部知識庫回答，未觸發額外搜尋。")
                else:
                    st.info("未啟用聯網或未取得來源中繼資料。")

        except Exception as e:
            st.error(f"搜尋失敗：{str(e)}")
