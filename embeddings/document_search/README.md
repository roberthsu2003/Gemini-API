# 🧠 向量檢索與語意搜尋 (Embeddings & Document Retrieval)

透過 **Gemini Embedding 模型 (`gemini-embedding-001`)**，可將文字、文章或技術文件轉換為高維度語意向量（Vector Embeddings）。藉由計算向量之間的幾何距離或餘弦相似度（Cosine Similarity），實現超脫傳統關鍵字比對的**智慧語意搜尋**與**檢索增強生成 (RAG)**。

> 📖 **官方說明**：
> `gemini-embedding-001` 預設輸出 3072 維度，支援透過 `task_type`（如 `RETRIEVAL_QUERY`、`RETRIEVAL_DOCUMENT`、`SEMANTIC_SIMILARITY`）優化特定任務，並支援 Matryoshka (MRL) 彈性縮減維度（如 768 或 512）。
> 官方文件：[Embeddings - Google AI for Developers](https://ai.google.dev/gemini-api/docs/embeddings)

---

## 📑 目錄導覽

1. [文本向量嵌入與語意相似度 (01_gemini_semantic_similarity.py)](#1-文本向量嵌入與語意相似度-01_gemini_semantic_similaritypy)
2. [知識庫非對稱語意檢索 (02_gemini_document_retrieval.py)](#2-知識庫非對稱語意檢索-02_gemini_document_retrievalpy)
3. [Matryoshka 向量維度縮減 (03_dimension_reduction.py)](#3-matryoshka-向量維度縮減-03_dimension_reductionpy)
4. [開源 Multilingual-E5 繁中模型 (04_document_search_e5.py)](#4-開源-multilingual-e5-繁中模型-04_document_search_e5py)
5. [課堂互動筆記本 (Jupyter Notebooks)](#5-課堂互動筆記本-jupyter-notebooks)

---

## 1. 文本向量嵌入與語意相似度 (`01_gemini_semantic_similarity.py`)

使用 `gemini-embedding-001` 取得文字向量並計算語意相似度：

- 核心程式檔案：[`01_gemini_semantic_similarity.py`](./01_gemini_semantic_similarity.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from google import genai
import numpy as np

client = genai.Client()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

texts = [
    "人工智慧正在改變軟體開發流程。",
    "大語言模型正在重塑現代程式設計架構。",
    "今天陽明山的天氣非常晴朗。"
]

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
)

embeddings = [np.array(e.values) for e in response.embeddings]
print("相似度 (1 vs 2):", cosine_similarity(embeddings[0], embeddings[1]))
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我開發 Gradio 語意相似度比對工具：
1. 提供兩個文字輸入框（句子 A 與 句子 B）。
2. 呼叫 gemini-embedding-001 取得向量並計算餘弦相似度分數（0.0 ~ 1.0）。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit 知識庫語意搜尋儀表板：
1. 側邊欄提供自訂維度下拉選單 (3072, 768, 512)。
2. 主畫面輸入查詢問題，動態計算與知識庫條目的相似度並以表格排行展示。
```

**Telegram Bot 知識庫問答 Prompt：**
```text
請幫我建立 Telegram 知識庫檢索機器人：
1. 預先建立知識庫文件的 Embedding。
2. 接收用戶提問時計算 Query 向量，比對並回傳相關度最高的知識條目。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/embed 與 POST /api/similarity 端點：
1. 封裝 Gemini Embedding 取得向量。
2. 支援傳入兩段文字計算相似度分數並回傳 JSON。
```
</details>

---

## 2. 知識庫非對稱語意檢索 (`02_gemini_document_retrieval.py`)

設定 `task_type="RETRIEVAL_DOCUMENT"` 與 `task_type="RETRIEVAL_QUERY"` 實現精確非對稱檢索：

- 核心程式檔案：[`02_gemini_document_retrieval.py`](./02_gemini_document_retrieval.py)
- 實務應用範例：[`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

---

## 3. Matryoshka 向量維度縮減 (`03_dimension_reduction.py`)

透過 `output_dimensionality` 彈性降低維度，節省 75% 向量儲存空間：

- 核心程式檔案：[`03_dimension_reduction.py`](./03_dimension_reduction.py)

---

## 4. 開源 Multilingual-E5 繁中模型 (`04_document_search_e5.py`)

- 核心程式檔案：[`04_document_search_e5.py`](./04_document_search_e5.py)

---

## 5. 課堂互動筆記本 (Jupyter Notebooks)

- [`gemini_embedding_tutorial.ipynb`](./gemini_embedding_tutorial.ipynb)：Gemini 向量嵌入互動教學
- [`csv_semantic_search.ipynb`](./csv_semantic_search.ipynb)：CSV 語意檢索筆記本
- [`embedding_benchmark.ipynb`](./embedding_benchmark.ipynb)：模型評測筆記本
- [`multilingual_e5_advanced.ipynb`](./multilingual_e5_advanced.ipynb)：Multilingual E5 筆記本
