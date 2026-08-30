# 📑 文件理解與長篇 PDF 解析 (Document Understanding)

Google Gemini 模型具備原生的**多模態文件理解能力**，支援直接傳入長達 1000 頁的 PDF 文件、掃描圖檔或圖表，無需預先透過 OCR 轉文字即可直接辨識文字、排版結構、表格數據與多模態圖示。

> 📖 **官方說明**：
> 小型文件（< 20MB）可直接以 Inline 方式傳入；大型長篇文件可透過 Google Files API 上傳，或結合 Context Caching（上下文快取）節省 75% 成本並加速回應。
> 官方文件：[Document processing - Google AI for Developers](https://ai.google.dev/gemini-api/docs/document-processing)

---

## 📑 目錄導覽

1. [Inline PDF 重點摘要 (01_inline_pdf_summary.py)](#1-inline-pdf-重點摘要-01_inline_pdf_summarypy)
2. [Files API 上傳大型 PDF 多輪問答 (02_files_api_pdf_chat.py)](#2-files-api-上傳大型-pdf-多輪問答-02_files_api_pdf_chatpy)
3. [遠端 URL PDF 下載與研讀 (03_remote_pdf_analysis.py)](#3-遠端-url-pdf-下載與研讀-03_remote_pdf_analysispy)
4. [多份 PDF 跨文件比對 (04_multi_pdf_comparison.py)](#4-多份-pdf-跨文件比對-04_multi_pdf_comparisonpy)
5. [PDF 結構化資訊萃取 (05_pdf_structured_extraction.py)](#5-pdf-結構化資訊萃取-05_pdf_structured_extractionpy)
6. [Context Caching 長篇文件快取 (06_pdf_context_caching.py)](#6-context-caching-長篇文件快取-06_pdf_context_cachingpy)
7. [課堂互動筆記本 (Jupyter Notebooks)](#7-課堂互動筆記本-jupyter-notebooks)

---

## 1. Inline PDF 重點摘要 (`01_inline_pdf_summary.py`)

小型 PDF 檔案可直接讀取 byte 資料傳入 `client.interactions.create`：

- 核心程式檔案：[`01_inline_pdf_summary.py`](./01_inline_pdf_summary.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
import os
from pathlib import Path
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
pdf_bytes = Path("document_understanding/說明書.pdf").read_bytes()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "請針對這份冷氣壁掛式說明書，用繁體中文條列出重要安全注意事項與保養方法。"
    ]
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 PDF 分析程式改寫為 Gradio 網頁應用：
1. 提供檔案上傳元件 gr.File(file_types=[".pdf"])。
2. 上傳後自動讀取二進位資料並呼叫 Gemini 3.7 Flash 進行重點摘要。
3. 輸出區以 Markdown 呈現排版結果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit PDF 助理：
1. 側邊欄提供 st.file_uploader 上傳 PDF。
2. 主畫面提供 st.chat_input 讓用戶對 PDF 內容進行自由提問。
```

**Telegram Bot 研讀 Prompt：**
```text
請幫我將上述程式封裝為 Telegram 機器人：
1. 監聽 MessageHandler(filters.Document.ALL)。
2. 當接收到 PDF 檔案時下載並呼叫 Gemini 產出文件摘要。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 FastAPI 端點 POST /api/pdf/analyze：
1. 使用 UploadFile 接收 PDF。
2. 調用 Gemini Interactions API 進行文件分析並回傳 JSON 結果。
```
</details>

---

## 2. Files API 上傳大型 PDF 多輪問答 (`02_files_api_pdf_chat.py`)

針對大型檔案，使用 Files API 上傳後由伺服器端保存並支援多輪對話：

- 核心程式檔案：[`02_files_api_pdf_chat.py`](./02_files_api_pdf_chat.py)
- 實務應用範例：[`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

```python
from google import genai

client = genai.Client()
uploaded_file = client.files.upload(file="document_understanding/說明書.pdf")

turn_1 = client.interactions.create(
    model="gemini-3.7-flash",
    input=[uploaded_file, "這台機器的濾網清洗週期是多久？"]
)
print(turn_1.output_text)

turn_2 = client.interactions.create(
    model="gemini-3.7-flash",
    input="若運轉出現異音可能的原因有哪些？",
    previous_interaction_id=turn_1.id
)
print(turn_2.output_text)
```

---

## 3. 遠端 URL PDF 下載與研讀 (`03_remote_pdf_analysis.py`)

- 核心程式檔案：[`03_remote_pdf_analysis.py`](./03_remote_pdf_analysis.py)

---

## 4. 多份 PDF 跨文件比對 (`04_multi_pdf_comparison.py`)

- 核心程式檔案：[`04_multi_pdf_comparison.py`](./04_multi_pdf_comparison.py)

---

## 5. PDF 結構化資訊萃取 (`05_pdf_structured_extraction.py`)

- 核心程式檔案：[`05_pdf_structured_extraction.py`](./05_pdf_structured_extraction.py)

---

## 6. Context Caching 長篇文件快取 (`06_pdf_context_caching.py`)

- 核心程式檔案：[`06_pdf_context_caching.py`](./06_pdf_context_caching.py)

---

## 7. 課堂互動筆記本 (Jupyter Notebooks)

- [`pdf_understanding_tutorial.ipynb`](./pdf_understanding_tutorial.ipynb)：PDF 文件理解教學筆記本
- [`csv_document_caching.ipynb`](./csv_document_caching.ipynb)：CSV 數據快取與問答筆記本
