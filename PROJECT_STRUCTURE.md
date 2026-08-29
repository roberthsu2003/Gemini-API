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

### 1. text_generation (文字生成)
- `README.md`：文字生成完整指南（涵蓋 Interactions API、Thinking 思考控制、System Instructions、多模態、即時串流、多輪狀態對話與最佳實踐）
- `zero_shot.py`：Zero-shot 文字生成與 Gradio 互動介面
- `text_streaming.py`：即時打字機串流生成（SSE 事件監聽）
- `chat.py`：伺服器端狀態管理（`previous_interaction_id`）多輪串流對話
- `image_text.py`：多模態圖文問答分析介面
- `text_to_summarization.py`：文章摘要與語氣風格控制
- `text_generation_quickstart.ipynb`：Interactions API 快速入門互動筆記本
- `trip_planner_system_instruction.ipynb`：旅遊規劃與系統指示詞筆記本
- `organ.jpg`、`bear.jpg`、`plant1.jpg` ~ `plant3.webp`：圖文問答範例圖片

### 2. image_generation (圖像生成)
- `README.md`：Imagen 3 與多模態圖像生成教學（涵蓋 Text-to-Image、長寬比控制、gemini-2.5-flash-image 與 Prompt 擴寫產圖工作流）
- `text_to_image_imagen.py`：Imagen 3 基礎文字生成高品質圖片
- `aspect_ratio_control.py`：自訂長寬比例（16:9、9:16、1:1）生成範例
- `gemini_flash_image.py`：Gemini 2.5 Flash Image 多模態圖像生成
- `prompt_enhancer_and_generator.py`：Gemini 擴寫提示詞 ➔ 自動調用 Imagen 生成圖片的一條龍工作流

### 3. document_understanding (文件理解)
- `README.md`：PDF 文件理解完整教學（涵蓋 Inline PDF、Files API、URL 遠端載入、多文件比對、結構化萃取與 Context Caching）
- `inline_pdf_summary.py`：以 Inline 方式傳入 PDF 進行重點摘要
- `files_api_pdf_chat.py`：Files API 上傳大型 PDF 並進行多輪對話問答
- `remote_pdf_analysis.py`：從 URL 遠端下載 PDF 論文並由 Gemini 進行深度剖析
- `multi_pdf_comparison.py`：多份 PDF 跨文件比對與 Markdown 表格輸出
- `pdf_structured_extraction.py`：結合 Pydantic 從 PDF 中提取結構化規格資訊
- `pdf_context_caching.py`：超長文件 Context Caching 快取加速與節省 Token 成本
- `pdf_understanding_tutorial.ipynb`：PDF 文件理解互動筆記本
- `csv_document_caching.ipynb`：CSV 文件快取與問答筆記本
- `說明書.pdf`：冷氣機使用說明書範例 PDF（4MB）
- `aqx_p_488.csv`：空氣品質範例資料檔（134KB）

### 4. structure_output (結構化輸出)
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

### 5. ground_search (聯網搜尋)
- `README.md`：Google Search 聯網搜尋與事實查核教學（涵蓋即時搜尋、來源引用、Code Execution 混合、Pydantic 結構化）
- `basic_search.py`：基礎 Google Search 聯網搜尋範例
- `search_citations.py`：解析搜尋步驟與引用來源網址範例
- `search_with_code_execution.py`：Google Search 搜尋與 Python 運算混合實戰
- `search_structured_output.py`：Google Search 搜尋與 Pydantic 結構化提取實戰

### 6. code_execution (程式碼執行)
- `README.md`：程式碼執行完整教學（涵蓋數學運算、多輪對話、圖片縮放檢驗、CSV 數據計算、Matplotlib 圖表繪製與聯網整合）
- `math_solver.py`：數學質數計算與程式碼執行歷程解析
- `currency_calculator.py`：載入 CSV 匯率表並透過 Python 進行跨幣別換匯精確計算
- `matplotlib_plotter.py`：Matplotlib 圖表動態生成並儲存 inline 圖片
- `image_zoom_inspection.py`：Gemini 3 圖片程式碼局部裁切縮放與視覺分析
- `math_and_code_execution.ipynb`：程式碼執行基礎與 Chat 整合筆記本
- `currency_calculator.ipynb`：牌告匯率 CSV 程式碼計算筆記本
- `2025_01_29.csv`：匯率範例資料檔

### 7. function_calling (函式呼叫)
- `README.md`：函式呼叫完整教學（涵蓋 4 步驟標準流程、平行呼叫、組合式決策、模式控制、聯網混合與多模態回傳）
- `meeting_scheduler.py`：會議排程動作執行範例（Interactions API 4 步驟）
- `weather_assistant.py`：即時天氣知識查詢與解析範例
- `parallel_function_calling.py`：多設備平行函式呼叫與批量結果回傳範例
- `multi_tool_search_and_function.py`：Google Search 聯網搜尋與自訂 Function Calling 混合使用範例
- `basic_function_calling.ipynb`：基礎函式呼叫互動筆記本
- `multi_function_calling.ipynb`：多函式自動路由與執行
- `chat_function_history.ipynb`：多輪對話歷史紀錄與函式呼叫
- `manual_function_calling.ipynb`：手動解析 Function Call 與執行回傳
- `function_calling_chain.ipynb`：多步驟鏈式函式呼叫工作流
- `parallel_function_calling.ipynb`：平行函式呼叫筆記本
- `extract_structured_data.ipynb`：透過 Function Calling 提取結構化資料
- `example1/`：臺灣銀行牌告匯率自動呼叫範例
- `example2/`：臺灣銀行牌告匯率手動呼叫範例
- `gradio_example1/`：Gradio 互動式介面整合範例

### 8. embeddings/document_search (向量檢索)
- `README.md`：向量嵌入與語意搜尋教學（涵蓋 gemini-embedding-001/002、MRL 維度縮減、Task Types、多語 E5 與 ChromaDB 整合）
- `gemini_semantic_similarity.py`：Gemini 文本向量相似度計算與矩陣生成
- `gemini_document_retrieval.py`：非對稱知識庫語意檢索 (Top-K) 排序
- `dimension_reduction.py`：Matryoshka 向量維度縮減 (3072 ➔ 768) 示範
- `document-search-e5.py`：Multilingual-E5 開源繁體中文向量搜尋腳本
- `gemini_embedding_tutorial.ipynb`：Gemini Embedding 基礎教學筆記本
- `csv_semantic_search.ipynb`：CSV 文件向量搜尋筆記本
- `multilingual_e5_test.ipynb`：Multilingual-E5 繁中測試筆記本
- `multilingual_e5_advanced.ipynb`：Multilingual-E5 進階筆記本
- `embedding_benchmark.ipynb`：向量模型評測筆記本
- `pretrain_and_query/`：CSV + pkl 預先向量化與快速查詢
- `pretrain_query_chromaDb/`：ChromaDB 向量資料庫實戰範例
- `001.csv`：說明文件範例資料
- `Embeddings模型評測.xlsx`：繁體中文各家 Embedding 效果評測表

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
