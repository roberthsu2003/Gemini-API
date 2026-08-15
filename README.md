# Gemini API 應用

本專案著重於 **Gemini API** 的介紹與實作，示範如何將 Google 大語言模型整合到專案中。

---

> **更新日期：2026-07** — 本專案已對齊 Gemini 3 世代模型與最新 [`google-genai`](https://github.com/googleapis/python-genai) SDK。
> 舊的 `google-generativeai`（`genai.configure` / `GenerativeModel`）SDK 已淘汰，請改用本文示範的 `from google import genai` 寫法。

## 環境需求

- **Python**：3.9+
- **套件**：見 [requirements.txt](./requirements.txt)  
  核心依賴：`google-genai`、`python-dotenv`、`ipywidgets`

安裝：

```bash
pip install -U google-genai python-dotenv ipywidgets
```

---

## 目前可用的模型（2026-07）

| 用途 | 建議模型 | 說明 |
|------|----------|------|
| **通用主力（本專案預設）** | `gemini-flash-latest` | 別名，永遠指向最新 Flash（目前為 Gemini 3.5 Flash）。速度、成本、能力平衡。 |
| 最新 Flash（明確版本） | `gemini-3.6-flash` | 2026-07 GA，token 效率更好、程式/代理任務更強。 |
| 高階推理 | `gemini-3.1-pro-preview` | 最強推理與長脈絡，適合複雜問題。 |
| 低成本高吞吐 | `gemini-3.5-flash-lite` | 最省、最快，適合大量簡單任務。 |
| 向量嵌入 | `gemini-embedding-001` | 支援 `task_type`、可調 `output_dimensionality`。 |
| 多模態嵌入 | `gemini-embedding-2` | 最新，支援文字/圖片/影片/音訊，但不支援 `task_type`。 |

> ⚠️ **已關閉/淘汰**：`gemini-2.0-flash-exp`、`gemini-2.0-flash`（2026-06-01 關閉）、`gemini-1.5-*` 全系列、`text-embedding-004`。本專案已全數更新，若你在舊筆記中看到這些名稱請一併替換。

---

## 快速開始

### 設定 API 金鑰

將 API 金鑰設為環境變數 `GEMINI_API_KEY`，SDK 會自動讀取。或於初始化時傳入：

```python
from google import genai
import os
from IPython.display import display, Markdown

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="AI 是如何工作的？（請使用繁體中文回答）"
)
display(Markdown(response.text))
```

### 關於「思考」功能（Gemini 3 世代）

Gemini 3 世代模型（含 `gemini-flash-latest`）預設會啟用思考模式，有助於回答品質，但會增加延遲與 token 用量。控制方式由舊版的 `thinking_budget`（數字）改為 **`thinking_level`**（`minimal` / `low` / `medium` / `high`）。想追求速度或降低成本時，調低層級：

```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="用幾句話說明 AI 如何運作",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)
print(response.text)
```

> 注意：Gemini 3 世代**不可同時**指定 `thinking_level` 與舊的 `thinking_budget`，且官方建議 `temperature` 維持預設 `1.0`（調動可能導致重複輸出或效能下降）。

---

## 官方資源

- [Google AI Studio](https://aistudio.google.com/prompts/new_chat)（測試與實驗）
- [Gemini API 模型列表](https://ai.google.dev/gemini-api/docs/models)
- [Gemini 3 開發者指南](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Python SDK（google-genai）](https://github.com/googleapis/python-genai)

---

## 專案章節導覽

| 章節 | 說明 | 路徑 |
|------|------|------|
| **何謂 AI Agent** | AI 代理與工作流概念 | [何謂AIAgent](./何謂AIAgent) |
| **1. 文字生成** | 單輪/串流/多輪對話、多模態 | [text_generation](./text_generation) |
| **2. 文件理解** | PDF 等文件讀取與分析 | [document_understanding](./document_understanding) |
| **3. 結構化輸出** | JSON 等結構化資料產生 | [structure_output](./structure_output) |
| **4. 程式碼執行** | 程式碼產生與執行 | [code_execution](./code_execution) |
| **5. 函式呼叫** | Function calling 範例與應用 | [function_calling](./function_calling) |
| **6. Embeddings** | 語意搜尋與向量檢索 | [embeddings/document_search](./embeddings/document_search) |
| **7. 開源模型** | Hugging Face 等非 Gemini 模型範例 | [開源模型](./開源模型) |

---

## 1. 文字生成 (text_generation)

- 統一採用官方推薦的 **Interactions API** (`client.interactions.create`)
- 單輪文字生成、串流回應（`stream=True` / `step.delta`）
- 伺服器端狀態化多輪對話（`previous_interaction_id`）與無狀態對話（`store=False`）
- 多模態圖文輸入、思考模式（`thinking_level`）與系統指示（`system_instruction`）
- 範例：Zero-shot、總結、翻譯、旅遊規劃、Gradio 介面整合等

詳見 [text_generation/README.md](./text_generation/README.md)。

---

## 2. 文件理解 (document_understanding)

- PDF（遠端/本機、大檔案）
- 摘要、問答、結構化擷取

詳見 [document_understanding/README.md](./document_understanding/README.md)。

---

## 3. 結構化輸出 (structure_output)

- 指定 JSON schema 產出
- 列舉與格式控制

詳見 [structure_output/README.md](./structure_output/README.md)。

---

## 4. 程式碼執行 (code_execution)

- 產生並執行 Python 程式碼
- Chat 內使用 code execution、匯率換算等範例

詳見 [code_execution/README.md](./code_execution/README.md)。

---

## 5. 函式呼叫 (function_calling)

- [最簡單範例](./function_calling/simple_sample.ipynb)
- [範例 1：匯率（自動呼叫）](./function_calling/example1)
- [範例 2：匯率（手動呼叫）](./function_calling/example2)
- [Gradio 範例](./function_calling/gradio_example1)
- [多函式](./function_calling/multiFunction.ipynb)
- [ChatSession.history](./function_calling/history.ipynb)
- [手動管理函式呼叫](./function_calling/manual_function_calling.ipynb)
- [鏈結呼叫](./function_calling/function_calling_chain.ipynb)
- [平行呼叫](./function_calling/parallel_function_call.ipynb)
- [從結構化資料擷取](./function_calling/extract_structured_data.ipynb)

詳見 [function_calling/README.md](./function_calling/README.md)。

---

## 6. Embeddings（語意搜尋）

- Gemini `gemini-embedding-001`、多語 E5 等
- 文件搜尋、預訓練與查詢、ChromaDB 整合

詳見 [embeddings/document_search/README.md](./embeddings/document_search/README.md)。

---

## 7. 開源模型

- Hugging Face Inference API 等 serverless 模型範例（如 Mistral-Nemo）
- 總結等應用

詳見 [開源模型/README.md](./開源模型/README.md)。

---

## 專案結構總覽

目錄樹與說明見 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。
