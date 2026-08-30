"""
app_gradio.py
實務應用整合：Gradio 結構化資料提取器
功能：輸入任意非結構化文字，強制以 Pydantic 輸出 JSON 並自動渲染為表格
"""

import json
import os
from typing import List
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types
import pandas as pd
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class ExchangeItem(BaseModel):
    currency: str = Field(description="幣別代碼與名稱，例如 USD (美金)")
    cash_buying: float = Field(description="現金買入匯率")
    cash_selling: float = Field(description="現金賣出匯率")


class ExchangeResult(BaseModel):
    source_date: str = Field(description="牌告匯率日期")
    items: List[ExchangeItem] = Field(description="匯率清單")


def extract_data(raw_text: str):
    if not raw_text.strip():
        return None, "請輸入文字內容"

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=[raw_text, "請將文字中的牌告匯率資訊嚴格轉為結構化資料。"],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExchangeResult,
        )
    )

    data = json.loads(response.text)
    df = pd.DataFrame(data["items"])
    return df, f"✅ 提取成功！資料日期：{data.get('source_date', '未知')}\n\n```json\n{response.text}\n```"


with gr.Blocks(title="結構化資訊萃取器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📊 Gemini 結構化輸出與表格轉換")
    gr.Markdown("將任意凌亂的網頁匯率、公告或報表文字，精確轉換為 Pandas DataFrame 表格與合法 JSON。")

    raw_input = gr.Textbox(
        label="貼上原始文字",
        placeholder="例如：臺灣銀行牌告匯率 2025/01/29 美金現金買入 32.45 現金賣出 33.12...",
        lines=6
    )
    extract_btn = gr.Button("⚡ 結構化萃取", variant="primary")

    df_output = gr.Dataframe(label="萃取出的表格數據")
    json_output = gr.Markdown(label="JSON Schema 原始輸出")

    extract_btn.click(fn=extract_data, inputs=[raw_input], outputs=[df_output, json_output])

if __name__ == "__main__":
    demo.launch()
