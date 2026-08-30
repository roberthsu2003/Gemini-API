# Gemini API 應用實戰指南

本專案全面介紹與實作 **Google Gemini API**，示範如何將 Google 最新的 Gemini 3 世代大語言模型與強大工具整合到各類 Python 應用程式與 AI Agent 工作流程中。

---

> **專案版本更新（2026 最新規範）**：
> - 全面採用 Google 官方推薦的 **Interactions API** (`client.interactions.create`) 與最新 [`google-genai`](https://github.com/googleapis/python-genai) SDK。
> - 支援 **Gemini 3** 最新模型（`gemini-3.7-flash`、`gemini-3.5-flash-lite`、`gemini-3.1-pro-preview` 等）。
> - 每個單元均提供可直接執行的 Python 腳本、Jupyter Notebook，並附帶 **AI 賦能提示詞 (Prompts)**，方便一鍵利用 AI 生成 Gradio 或 Streamlit 視覺化 Web 介面。

## 📱 Telegram Bot 連線與應用

Telegram 是串接大語言模型與 AI Agent 最輕量、好寫且開發體驗極佳的通訊管道（免 Webhook/伺服器、支援本機 Polling 輪詢快速測試、30 秒極速申請 Token）。

👉 **完整教學與範例程式碼請參閱專屬章節**：[**【📱 Telegram Bot 連線方式與機器人開發】(./telegram_bot)**](./telegram_bot)
- [`basic_bot.py`](./telegram_bot/basic_bot.py)：Telegram 基礎連線與 Echo 文字回覆範例
- [`gemini_bot.py`](./telegram_bot/gemini_bot.py)：串接 Gemini 3.7 Flash Interactions API 的智慧對話助理
- [`README.md`](./telegram_bot/README.md)：Token 申請、Polling/Webhook 部署考量與完整開發手冊

---

## 🛠️ 環境需求與安裝

- **Python**：3.9+
- **套件管理**：推薦使用 `uv` 或 `pip`
- **核心套件**：`google-genai`、`pydantic`、`python-dotenv`、`gradio`、`streamlit`

使用 `uv` 快速安裝：
```bash
uv add google-genai pydantic python-dotenv gradio requests beautifulsoup4
```

設定 API Key（儲存於專案根目錄 `.env` 檔案中）：
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🤖 目前推薦模型清單

| 用途 | 推薦模型 | 特性與說明 |
|---|---|---|
| **通用主力（預設首選）** | `gemini-3.7-flash` | 1M tokens 上下文，平衡速度、多模態、思考推理與 Agentic 任務。 |
| **低成本 / 高吞吐** | `gemini-3.5-flash-lite` | 最經濟、極速回應，適合高頻次輕量任務與資料萃取。 |
| **深度推理 / 複雜編程** | `gemini-3.1-pro-preview` | 1M tokens 上下文，頂級程式碼生成、數學邏輯與深度研究。 |
| **文字向量嵌入** | `gemini-embedding-001` | 支援 `task_type` 與可自訂維度 (`output_dimensionality`)。 |
| **多模態向量嵌入** | `gemini-embedding-2` | 支援文字、圖片、影片與音訊的多模態統一嵌入。 |

> ⚠️ **已淘汰模型**：舊版 `gemini-2.0-*`、`gemini-1.5-*` 全系列及舊版 `google-generativeai` 套件已全面停用，請使用上述最新模型。

---

## ⚡ 快速開始 (Interactions API)

Interactions API 是 Google 官方推薦的統一互動介面，使用 `client.interactions.create()` 即可涵蓋文字生成、多模態輸入、串流輸出、工具調用與伺服器端狀態維護的多輪對話。

### 基本文字生成

```python
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請用繁體中文以三點簡要說明什麼是 AI Agent？"
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入 Gradio / Streamlit 介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述的 Gemini 基本文字生成 Python 程式碼改寫為 Gradio 網頁應用程式：
1. 使用 gr.Blocks 建立介面，包含一個多行文字輸入框與「送出」按鈕。
2. 使用 gr.Markdown 呈現模型的回覆。
3. 整合 client.interactions.create(model="gemini-3.7-flash", input=...) 邏輯。
4. 加入問題範例選單（gr.Examples）供使用者點選測試。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述的 Gemini 基本文字生成 Python 程式碼改寫為 Streamlit 網頁應用程式：
1. 使用 st.set_page_config 與 st.title 建立美觀標題。
2. 側邊欄提供 API Key 設定與模型選擇。
3. 主畫面提供 st.text_area 接收使用者問題，按下按鈕後以 st.spinner 提示，並以 st.markdown 呈現排版結果。
```
</details>

---

### 思考模式設定 (Thinking with Gemini)

Gemini 3 世代模型具備內建思考推理能力，可透過 `generation_config` 中的 `thinking_level`（`minimal` / `low` / `medium` / `high`）精準調節思考深度：

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請分析量子運算對現行 RSA 加密演算法帶來的具體衝擊。",
    generation_config={
        "thinking_level": "medium",
        "temperature": 1.0  # 官方建議思考模式下維持預設 1.0
    }
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入思考深度控制介面</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述包含 thinking_level 的程式改寫為 Streamlit 應用程式：
1. 在側邊欄使用 st.select_slider 讓使用者自由調節思考深度（minimal, low, medium, high）。
2. 主畫面輸入問題後，呼叫 Gemini 3.7 Flash 進行深度推理回答。
```
</details>

---

## 📚 專案核心章節導覽（推薦學習順序）

本教學專案依據學生的認知學習曲線，分為五大進階階段：

---

### 🔰 第一階段：基礎互動與多模態體驗（建立成就感）

#### [1. 文字生成 (text_generation)](./text_generation)
劃分「Gemini 核心功能指南（純 Python 教學）」與「實務應用整合實戰（Telegram / Gradio / Streamlit / FastAPI）」雙層架構：
- **核心教學**：[`01_basic_text.py`](./text_generation/01_basic_text.py)（文字生成）、[`02_thinking_mode.py`](./text_generation/02_thinking_mode.py)（思考深度）、[`03_system_and_params.py`](./text_generation/03_system_and_params.py)（系統指示詞與參數）、[`04_multimodal_image.py`](./text_generation/04_multimodal_image.py)（多模態圖文）、[`05_streaming.py`](./text_generation/05_streaming.py)（即時串流）、[`06_stateful_chat.py`](./text_generation/06_stateful_chat.py)（狀態化對話）、[`07_stateless_chat.py`](./text_generation/07_stateless_chat.py)（無狀態對話）
- **實務整合**：[`app_telegram_bot.py`](./text_generation/app_telegram_bot.py)（Telegram Bot）、[`app_gradio.py`](./text_generation/app_gradio.py)（Gradio Web UI）、[`app_streamlit.py`](./text_generation/app_streamlit.py)（Streamlit 儀表板）、[`app_fastapi.py`](./text_generation/app_fastapi.py)（FastAPI 後端與 SSE 串流）
- **互動筆記**：[`text_generation_quickstart.ipynb`](./text_generation/text_generation_quickstart.ipynb)、[`trip_planner_system_instruction.ipynb`](./text_generation/trip_planner_system_instruction.ipynb)

#### [2. 圖像生成 (image_generation)](./image_generation)
使用 Google Imagen 3 (`imagen-3.0-generate-002`) 與 `gemini-2.5-flash-image` 進行 Text-to-Image 生成與 Prompt 擴寫工作流：
- **核心教學**：[`01_text_to_image.py`](./image_generation/01_text_to_image.py)（基礎生圖）、[`02_aspect_ratio.py`](./image_generation/02_aspect_ratio.py)（比例控制）、[`03_gemini_flash_image.py`](./image_generation/03_gemini_flash_image.py)（Gemini 生圖）、[`04_prompt_enhancer.py`](./image_generation/04_prompt_enhancer.py)（Prompt 智慧擴寫）
- **實務整合**：[`app_telegram_bot.py`](./image_generation/app_telegram_bot.py)（Telegram 算圖 Bot）、[`app_gradio.py`](./image_generation/app_gradio.py)（Gradio 畫廊工作台）、[`app_streamlit.py`](./image_generation/app_streamlit.py)（Streamlit 生圖室）、[`app_fastapi.py`](./image_generation/app_fastapi.py)（FastAPI 產圖 API）

#### [3. 文件理解 (document_understanding)](./document_understanding)
原生多模態 PDF 視覺理解（支援達 1000 頁 / 50MB），涵蓋 Inline、Files API、跨文件比對與 Context Caching 快取：
- **核心教學**：[`01_inline_pdf_summary.py`](./document_understanding/01_inline_pdf_summary.py)（Inline 摘要）、[`02_files_api_pdf_chat.py`](./document_understanding/02_files_api_pdf_chat.py)（Files API 多輪問答）、[`03_remote_pdf_analysis.py`](./document_understanding/03_remote_pdf_analysis.py)（URL 下載研讀）、[`04_multi_pdf_comparison.py`](./document_understanding/04_multi_pdf_comparison.py)（跨文件比對）、[`05_pdf_structured_extraction.py`](./document_understanding/05_pdf_structured_extraction.py)（Pydantic 規格萃取）、[`06_pdf_context_caching.py`](./document_understanding/06_pdf_context_caching.py)（Context Caching 快取）
- **實務整合**：[`app_telegram_bot.py`](./document_understanding/app_telegram_bot.py)（Telegram PDF 助理）、[`app_gradio.py`](./document_understanding/app_gradio.py)（Gradio 研讀工作台）、[`app_streamlit.py`](./document_understanding/app_streamlit.py)（Streamlit 知識庫問答）、[`app_fastapi.py`](./document_understanding/app_fastapi.py)（FastAPI 分析端點）
- **互動筆記**：[`pdf_understanding_tutorial.ipynb`](./document_understanding/pdf_understanding_tutorial.ipynb)、[`csv_document_caching.ipynb`](./document_understanding/csv_document_caching.ipynb)

---

### ⚙️ 第二階段：工程化與資料約束（應用開發必備）

#### [4. 結構化輸出 (structure_output)](./structure_output)
強制約束模型輸出嚴格符合 JSON Schema 或 Pydantic 模型，涵蓋條件多態 (`Union`)、遞迴樹狀結構與列舉：
- **核心教學**：[`01_pydantic_basic.py`](./structure_output/01_pydantic_basic.py)（Pydantic 基礎）、[`02_advanced_schemas.py`](./structure_output/02_advanced_schemas.py)（遞迴樹狀與 Enum）、[`03_currency_exchange.py`](./structure_output/03_currency_exchange.py)（匯率文字轉數據）
- **實務整合**：[`app_telegram_bot.py`](./structure_output/app_telegram_bot.py)（Telegram 結構化提取）、[`app_gradio.py`](./structure_output/app_gradio.py)（Gradio 表格轉換器）、[`app_streamlit.py`](./structure_output/app_streamlit.py)（Streamlit CSV 下載工具）、[`app_fastapi.py`](./structure_output/app_fastapi.py)（FastAPI 強型別 API）
- **互動筆記**：[`lesson1.ipynb`](./structure_output/lesson1.ipynb)、[`exchange_rate_extraction.ipynb`](./structure_output/exchange_rate_extraction.ipynb)、[`exchange_rate_to_csv.ipynb`](./structure_output/exchange_rate_to_csv.ipynb)

---

### 🛠️ 第三階段：外掛能力與工具整合（突破 LLM 限制）

#### [5. 聯網搜尋 (ground_search)](./ground_search)
啟用 Google Search Grounding 讓模型自主聯網搜尋最新即時資訊，自動標註來源網址：
- **核心教學**：[`01_basic_search.py`](./ground_search/01_basic_search.py)（基礎聯網）、[`02_search_citations.py`](./ground_search/02_search_citations.py)（引用來源解析）、[`03_search_with_code_execution.py`](./ground_search/03_search_with_code_execution.py)（聯網 + Python 運算）、[`04_search_structured_output.py`](./ground_search/04_search_structured_output.py)（聯網 + 結構化輸出）
- **實務整合**：[`app_telegram_bot.py`](./ground_search/app_telegram_bot.py)（Telegram 查證 Bot）、[`app_gradio.py`](./ground_search/app_gradio.py)（Gradio 來源查核）、[`app_streamlit.py`](./ground_search/app_streamlit.py)（Streamlit 時事情報）、[`app_fastapi.py`](./ground_search/app_fastapi.py)（FastAPI 搜尋端點）

#### [6. 程式碼執行 (code_execution)](./code_execution)
模型自主在 Google 託管的 Python 安全沙盒中編寫並執行程式碼，徹底避免算術幻覺：
- **核心教學**：[`01_math_solver.py`](./code_execution/01_math_solver.py)（數學運算求解）、[`02_currency_calculator.py`](./code_execution/02_currency_calculator.py)（CSV 匯率運算）、[`03_matplotlib_plotter.py`](./code_execution/03_matplotlib_plotter.py)（Matplotlib 動態繪圖）、[`04_image_zoom_inspection.py`](./code_execution/04_image_zoom_inspection.py)（圖片程式碼局部裁切）
- **實務整合**：[`app_telegram_bot.py`](./code_execution/app_telegram_bot.py)（Telegram 運算 Bot）、[`app_gradio.py`](./code_execution/app_gradio.py)（Gradio 沙盒工作台）、[`app_streamlit.py`](./code_execution/app_streamlit.py)（Streamlit 演算儀表板）、[`app_fastapi.py`](./code_execution/app_fastapi.py)（FastAPI 沙盒 API）
- **互動筆記**：[`math_and_code_execution.ipynb`](./code_execution/math_and_code_execution.ipynb)、[`currency_calculator.ipynb`](./code_execution/currency_calculator.ipynb)

#### [7. 函式呼叫 (function_calling)](./function_calling)
讓模型連接外部 API 與工具，自動識別意圖、提取參數並執行動作：
- **核心教學**：[`01_meeting_scheduler.py`](./function_calling/01_meeting_scheduler.py)（會議預約 4 步驟）、[`02_weather_assistant.py`](./function_calling/02_weather_assistant.py)（即時天氣查詢）、[`03_parallel_function_calling.py`](./function_calling/03_parallel_function_calling.py)（多工具平行呼叫）、[`04_multi_tool_search_and_function.py`](./function_calling/04_multi_tool_search_and_function.py)（聯網 + 自訂工具混合）
- **實務整合**：[`app_telegram_bot.py`](./function_calling/app_telegram_bot.py)（Telegram 工具管家）、[`app_gradio.py`](./function_calling/app_gradio.py)（Gradio 智慧控制台）、[`app_streamlit.py`](./function_calling/app_streamlit.py)（Streamlit 管家儀表板）、[`app_fastapi.py`](./function_calling/app_fastapi.py)（FastAPI 工具 API）
- **互動筆記**：[`basic_function_calling.ipynb`](./function_calling/basic_function_calling.ipynb)、[`multi_function_calling.ipynb`](./function_calling/multi_function_calling.ipynb)、[`parallel_function_calling.ipynb`](./function_calling/parallel_function_calling.ipynb)、[`chat_function_history.ipynb`](./function_calling/chat_function_history.ipynb)

---

### 🧠 第四階段：企業級記憶與 RAG 檢索（海量資料庫）

#### [8. 向量檢索 (embeddings)](./embeddings/document_search)
將文字內容轉為語意向量，支援 `gemini-embedding-001`、Matryoshka (MRL) 維度縮減與非對稱檢索：
- **核心教學**：[`01_gemini_semantic_similarity.py`](./embeddings/document_search/01_gemini_semantic_similarity.py)（語意相似度）、[`02_gemini_document_retrieval.py`](./embeddings/document_search/02_gemini_document_retrieval.py)（非對稱檢索）、[`03_dimension_reduction.py`](./embeddings/document_search/03_dimension_reduction.py)（Matryoshka 維度縮減）、[`04_document_search_e5.py`](./embeddings/document_search/04_document_search_e5.py)（開源 E5 模型）
- **實務整合**：[`app_telegram_bot.py`](./embeddings/document_search/app_telegram_bot.py)（Telegram 知識庫 Bot）、[`app_gradio.py`](./embeddings/document_search/app_gradio.py)（Gradio 相似度工作台）、[`app_streamlit.py`](./embeddings/document_search/app_streamlit.py)（Streamlit 語意搜尋儀表板）、[`app_fastapi.py`](./embeddings/document_search/app_fastapi.py)（FastAPI 向量 API）
- **互動筆記**：[`gemini_embedding_tutorial.ipynb`](./embeddings/document_search/gemini_embedding_tutorial.ipynb)、[`csv_semantic_search.ipynb`](./embeddings/document_search/csv_semantic_search.ipynb)

---

### 🚀 第五階段：綜合架構與生態拓展（融會貫通）

#### [9. 何謂 AI Agent (何謂AIAgent)](./何謂AIAgent)
代理觀念與工作流設計模式，探討 LLM 工作流與自主代理人的本質區別。
- 涵蓋設計模式：Prompt chaining、Routing、Parallelization、Orchestrator-workers、Evaluator-optimizer
- 核心手冊：[`README.md`](./何謂AIAgent/README.md)

#### [10. 開源模型 (開源模型)](./開源模型)
整合 Hugging Face Serverless Inference API，調用開源大語言模型（如 Mistral-Nemo-Instruct）進行文字生成與摘要任務。
- [`text_to_summarization.py`](./開源模型/text_to_summarization.py)：Hugging Face 模型文字摘要實作
- [`test.ipynb`](./開源模型/test.ipynb)：開源模型調用測試筆記本

---

## 📦 專案內建完整素材與資料檔 (Assets)

本專案在 GitHub 上已包含所有教學範例所需的完整素材檔案，學生 Clone 專案後**無需自行尋找或下載任何素材**即可直接練習：

- 📄 **PDF 文件**：[`說明書.pdf`](./document_understanding/說明書.pdf)（冷氣壁掛式說明書，4MB，用於長文件問答與快取）
- 📊 **表格資料**：
  - [`2025_01_29.csv`](./structure_output/2025_01_29.csv)（臺灣銀行牌告匯率表格）
  - [`aqx_p_488.csv`](./document_understanding/aqx_p_488.csv)（空氣品質監測資料，134KB）
  - [`001.csv`](./embeddings/document_search/001.csv)（知識庫說明文件，用於語意檢索）
- 🖼️ **圖片素材**：
  - [`organ.jpg`](./structure_output/organ.jpg)（管風琴樂器相片，用於分類與多模態分析）
  - [`bear.jpg`](./text_generation/bear.jpg)（棕熊相片，用於圖文問答）
  - [`plant1.jpg`](./text_generation/plant1.jpg) ~ [`plant3.webp`](./text_generation/plant3.webp)（植物相片）
- 📑 **評測與向量檔**：
  - [`Embeddings模型評測.xlsx`](./embeddings/document_search/Embeddings模型評測.xlsx)（繁體中文 Embedding 效果評測表）
  - [`embeddings.pkl`](./embeddings/document_search/pretrain_and_query/embeddings.pkl)（預先計算之向量庫檔案）

---

## 📖 專案結構細節

詳細目錄樹結構與各檔案詳細介紹請參閱 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。
