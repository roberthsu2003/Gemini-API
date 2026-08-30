# 📊 結構化輸出 (Structured Outputs & Pydantic)

Google Gemini API 支援**結構化輸出 (Structured Outputs)**，可透過傳入 Python `Pydantic` 模型或 `JSON Schema`，強制模型保證輸出的內容 100% 符合定義的型別架構（無任何多餘的 Markdown 標記或語法錯誤），是打造可靠 AI Agent 與資料萃取系統的關鍵能力。

> 📖 **官方說明**：
> 透過設定 `response_mime_type="application/json"` 與 `response_schema`，可支援巢狀物件、清單、條件多態 (`Union`)、遞迴樹狀結構與列舉 (`Enum`)。
> 官方文件：[Structured outputs - Google AI for Developers](https://ai.google.dev/gemini-api/docs/structured-output)

---

## 📑 目錄導覽

1. [Pydantic 基礎 Schema 資料萃取 (01_pydantic_basic.py)](#1-pydantic-基礎-schema-資料萃取-01_pydantic_basicpy)
2. [進階 Schema：遞迴樹狀與列舉 (02_advanced_schemas.py)](#2-進階-schema遞迴樹狀與列舉-02_advanced_schemaspy)
3. [非結構化匯率文字轉結構化數據 (03_currency_exchange.py)](#3-非結構化匯率文字轉結構化數據-03_currency_exchangepy)
4. [課堂互動筆記本 (Jupyter Notebooks)](#4-課堂互動筆記本-jupyter-notebooks)

---

## 1. Pydantic 基礎 Schema 資料萃取 (`01_pydantic_basic.py`)

使用 Pydantic 定義強型別資料模型，確保輸出為精確的 JSON 物件：

- 核心程式檔案：[`01_pydantic_basic.py`](./01_pydantic_basic.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

client = genai.Client()

class Ingredient(BaseModel):
    name: str = Field(description="食材名稱")
    quantity: str = Field(description="份量")

class Recipe(BaseModel):
    recipe_name: str = Field(description="食譜名稱")
    cooking_time_minutes: int = Field(description="烹飪時間（分鐘）")
    ingredients: List[Ingredient] = Field(description="食材清單")
    steps: List[str] = Field(description="料理步驟")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="請提供一份義大利番茄肉醬麵的食譜。",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Recipe,
    )
)

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述結構化提取程式改寫為 Gradio 應用：
1. 包含文字輸入框供使用者輸入需求。
2. 呼叫 Gemini 結構化輸出取得 JSON 後，自動轉為 Pandas DataFrame 並以 gr.Dataframe 展示。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit 應用：
1. 主畫面輸入文字，點擊按鈕後進行結構化資料提取。
2. 畫面呈現互動式表格，並提供一鍵下載 CSV 按鈕 (st.download_button)。
```

**Telegram Bot 結構化小幫手 Prompt：**
```text
請幫我將結構化提取程式封裝為 Telegram Bot：
1. 接收使用者輸入的菜餚名稱。
2. 呼叫 Gemini Pydantic Schema 生成 JSON，排版為清楚的食材清單與步驟回應用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/extract-recipe 端點：
1. 接收 Request 包含 text 欄位。
2. 呼叫 Gemini 回傳強型別 RecipeModel JSON 物件。
```
</details>

---

## 2. 進階 Schema：遞迴樹狀與列舉 (`02_advanced_schemas.py`)

支援 Enum 狀態約束與自身遞迴的樹狀 WBS 任務結構：

- 核心程式檔案：[`02_advanced_schemas.py`](./02_advanced_schemas.py)

---

## 3. 非結構化匯率文字轉結構化數據 (`03_currency_exchange.py`)

- 核心程式檔案：[`03_currency_exchange.py`](./03_currency_exchange.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

---

## 4. 課堂互動筆記本 (Jupyter Notebooks)

- [`lesson1.ipynb`](./lesson1.ipynb)：結構化輸出完整教學筆記本
- [`exchange_rate_extraction.ipynb`](./exchange_rate_extraction.ipynb)：牌告匯率提取筆記本
- [`exchange_rate_to_csv.ipynb`](./exchange_rate_to_csv.ipynb)：牌告匯率存為 CSV 筆記本
