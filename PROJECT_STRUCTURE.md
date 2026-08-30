# 專案結構說明

本文件說明 Gemini-API 專案的目錄與檔案用途，方便快速找到對應範例。

---

## 根目錄

| 檔案 | 說明 |
|------|------|
| `README.md` | 專案總覽、環境設定、五大學習階段導覽與檔案速查 |
| `requirements.txt` | Python 依賴（核心與選用已分區註解） |
| `PROJECT_STRUCTURE.md` | 本檔案，專案結構說明 |

---

## 章節目錄概覽（依推薦學習路徑）

```
Gemini-API/
├── telegram_bot/              # 0. Telegram 機器人連線與 AI 助理串接
├── text_generation/          # 1. 文字生成（單輪、串流、Chat、Thinking）
├── image_generation/         # 2. 圖像生成（Imagen 3、比例控制、多模態）
├── document_understanding/   # 3. 文件理解（PDF、Files API、快取）
├── structure_output/        # 4. 結構化輸出（Pydantic、JSON Schema）
├── ground_search/           # 5. 聯網搜尋（Google Search 接地、事實查核）
├── code_execution/          # 6. 程式碼執行（Python 沙盒、Matplotlib）
├── function_calling/        # 7. 函式呼叫（外部 API、多工具協同）
├── embeddings/              # 8. 向量檢索（語意搜尋、ChromaDB）
│   └── document_search/
├── 何謂AIAgent/             # 9. AI 代理與工作流概念
└── 開源模型/                # 10. 開源大語言模型（Hugging Face）
```

---

## 各章節重點檔案

### 0. telegram_bot (Telegram 機器人)
- `README.md`：Telegram Bot 連線完整指南（涵蓋 Token 申請、Polling 輪詢機制、Webhook 生產部署考量、Gemini AI 助理串接）
- `basic_bot.py`：Telegram 基礎連線與 Echo 回覆範例（`python-telegram-bot` v20+ 非同步架構）
- `gemini_bot.py`：串接 Gemini 3.7 Flash Interactions API 的 Telegram AI 智慧對話助理

### 1. text_generation (文字生成)
- `README.md`：文字生成完整指南（劃分「Gemini 核心功能指南」與「實務應用整合實戰」兩大篇章）
- **核心功能教學（純 Python）**：
  - `01_basic_text.py`：基礎文字生成 (Zero-shot)
  - `02_thinking_mode.py`：思考模式與推理深度控制 (`thinking_level`)
  - `03_system_and_params.py`：系統指示詞與生成參數配置 (`temperature`, `max_output_tokens`)
  - `04_multimodal_image.py`：多模態圖文輸入與視覺分析 (PIL Image)
  - `05_streaming.py`：終端機即時打字機串流輸出 (`stream=True`)
  - `06_stateful_chat.py`：伺服器端狀態化多輪對話 (`previous_interaction_id`)
  - `07_stateless_chat.py`：客戶端無狀態多輪對話
  - `text_generation_quickstart.ipynb`：Interactions API 快速入門互動筆記本
  - `trip_planner_system_instruction.ipynb`：旅遊規劃與系統指示詞筆記本
  - `bear.jpg`、`organ.jpg`、`plant1.jpg` ~ `plant3.webp`：圖文問答範例圖片
- **實務應用整合（跨通道框架）**：
  - `app_telegram_bot.py`：Telegram 機器人（Polling 模式，支援文字與圖片問答）
  - `app_gradio.py`：Gradio 互動式 Web 介面（思考深度切換與串流多輪 Chat）
  - `app_streamlit.py`：Streamlit 互動式 Web 儀表板（側邊欄參數調節與即時對話）
  - `app_fastapi.py`：FastAPI 後端 API（RESTful `/generate` 與 SSE `/chat/stream` 串流）

### 2. image_generation (圖像生成)
- `README.md`：Imagen 3 與多模態圖像生成教學
- **核心教學**：
  - `01_text_to_image.py`：Imagen 3 基礎文字生成高品質圖片
  - `02_aspect_ratio.py`：自訂長寬比例（16:9、9:16、1:1）生成範例
  - `03_gemini_flash_image.py`：Gemini 2.5 Flash Image 多模態圖像生成
  - `04_prompt_enhancer.py`：Gemini 擴寫提示詞 ➔ 自動調用 Imagen 生成圖片的一條龍工作流
- **實務整合**：
  - `app_telegram_bot.py`：Telegram AI 算圖機器人
  - `app_gradio.py`：Gradio 藝術生圖工作台
  - `app_streamlit.py`：Streamlit 生圖工作室
  - `app_fastapi.py`：FastAPI 圖像生成 API 端點

### 3. document_understanding (文件理解)
- `README.md`：PDF 文件理解完整教學
- **核心教學**：
  - `01_inline_pdf_summary.py`：以 Inline 方式傳入 PDF 進行重點摘要
  - `02_files_api_pdf_chat.py`：Files API 上傳大型 PDF 並進行多輪對話問答
  - `03_remote_pdf_analysis.py`：從 URL 遠端下載 PDF 論文進行深度研讀
  - `04_multi_pdf_comparison.py`：多份 PDF 跨文件比對與 Markdown 表格輸出
  - `05_pdf_structured_extraction.py`：結合 Pydantic 提取結構化規格資訊
  - `06_pdf_context_caching.py`：Context Caching 長篇文件快取加速與節省成本
  - `pdf_understanding_tutorial.ipynb`：PDF 文件理解互動筆記本
  - `csv_document_caching.ipynb`：CSV 文件快取與問答筆記本
  - `說明書.pdf`：冷氣壁掛式使用說明書（4MB）
  - `aqx_p_488.csv`：空氣品質監測資料檔
- **實務整合**：
  - `app_telegram_bot.py`：Telegram PDF 研讀機器人
  - `app_gradio.py`：Gradio PDF 研讀與多輪問答介面
  - `app_streamlit.py`：Streamlit PDF 知識庫問答儀表板
  - `app_fastapi.py`：FastAPI PDF 分析微服務

### 4. structure_output (結構化輸出)
- `README.md`：JSON Schema 與 Pydantic 結構化輸出教學
- **核心教學**：
  - `01_pydantic_basic.py`：Pydantic 基礎食譜與食材萃取範例
  - `02_advanced_schemas.py`：遞迴樹狀結構 WBS 與 Enum 狀態列舉
  - `03_currency_exchange.py`：牌告匯率文字精確結構化轉換
  - `lesson1.ipynb`：結構化輸出完整互動教學筆記本
  - `exchange_rate_extraction.ipynb`：牌告匯率擷取與結構化轉換
  - `exchange_rate_to_csv.ipynb`：牌告匯率擷取並儲存為 CSV
  - `2025_01_29.csv`、`organ.jpg`：測試素材
- **實務整合**：
  - `app_telegram_bot.py`：Telegram 結構化食譜小幫手
  - `app_gradio.py`：Gradio 結構化表格轉換器
  - `app_streamlit.py`：Streamlit 結構化資料萃取與 CSV 下載工具
  - `app_fastapi.py`：FastAPI 強型別結構化輸出端點

### 5. ground_search (聯網搜尋)
- `README.md`：Google Search 聯網搜尋與事實查核教學
- **核心教學**：
  - `01_basic_search.py`：基礎 Google Search 聯網搜尋
  - `02_search_citations.py`：解析搜尋步驟與引用來源網址
  - `03_search_with_code_execution.py`：Google Search 搜尋即時數據 + Python 運算混合實戰
  - `04_search_structured_output.py`：Google Search 搜尋即時資訊 + Pydantic 結構化提取實戰
- **實務整合**：
  - `app_telegram_bot.py`：Telegram 即時聯網查證機器人
  - `app_gradio.py`：Gradio 聯網搜尋與來源查核介面
  - `app_streamlit.py`：Streamlit 即時情報與聯網搜尋儀表板
  - `app_fastapi.py`：FastAPI 聯網即時搜尋 API 微服務

### 6. code_execution (程式碼執行)
- `README.md`：程式碼執行與沙盒運算教學
- **核心教學**：
  - `01_math_solver.py`：數學質數計算與程式碼執行歷程
  - `02_currency_calculator.py`：載入 CSV 匯率表透過 Python 進行跨幣別換匯計算
  - `03_matplotlib_plotter.py`：Matplotlib 圖表動態生成並輸出
  - `04_image_zoom_inspection.py`：Gemini 3 圖片程式碼局部裁切縮放與視覺檢測
  - `math_and_code_execution.ipynb`：程式碼執行基礎與 Chat 整合筆記本
  - `currency_calculator.ipynb`：牌告匯率 CSV 程式碼計算筆記本
  - `2025_01_29.csv`：匯率範例資料檔
- **實務整合**：
  - `app_telegram_bot.py`：Telegram Python 運算解題機器人
  - `app_gradio.py`：Gradio Python 運算與繪圖沙盒工作台
  - `app_streamlit.py`：Streamlit Python 數據演算與圖表工作台
  - `app_fastapi.py`：FastAPI 程式碼沙盒運算 API 微服務

### 7. function_calling (函式呼叫)
- `README.md`：函式呼叫與工具自動路由教學
- **核心教學**：
  - `01_meeting_scheduler.py`：會議排程動作執行範例（標準 4 步驟）
  - `02_weather_assistant.py`：即時天氣查詢與解析範例
  - `03_parallel_function_calling.py`：多設備平行函式呼叫與批量結果回傳
  - `04_multi_tool_search_and_function.py`：Google Search 聯網搜尋與自訂工具混合使用
  - `basic_function_calling.ipynb`：基礎函式呼叫互動筆記本
  - `multi_function_calling.ipynb`：多函式自動路由筆記本
  - `parallel_function_calling.ipynb`：平行函式呼叫筆記本
  - `chat_function_history.ipynb`：對話歷史與函式呼叫整合
- **實務整合**：
  - `app_telegram_bot.py`：Telegram 智慧助理與函式呼叫機器人
  - `app_gradio.py`：Gradio 智慧家庭與工具調用控制台
  - `app_streamlit.py`：Streamlit AI 智慧管家工具儀表板
  - `app_fastapi.py`：FastAPI 函式呼叫與工具執行 API 微服務

### 8. embeddings/document_search (向量檢索)
- `README.md`：向量嵌入與語意搜尋教學
- **核心教學**：
  - `01_gemini_semantic_similarity.py`：文本向量相似度計算
  - `02_gemini_document_retrieval.py`：非對稱知識庫語意檢索 (Top-K)
  - `03_dimension_reduction.py`：Matryoshka 向量維度縮減 (3072 ➔ 768)
  - `04_document_search_e5.py`：Multilingual-E5 開源繁體中文向量搜尋
  - `gemini_embedding_tutorial.ipynb`：Gemini Embedding 基礎教學筆記本
  - `csv_semantic_search.ipynb`：CSV 文件向量搜尋筆記本
  - `001.csv`：說明文件範例資料
  - `Embeddings模型評測.xlsx`：繁體中文各家 Embedding 效果評測表
- **實務整合**：
  - `app_telegram_bot.py`：Telegram 企業知識庫 RAG 檢索機器人
  - `app_gradio.py`：Gradio 語意相似度與知識庫搜尋工作台
  - `app_streamlit.py`：Streamlit 語意檢索與知識庫問答儀表板
  - `app_fastapi.py`：FastAPI 向量嵌入與語意相似度 API 微服務

### 9. 何謂AIAgent (AI Agent 觀念)
- `README.md`：工作流類型（Prompt chaining、Routing、Parallelization 等）、Agent 概念與參考影片

### 10. 開源模型 (開源模型)
- `README.md`：Hugging Face serverless（如 Mistral-Nemo）、總結範例
- `text_to_summarization.py`、`test.ipynb`

---

## 📦 專案內建完整素材與資料檔 (Assets)

本專案已在各章節中附帶所有測試所需的完整素材檔案，學生 Clone 本專案後**無需自行上網尋找或下載任何素材**即可直接執行所有範例：

| 檔案名稱 | 所在目錄 | 檔案用途與適用範例 |
| :--- | :--- | :--- |
| `說明書.pdf` | `document_understanding/` | 富士通空調壁掛式說明書（4MB），用於 PDF 視覺理解、多輪問答、規格萃取與 Context Caching 快取。 |
| `aqx_p_488.csv` | `document_understanding/` | 全台空氣品質即時監測資料（134KB），用於 CSV 數據分析與文件快取。 |
| `2025_01_29.csv` | `structure_output/`<br>`code_execution/` | 臺灣銀行牌告匯率表格，用於 Pydantic 結構化提取與 Code Execution Python 精確換匯運算。 |
| `organ.jpg` | `structure_output/`<br>`text_generation/` | 管風琴樂器相片，用於多模態 Enum 列舉分類與圖片局部辨識。 |
| `bear.jpg` | `text_generation/` | 棕熊相片，用於文字與多模態圖文問答。 |
| `plant1.jpg` ~ `plant3.webp` | `text_generation/` | 植物與多模態圖片，用於圖文理解與植物辨識。 |
| `001.csv` | `embeddings/document_search/` | 產品與功能說明文章資料庫，用於向量嵌入與非對稱語意檢索。 |
| `embeddings.pkl` | `embeddings/.../pretrain_and_query/` | 預先計算好的向量資料檔，可直接載入進行快速比對。 |
| `Embeddings模型評測.xlsx` | `embeddings/document_search/` | 各家主流 Embedding 模型在繁體中文檢索上的評測對照表。 |

---

## 建議閱讀順序

1. 根目錄 `README.md`：環境配置與五大學習階段總覽
2. **第一階段（基礎與多模態）**：`text_generation/` ➔ `image_generation/` ➔ `document_understanding/`
3. **第二階段（工程化）**：`structure_output/`
4. **第三階段（外掛工具）**：`ground_search/` ➔ `code_execution/` ➔ `function_calling/`
5. **第四階段（RAG 檢索）**：`embeddings/document_search/`
6. **第五階段（進階 Agent）**：`何謂AIAgent/` ➔ `開源模型/`
