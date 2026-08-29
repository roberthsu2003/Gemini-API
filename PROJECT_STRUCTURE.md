# 專案結構說明

本文件說明 Gemini-API 專案的目錄與檔案用途，方便快速找到對應範例。

---

## 根目錄

| 檔案 | 說明 |
|------|------|
| `README.md` | 專案總覽、環境設定、章節導覽 |
| `requirements.txt` | Python 依賴（核心與選用已分區註解） |
| `PROJECT_STRUCTURE.md` | 本檔案，專案結構說明 |

---

## 章節目錄概覽

```
Gemini-API/
├── 何謂AIAgent/          # AI 代理與工作流概念
├── text_generation/      # 1. 文字生成（單輪、串流、Chat、多模態）
├── document_understanding/  # 2. 文件理解（PDF 等）
├── structure_output/     # 3. 結構化輸出（JSON schema）
├── code_execution/       # 4. 程式碼產生與執行
├── function_calling/     # 5. 函式呼叫（含 Gradio 範例）
├── embeddings/           # 6. Embeddings 與語意搜尋
│   └── document_search/
└── 開源模型/             # 7. 非 Gemini 模型（如 Hugging Face）
```

---

## 各章節重點檔案

### 何謂AIAgent
- `README.md`：工作流類型（Prompt chaining、Routing、Parallelization 等）、Agent 概念與參考影片

### text_generation
- `README.md`：完整文字生成教學（含參數說明）
- `zero_shot.py`、`text_streaming.py`、`chat.py`、`image_text.py`、`text_to_summarization.py`
- `quickstart.ipynb`、`tripPlanner.ipynb`

### document_understanding
- `README.md`：PDF 遠端/本機、大檔案、暫存與 cache
- `demo1.ipynb`、`demo2.ipynb`
- `aqx_p_488.csv`：範例資料

### structure_output
- `README.md`：JSON Schema 結構化輸出教學（含 Interactions API、Pydantic、多態、遞迴、串流與工具整合）
- `recipe_extractor.py`：Pydantic 基礎食譜與食材萃取範例
- `advanced_schemas.py`：條件分支 (anyOf/Union 內容審查)、遞迴架構圖與串流輸出範例
- `currency_exchange_gradio.py`：臺灣銀行牌告匯率提取與 Gradio 換算介面
- `lesson1.ipynb`：結構化輸出完整互動筆記本教學（Prompt Schema、Pydantic、Enum 分類等）
- `exchange_rate_extraction.ipynb`：牌告匯率網頁擷取與 Pydantic 結構化轉換
- `exchange_rate_to_csv.ipynb`：牌告匯率擷取並轉換儲存為 CSV
- `article_content_extraction.ipynb`：新聞文章內容擷取與整理
- `web_link_extraction.ipynb`：網頁指定超連結擷取
- `2025_01_29.csv`：牌告匯率範例資料
- `organ.jpg`：樂器分類範例圖片

### code_execution
- `README.md`：程式碼執行完整教學（涵蓋數學運算、多輪對話、圖片縮放檢驗、CSV 數據計算、Matplotlib 圖表繪製與聯網整合）
- `math_solver.py`：數學質數計算與程式碼執行歷程解析
- `currency_calculator.py`：載入 CSV 匯率表並透過 Python 進行跨幣別換匯精確計算
- `matplotlib_plotter.py`：Matplotlib 圖表動態生成並儲存 inline 圖片
- `image_zoom_inspection.py`：Gemini 3 圖片程式碼局部裁切縮放與視覺分析
- `math_and_code_execution.ipynb`：程式碼執行基礎與 Chat 整合筆記本
- `currency_calculator.ipynb`：牌告匯率 CSV 程式碼計算筆記本
- `2025_01_29.csv`：匯率範例資料檔

### function_calling
- `README.md`：函式呼叫完整教學（涵蓋 4 步驟標準流程、平行呼叫、組合式決策、模式控制、聯網混合與多模態回傳）
- `meeting_scheduler.py`：會議排程動作執行範例（Interactions API 4 步驟）
- `weather_assistant.py`：即時天氣知識查詢與解析範例
- `parallel_function_calling.py`：多設備平行函式呼叫與批量結果回傳範例
- `multi_tool_search_and_function.py`：Google Search 聯網搜尋與自訂 Function Calling 混合使用範例
- `basic_function_calling.ipynb`：基礎函式呼叫互動筆記本
- `multi_function_calling.ipynb`：多函式自動選擇與執行
- `chat_function_history.ipynb`：多輪對話歷史紀錄與函式呼叫
- `manual_function_calling.ipynb`：手動解析 Function Call 與執行回傳
- `function_calling_chain.ipynb`：多步驟鏈式函式呼叫工作流
- `parallel_function_calling.ipynb`：平行函式呼叫筆記本
- `extract_structured_data.ipynb`：透過 Function Calling 提取結構化資料
- `example1/`：臺灣銀行牌告匯率自動呼叫範例
- `example2/`：臺灣銀行牌告匯率手動呼叫範例
- `gradio_example1/`：Gradio 互動式介面整合範例

### embeddings/document_search
- `README.md`：Gemini embedding、多語 E5、ChromaDB
- `document_search*.ipynb`、`document-search-e5.py`
- `pretrain_and_query/`：CSV + pkl 預訓練與查詢
- `pretrain_query_chromaDb/`：ChromaDB 向量庫範例
- `001.csv`：範例資料

### 開源模型
- `README.md`：Hugging Face serverless（如 Mistral-Nemo）、總結範例
- `text_to_summarization.py`、`test.ipynb`

---

## 範例資料檔

- `*.csv`：多處用於匯率、結構化輸出、embedding 等範例（如 `2025_01_29.csv`、`001.csv`）
- 各子目錄的 `README.md` 若提到 `./images/`，表示需自行準備截圖或示意圖（專案中未附圖片檔）

---

## 建議閱讀順序

1. 根目錄 `README.md`：環境與快速開始  
2. `text_generation/README.md`：基本呼叫與參數  
3. 依需求進入：文件理解、結構化輸出、程式碼執行、函式呼叫、Embeddings、開源模型  
4. 各章節內 `.ipynb` 與 `.py` 為可執行範例，建議搭配對應 `README.md` 閱讀  
