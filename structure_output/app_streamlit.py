"""
app_streamlit.py
實務應用整合：Streamlit 結構化資料萃取與 CSV 下載工具
功能：輸入任意文字，結構化提取為 JSON，支援即時表格預覽與一鍵下載 CSV
"""

import json
import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pandas as pd
from pydantic import BaseModel, Field
import streamlit as st

st.set_page_config(page_title="結構化資料萃取儀表板", page_icon="📑", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("📑 Gemini 結構化輸出 (Pydantic / JSON)")
st.caption("將非結構化文字自動轉化為強型別 JSON 與 Pandas 表格")


class RateItem(BaseModel):
    currency_code: str = Field(description="幣別代碼")
    currency_name: str = Field(description="中文幣別")
    cash_buying: float = Field(description="現金買入")
    cash_selling: float = Field(description="現金賣出")


class RateTable(BaseModel):
    query_date: str = Field(description="牌告日期")
    rates: List[RateItem] = Field(description="匯率資料")


sample_text = """
臺灣銀行牌告匯率 查詢日期：2025/01/29
美金 (USD) 現金買入：32.45000 現金賣出：33.12000
日圓 (JPY) 現金買入：0.20800 現金賣出：0.21800
歐元 (EUR) 現金買入：33.80000 現金賣出：35.10000
人民幣 (CNY) 現金買入：4.45000 現金賣出：4.62000
"""

raw_input = st.text_area("輸入或貼上非結構化文字：", value=sample_text, height=150)

if st.button("⚡ 開始結構化提取", type="primary"):
    with st.spinner("Gemini 正在透過 Pydantic Schema 進行精確結構化..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=[raw_input, "請將牌告匯率文字轉為結構化資料。"],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RateTable,
                )
            )
            data = json.loads(response.text)
            st.success(f"✅ 提取成功！查詢日期：{data.get('query_date')}")

            df = pd.DataFrame(data["rates"])
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 下載為 CSV 檔案",
                data=csv,
                file_name="exchange_rates.csv",
                mime="text/csv"
            )

            with st.expander("檢視原始 JSON"):
                st.json(data)

        except Exception as e:
            st.error(f"提取失敗：{str(e)}")
