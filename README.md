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
使用 Interactions API 進行單輪生成、Thinking 思考層級控制、系統指示、多模態圖文理解與狀態化多輪串流對話。
- [`zero_shot.py`](./text_generation/zero_shot.py)：零樣本文字生成與 Gradio 介面
- [`text_streaming.py`](./text_generation/text_streaming.py)：即時 Token 串流輸出（SSE 事件）
- [`chat.py`](./text_generation/chat.py)：伺服器端狀態化多輪對話 (`previous_interaction_id`)
- [`image_text.py`](./text_generation/image_text.py)：多模態圖文綜合理解與問答
- [`text_to_summarization.py`](./text_generation/text_to_summarization.py)：長文本重點摘要與語氣風格控制
- [`text_generation_quickstart.ipynb`](./text_generation/text_generation_quickstart.ipynb)：Interactions API 完整語法互動筆記本
- [`trip_planner_system_instruction.ipynb`](./text_generation/trip_planner_system_instruction.ipynb)：旅遊規劃與 System Instruction 實戰

#### [2. 圖像生成 (image_generation)](./image_generation)
使用 Google Imagen 3 (`imagen-3.0-generate-002`) 與 `gemini-2.5-flash-image` 進行 Text-to-Image 生成，支援比例自訂與 Prompt 智慧擴寫產圖工作流。
- [`text_to_image_imagen.py`](./image_generation/text_to_image_imagen.py)：Imagen 3 基礎文字生成高品質圖片
- [`aspect_ratio_control.py`](./image_generation/aspect_ratio_control.py)：自訂長寬比例（16:9、9:16、1:1）生成範例
- [`gemini_flash_image.py`](./image_generation/gemini_flash_image.py)：Gemini 2.5 Flash Image 多模態圖像生成
- [`prompt_enhancer_and_generator.py`](./image_generation/prompt_enhancer_and_generator.py)：Gemini 擴寫提示詞 ➔ 自動調用 Imagen 生成圖片的一條龍工作流

#### [3. 文件理解 (document_understanding)](./document_understanding)
原生多模態 PDF 視覺理解（支援達 1000 頁 / 50MB），涵蓋 Inline 傳遞、Files API 上傳、跨文件比對、結構化萃取與 Context Caching 快取加速。
- [`inline_pdf_summary.py`](./document_understanding/inline_pdf_summary.py)：Inline PDF 文件重點摘要
- [`files_api_pdf_chat.py`](./document_understanding/files_api_pdf_chat.py)：Files API 上傳大型 PDF 並進行多輪對話
- [`remote_pdf_analysis.py`](./document_understanding/remote_pdf_analysis.py)：遠端下載 PDF 論文進行深度研讀
- [`multi_pdf_comparison.py`](./document_understanding/multi_pdf_comparison.py)：多份 PDF 跨文件比對與表格輸出
- [`pdf_structured_extraction.py`](./document_understanding/pdf_structured_extraction.py)：結合 Pydantic 提取結構化規格資訊
- [`pdf_context_caching.py`](./document_understanding/pdf_context_caching.py)：Context Caching 快取長篇文件加速與節省 75% 成本
- [`pdf_understanding_tutorial.ipynb`](./document_understanding/pdf_understanding_tutorial.ipynb)：PDF 文件理解互動教學筆記本
- [`csv_document_caching.ipynb`](./document_understanding/csv_document_caching.ipynb)：CSV 數據快取與問答筆記本

---

### ⚙️ 第二階段：工程化與資料約束（應用開發必備）

#### [4. 結構化輸出 (structure_output)](./structure_output)
強制約束模型輸出嚴格符合 JSON Schema 或 Pydantic 模型，涵蓋條件多態 (`anyOf`/`Union`)、遞迴樹狀結構、串流 JSON 與 Enum 列舉。
- [`recipe_extractor.py`](./structure_output/recipe_extractor.py)：Pydantic 基礎資料萃取（Interactions API）
- [`advanced_schemas.py`](./structure_output/advanced_schemas.py)：條件多態結構 (`anyOf`/`Union`)、遞迴組織架構圖與串流 JSON
- [`currency_exchange_gradio.py`](./structure_output/currency_exchange_gradio.py)：牌告匯率結構化萃取與 Gradio 試算介面
- [`lesson1.ipynb`](./structure_output/lesson1.ipynb)：結構化輸出完整互動式教學筆記本
- [`exchange_rate_extraction.ipynb`](./structure_output/exchange_rate_extraction.ipynb)：牌告匯率網頁擷取與結構化轉換
- [`exchange_rate_to_csv.ipynb`](./structure_output/exchange_rate_to_csv.ipynb)：牌告匯率擷取並儲存為 CSV

---

### 🛠️ 第三階段：外掛能力與工具整合（突破 LLM 限制）

#### [5. 聯網搜尋 (ground_search)](./ground_search)
啟用 Google Search Grounding 讓模型自主聯網搜尋最新即時新聞、賽事與股價，自動標註來源網址，並可與 Code Execution / 結構化輸出混合使用。
- [`basic_search.py`](./ground_search/basic_search.py)：基礎 Google Search 聯網搜尋
- [`search_citations.py`](./ground_search/search_citations.py)：解析搜尋步驟與引用來源網址 (Sources & Citations)
- [`search_with_code_execution.py`](./ground_search/search_with_code_execution.py)：Google Search 搜尋即時數據 + Python 運算混合實戰
- [`search_structured_output.py`](./ground_search/search_structured_output.py)：Google Search 搜尋即時資訊 + Pydantic 結構化提取實戰

#### [6. 程式碼執行 (code_execution)](./code_execution)
模型自主在 Google 託管的 Python 安全沙盒中編寫並執行程式碼，解決算術幻覺、進行 CSV 運算、Matplotlib 圖表動態繪製與 Gemini 3 圖片局部裁切縮放。
- [`math_solver.py`](./code_execution/math_solver.py)：數學運算與質數演算法求解歷程
- [`currency_calculator.py`](./code_execution/currency_calculator.py)：載入 CSV 匯率表透過 Python 進行跨幣別換匯計算
- [`matplotlib_plotter.py`](./code_execution/matplotlib_plotter.py)：Matplotlib 圖表動態生成並接收輸出圖檔
- [`image_zoom_inspection.py`](./code_execution/image_zoom_inspection.py)：Gemini 3 圖片程式碼局部裁切縮放與視覺檢測
- [`math_and_code_execution.ipynb`](./code_execution/math_and_code_execution.ipynb)：程式碼執行與 Chat 互動教學筆記本
- [`currency_calculator.ipynb`](./code_execution/currency_calculator.ipynb)：牌告匯率 CSV 程式碼計算筆記本

#### [7. 函式呼叫 (function_calling)](./function_calling)
讓模型連接外部 API 與工具，涵蓋 4 步驟標準流程、平行呼叫、組合式鏈結、模式控制 (`AUTO`/`ANY`/`NONE`)、Google Search 聯網混合與多模態回傳。
- [`meeting_scheduler.py`](./function_calling/meeting_scheduler.py)：會議預約外部動作執行（標準 4 步驟流程）
- [`weather_assistant.py`](./function_calling/weather_assistant.py)：外部即時資料查詢與解析
- [`parallel_function_calling.py`](./function_calling/parallel_function_calling.py)：多設備平行呼叫與批量結果回傳
- [`multi_tool_search_and_function.py`](./function_calling/multi_tool_search_and_function.py)：Google Search 聯網與自訂工具混合使用
- [`basic_function_calling.ipynb`](./function_calling/basic_function_calling.ipynb)：基礎函式呼叫教學
- [`multi_function_calling.ipynb`](./function_calling/multi_function_calling.ipynb)：多函式自動路由與執行
- [`chat_function_history.ipynb`](./function_calling/chat_function_history.ipynb)：對話歷史與函式呼叫整合

---

### 🧠 第四階段：企業級記憶與 RAG 檢索（海量資料庫）

#### [8. 向量檢索 (embeddings)](./embeddings/document_search)
將文字/多模態內容轉為語意向量，涵蓋 `gemini-embedding-001`、多模態 `gemini-embedding-2`、Matryoshka (MRL) 維度縮減、多語 E5 與 ChromaDB 向量庫整合。
- [`gemini_semantic_similarity.py`](./embeddings/document_search/gemini_semantic_similarity.py)：文本向量嵌入與相似度矩陣
- [`gemini_document_retrieval.py`](./embeddings/document_search/gemini_document_retrieval.py)：知識庫非對稱語意檢索 (Top-K)
- [`dimension_reduction.py`](./embeddings/document_search/dimension_reduction.py)：Matryoshka 向量維度縮減 (3072 ➔ 768)
- [`document-search-e5.py`](./embeddings/document_search/document-search-e5.py)：Multilingual-E5 開源繁中向量模型檢索
- [`gemini_embedding_tutorial.ipynb`](./embeddings/document_search/gemini_embedding_tutorial.ipynb)：Gemini 向量嵌入與語意相似度互動教學
- [`pretrain_query_chromaDb/`](./embeddings/document_search/pretrain_query_chromaDb)：ChromaDB 向量資料庫實戰範例

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
