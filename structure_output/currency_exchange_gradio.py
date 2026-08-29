import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr
from pydantic import BaseModel, Field

load_dotenv()

with open("2025_01_29.csv", encoding="utf-8") as file:
    csv_content = file.read()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

base_instruction = (
    """
## 請依據以下的csv格式的文字回答問題
## 這個表格是銀行的台幣和各幣值的轉換匯率
## 如果沒有資料,請輸出`沒有相關幣的資料`
## 規則:
    1.如果使用者輸入的是台幣要換取美金,換算公式為:
    `台幣/現金匯率本行賣出的美金價格=`
    2.如果使用者輸入的是美金換取台幣,換算公式為:
    `現金匯率本行買入美金*美金的金額=`
    3.如果不是換成台幣,請先將金額換成台幣後,再轉換為使用者要求的幣值
"""
    + csv_content
)


class CurrencyList(BaseModel):
    currencies: list[str] = Field(description="支援換算的貨幣名稱清單")


# 透過 Interactions API 取得可換算幣別清單 (JSON 結構化輸出)
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="""
1. 以現有的資料,台幣可以換算的幣值有哪一些?
2. 請排除無法計算的幣別
3. 請加入台幣
""",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": CurrencyList.model_json_schema(),
    },
    system_instruction=base_instruction,
)

currency_data = CurrencyList.model_validate_json(interaction.output_text)
currencies = currency_data.currencies


with gr.Blocks(title="Gemini 牌告匯率換算") as demo:
    currency_in = "台幣"
    currency_out = ""
    gr.Markdown(
        """
        # 💱 智慧匯率換算助理
        **資料來源：臺灣銀行牌告匯率（結合 Gemini 結構化輸出）**
        """
    )

    in_radio = gr.Radio(
        currencies, label="持有幣別", info="您手上的幣別", value=currency_in
    )
    out_radio = gr.Radio(currencies, label="兌換幣別", info="您要轉換的幣別")

    with gr.Row():
        number = gr.Number(
            value=1000, label=f"{currency_in} 轉換為 {currency_out}", visible=True
        )
        btn = gr.Button(value="開始計算", variant="primary", visible=True)

    result_markdown = gr.Markdown()

    def radio_change(in_radio_value, in_output_value):
        currencies_copy = currencies.copy()
        if in_radio_value in currencies_copy:
            currencies_copy.remove(in_radio_value)
        if in_radio_value and in_output_value:
            return [
                gr.Number(
                    visible=True,
                    label=f"{in_radio_value} 轉換為 {in_output_value}",
                    interactive=True,
                ),
                gr.Button(visible=True),
                gr.Radio(currencies_copy, label="兌換幣別", info="您要轉換的幣別"),
            ]
        else:
            return [
                gr.Number(visible=False),
                gr.Button(visible=False),
                gr.Radio(currencies_copy, label="兌換幣別", info="您要轉換的幣別"),
            ]

    gr.on(
        triggers=[in_radio.change, out_radio.change],
        fn=radio_change,
        inputs=[in_radio, out_radio],
        outputs=[number, btn, out_radio],
    )

    @btn.click(inputs=[number, in_radio, out_radio], outputs=result_markdown)
    def btn_click(number_value, in_radio_value, in_output_value):
        if not in_radio_value or not in_output_value:
            return "請先選擇持有幣別與兌換幣別！"

        prompt = f"請將 {number_value} {in_radio_value} 轉換為 {in_output_value}，請輸出為 Markdown 格式並附上計算步驟與公式。"
        res = client.interactions.create(
            model="gemini-3.7-flash",
            input=prompt,
            system_instruction=base_instruction,
        )
        return res.output_text


if __name__ == "__main__":
    demo.launch()
