# Gemini API 應用實戰指南

本專案全面介紹與實作 **Google Gemini API**，示範如何將 Google 最新的 Gemini 3 世代大語言模型與強大工具整合到各類 Python 應用程式與 AI Agent 工作流程中。

---

> **專案版本更新（2026 最新規範）**：
> - 全面採用 Google 官方推薦的 **Interactions API** (`client.interactions.create`) 與最新 [`google-genai`](https://github.com/googleapis/python-genai) SDK。
> - 支援 **Gemini 3** 最新模型（`gemini-3.7-flash`、`gemini-3.5-flash-lite`、`gemini-3.1-pro-preview` 等）。
> - 每個單元均提供可直接執行的 Python 腳本、Jupyter Notebook，並附帶 **AI 賦能提示詞 (Prompts)**，方便一鍵利用 AI 生成 Gradio 或 Streamlit 視覺化 Web 介面。

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

## 📚 專案核心章節導覽

| 章節 | 核心主題 | 重點內容與範例 | 目錄路徑 |
|---|---|---|---|
| **0. 何謂 AI Agent** | 代理觀念與架構 | Prompt chaining、Routing、Parallelization、Evaluator-optimizer 等設計模式 | [何謂AIAgent](./何謂AIAgent) |
| **1. 文字生成** | Text Generation | 單輪生成、即時串流 (`step.delta`)、狀態化多輪對話、多模態圖文分析 | [text_generation](./text_generation) |
| **2. 文件理解** | Document Understanding | 本機/遠端 PDF 文件解析、長篇文件摘要、表格萃取與快取機制 | [document_understanding](./document_understanding) |
| **3. 結構化輸出** | Structured Outputs | JSON Schema 強制約束、Pydantic / Zod 型別驗證、多態 (`Union`)、遞迴樹狀結構與串流 JSON | [structure_output](./structure_output) |
| **4. 程式碼執行** | Code Execution | 內建 Python 執行沙盒、數據運算、演算法驗證與圖表繪製 | [code_execution](./code_execution) |
| **5. 函式呼叫** | Function Calling | 4 步驟標準流程、平行呼叫、組合式鏈結、模式控制 (`AUTO`/`ANY`)、聯網工具混合與多模態回傳 | [function_calling](./function_calling) |
| **6. 向量檢索** | Embeddings & Search | `gemini-embedding-001`、多語 E5、ChromaDB 向量資料庫與語意搜尋 | [embeddings/document_search](./embeddings/document_search) |
| **7. 開源模型** | Open Source Models | Hugging Face Serverless Inference API 整合實作 | [開源模型](./開源模型) |

---

## 📂 各章節核心實作檔案速查

### [1. 文字生成 (text_generation)](./text_generation)
- [`zero_shot.py`](./text_generation/zero_shot.py)：零樣本文字生成
- [`text_streaming.py`](./text_generation/text_streaming.py)：即時 Token 串流輸出
- [`chat.py`](./text_generation/chat.py)：伺服器端狀態化多輪對話
- [`image_text.py`](./text_generation/image_text.py)：多模態圖文綜合理解
- [`text_to_summarization.py`](./text_generation/text_to_summarization.py)：長文本重點摘要

### [2. 文件理解 (document_understanding)](./document_understanding)
- [`demo1.ipynb`](./document_understanding/demo1.ipynb)：本機與遠端 PDF 文件分析與問答
- [`demo2.ipynb`](./document_understanding/demo2.ipynb)：多頁大檔案處理與長上下文摘要

### [3. 結構化輸出 (structure_output)](./structure_output)
- [`recipe_extractor.py`](./structure_output/recipe_extractor.py)：Pydantic 基礎資料萃取（Interactions API）
- [`advanced_schemas.py`](./structure_output/advanced_schemas.py)：條件多態結構 (`anyOf`/`Union`)、遞迴組織架構圖與串流 JSON
- [`currency_exchange_gradio.py`](./structure_output/currency_exchange_gradio.py)：牌告匯率結構化萃取與 Gradio 試算介面
- [`lesson1.ipynb`](./structure_output/lesson1.ipynb)：結構化輸出完整互動式教學筆記本

### [4. 程式碼執行 (code_execution)](./code_execution)
- [`math_solver.py`](./code_execution/math_solver.py)：數學運算與演算法求解歷程
- [`currency_calculator.py`](./code_execution/currency_calculator.py)：載入 CSV 匯率表透過 Python 進行跨幣別換匯計算
- [`matplotlib_plotter.py`](./code_execution/matplotlib_plotter.py)：Matplotlib 圖表動態生成並接收輸出圖檔
- [`image_zoom_inspection.py`](./code_execution/image_zoom_inspection.py)：Gemini 3 圖片程式碼局部裁切縮放與視覺檢測
- [`math_and_code_execution.ipynb`](./code_execution/math_and_code_execution.ipynb)：程式碼執行與 Chat 互動教學筆記本

### [5. 函式呼叫 (function_calling)](./function_calling)
- [`meeting_scheduler.py`](./function_calling/meeting_scheduler.py)：會議預約外部動作執行（標準 4 步驟流程）
- [`weather_assistant.py`](./function_calling/weather_assistant.py)：外部即時資料查詢與解析
- [`parallel_function_calling.py`](./function_calling/parallel_function_calling.py)：多設備平行呼叫與批量結果回傳
- [`multi_tool_search_and_function.py`](./function_calling/multi_tool_search_and_function.py)：Google Search 聯網與自訂工具混合使用
- [`basic_function_calling.ipynb`](./function_calling/basic_function_calling.ipynb)：基礎函式呼叫教學
- [`multi_function_calling.ipynb`](./function_calling/multi_function_calling.ipynb)：多函式自動路由與執行
- [`chat_function_history.ipynb`](./function_calling/chat_function_history.ipynb)：對話歷史與函式呼叫整合

### [6. 向量檢索 (embeddings)](./embeddings/document_search)
- [`document-search-e5.py`](./embeddings/document_search/document-search-e5.py)：多語向量模型檢索
- [`document_search.ipynb`](./embeddings/document_search/document_search.ipynb)：Gemini 向量嵌入與語意相似度計算

---

## 🔗 官方參考文件

- [Google AI Studio 實驗室](https://aistudio.google.com/)
- [Gemini API 官方開發者文件](https://ai.google.dev/gemini-api/docs)
- [Interactions API 指南](https://ai.google.dev/gemini-api/docs/interactions)
- [Structured Outputs 指南](https://aistudio.google.com/docs/structured-output)
- [Function Calling 指南](https://aistudio.google.com/docs/function-calling)
- [Google GenAI Python SDK (GitHub)](https://github.com/googleapis/python-genai)

---

## 📖 專案結構細節

詳細目錄樹結構與各檔案詳細介紹請參閱 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。
