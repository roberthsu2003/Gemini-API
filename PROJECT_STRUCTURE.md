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
- `README.md`：JSON schema、列舉、實作範例
- `lesson1.ipynb`、`demo1.py`、`demo4.py`、`test*.ipynb`
- `2025_01_29.csv`：範例資料

### code_execution
- `README.md`：code execution 啟用方式、Chat 內使用、匯率範例
- `lesson1.ipynb`、`demo1.ipynb`～`demo4.ipynb`、`demo2.py`
- `2025_01_29.csv`：匯率範例資料

### function_calling
- `README.md`：函式呼叫總覽
- `simple_sample.ipynb`、`multiFunction.ipynb`、`history.ipynb`
- `manual_function_calling.ipynb`、`function_calling_chain.ipynb`、`parallel_function_call.ipynb`、`extract_structured_data.ipynb`
- `example1/`：匯率自動呼叫；`example2/`：手動呼叫
- `gradio_example1/`：Gradio 介面範例

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
