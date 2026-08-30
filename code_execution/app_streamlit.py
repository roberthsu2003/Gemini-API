"""
app_streamlit.py
實務應用整合：Streamlit Python 數據演算與圖表工作台
功能：輸入自訂數據或演算法問題，即時在沙盒中運算與繪圖
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st

st.set_page_config(page_title="Python 沙盒運算儀表板", page_icon="⚡", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("⚡ Gemini 程式碼執行沙盒 (Code Execution)")
st.caption("透過 Google 託管的 Python 沙盒執行程式，解決數值運算與資料視覺化任務")

task_type = st.selectbox(
    "選擇任務類型範例：",
    [
        "數學與演算法求解 (計算 1 到 1000 的質數數量與清單)",
        "牌告匯率換算 (計算 10 萬台幣依賣出匯率換算美金/日圓/歐元)",
        "動態統計繪圖 (繪製鳶尾花特徵常態分佈曲線)"
    ]
)

custom_prompt = st.text_area("或自行輸入運算需求：", value=task_type, height=100)

if st.button("🚀 執行 Python 沙盒運算", type="primary"):
    with st.spinner("Gemini 正在撰寫 Python 程式並於沙盒中執行..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=custom_prompt + "\n（請使用 Python 程式碼演算，並以繁體中文完整解釋）",
                config=types.GenerateContentConfig(
                    tools=[types.Tool(code_execution=types.ToolCodeExecution())],
                ),
            )
            st.markdown("### 🤖 執行歷程與解答")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"運算失敗：{str(e)}")
