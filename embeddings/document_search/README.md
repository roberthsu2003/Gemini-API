# 向量嵌入與語意搜尋 (Embeddings & Semantic Search)

**向量嵌入 (Embeddings)** 是將文字、圖片或音訊等非結構化資料，轉換為具備語意資訊的數值向量（高維浮點數陣列）。

與傳統基於關鍵字精確匹配的搜尋技術相比，語意搜尋能夠理解使用者的**查詢意圖**、**同義詞**、**上下文關聯**與**跨語言表達**，是構建 **RAG（檢索增強生成）**、知識庫問答、智慧推薦與分類系統的核心基石。

---

## 核心模型選擇

| 模型名稱 | 模態支援 | 核心特色 | 推薦使用場景 |
|---|---|---|---|
| **`gemini-embedding-001`** | 純文字 | 支援原生 `task_type` 參數與 MRL 維度控制 (`output_dimensionality`)。 | 文字知識庫檢索、FAQ 比對、問答系統、對稱相似度計算。 |
| **`gemini-embedding-2`** | 文字、圖片、影片、音訊、文件 | 最新多模態統一向量空間，支援跨模態搜尋（圖搜文、文搜圖），透過 Prompt 前綴自訂任務指令。 | 多模態檢索、圖片/商品搜尋、影片音訊內容關聯分析。 |

> ⚠️ **淘汰提醒**：舊版 `text-embedding-004` 已淘汰，請全面改用 `gemini-embedding-001` 或 `gemini-embedding-2`。

---

## 1. 快速開始：文本向量嵌入與相似度矩陣 (Semantic Similarity)

使用 `gemini-embedding-001` 計算不同句子之間的語意向量，並透過餘弦相似度（Cosine Similarity）評估語意相近程度。

```python
import os
from google import genai
from google.genai import types
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

sentences = [
    "生命的意義是什麼？",
    "人類存在的目的是什麼？",
    "如何烤出美味的巧克力蛋糕？",
    "製作甜點與烘焙蛋糕的食譜有哪些？",
    "量子電腦如何改變加密技術？",
]

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=sentences,
    config=types.EmbedContentConfig(
        task_type="SEMANTIC_SIMILARITY",
        output_dimensionality=768,
    ),
)

# 取得向量並計算相似度矩陣
embeddings = [e.values for e in result.embeddings]
df_sim = pd.DataFrame(
    cosine_similarity(embeddings),
    index=[f"S{i+1}" for i in range(len(sentences))],
    columns=[f"S{i+1}" for i in range(len(sentences))],
)
print(df_sim.round(4))
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：語意相似度比對與重複內容偵測介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Gemini 向量相似度程式改寫為 Gradio 應用：
1. 介面提供兩個文字輸入框（句子 A 與 句子 B）。
2. 呼叫 gemini-embedding-001 計算兩個句子的向量與餘弦相似度分數（0% ~ 100%）。
3. 介面以進度條（gr.Progress / gr.Slider）呈現相似度，並以色彩標記是否為高度重複內容（> 85% 標記紅色）。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 文本語意矩陣視覺化應用：
1. 提供多行輸入框讓使用者輸入多個句子（每行一句）。
2. 計算兩兩之間的 Cosine Similarity 矩陣。
3. 使用 Seaborn / Plotly 繪製熱力圖 (Heatmap)，直觀展示句子間的語意距離分佈。
```
</details>

---

## 2. 非對稱知識庫檢索 (Asymmetric Document Retrieval)

在文件檢索情境中，使用者的「查詢字串（短問句）」與知識庫的「文件段落（長文本）」在結構上通常是不對稱的。
- 知識庫文件索引時：設定 `task_type="RETRIEVAL_DOCUMENT"`
- 使用者提出查詢時：設定 `task_type="RETRIEVAL_QUERY"`

```python
import os
from google import genai
from google.genai import types
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

documents = [
    {"title": "空調保養", "text": "定期清洗空氣過濾網能維持冷房效果並節省電力。建議每兩週拆下水洗。"},
    {"title": "異常排除", "text": "若指示燈閃爍且無法吹出冷風，請先拔掉電源並聯絡授權維修人員。"},
    {"title": "咖啡烘焙", "text": "中度烘焙能保留咖啡豆的果香與酸甜感，適合手沖與虹吸壺萃取。"},
]

# 1. 文件建立索引 (RETRIEVAL_DOCUMENT)
doc_texts = [f"Title: {d['title']}\nContent: {d['text']}" for d in documents]
doc_res = client.models.embed_content(
    model="gemini-embedding-001",
    contents=doc_texts,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768),
)
doc_vectors = np.array([e.values for e in doc_res.embeddings])

# 2. 查詢檢索 (RETRIEVAL_QUERY)
query = "冷氣如果故障不會冷要如何處理？"
query_res = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY", output_dimensionality=768),
)
query_vec = np.array(query_res.embeddings[0].values).reshape(1, -1)

# 3. 相似度排序
sims = cosine_similarity(query_vec, doc_vectors)[0]
top_idx = np.argsort(sims)[::-1]

for rank, idx in enumerate(top_idx, 1):
    print(f"Top {rank} [相似度: {sims[idx]:.4f}] {documents[idx]['title']}: {documents[idx]['text']}")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧知識庫檢索與問答問詢台</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「非對稱語意檢索」改寫為 Gradio 知識庫問答應用：
1. 側邊欄支援上傳 FAQ CSV 檔案（包含 title, content 欄位），系統自動建立向量索引。
2. 主畫面提供搜尋輸入框，使用者輸入口語化問題。
3. 介面以卡片方式呈現 Top-3 相關度最高的文件條目，並附帶匹配信心度分數。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 語意搜尋後台：
1. 支援載入 001.csv 知識庫資料並將向量快取在 st.session_state。
2. 主畫面搜尋輸入後，以 st.expander 展開最符合的前 3 筆資料，並提供使用者點選「向 Gemini 生成總結回答」。
```
</details>

---

## 3. 多模態向量嵌入 (`gemini-embedding-2`)

`gemini-embedding-2` 是最新的多模態嵌入模型，能將文字、圖片、視訊與音訊對齊到同一個向量空間，支援**跨模態檢索**。

> [!NOTE]
> 對於 `gemini-embedding-2` 的文字任務，請使用 Prompt 前綴指令（如 `task: search result | query: ...` 或 `title: ... | text: ...`）代替 `task_type` 參數。

```python
from google import genai

client = genai.Client()

# 格式化文字檢索前綴
query_text = "task: search result | query: 尋找海灘夕陽與衝浪相關的風景照"
doc_text = "title: 墾丁日落 | text: 墾丁白沙灣傍晚美麗的落日餘暉與海浪衝浪者"

result_query = client.models.embed_content(
    model="gemini-embedding-2",
    contents=query_text,
)

result_doc = client.models.embed_content(
    model="gemini-embedding-2",
    contents=doc_text,
)

print(f"Query 向量長度: {len(result_query.embeddings[0].values)}")
print(f"Doc 向量長度: {len(result_doc.embeddings[0].values)}")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多模態圖文跨媒體搜尋系統</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將 gemini-embedding-2 多模態向量程式改寫為 Gradio 圖文搜尋應用：
1. 支援使用者上傳圖片資料庫（多張相片）。
2. 提供文字搜尋框（如「找一張紅色跑車在山路行駛的照片」），計算跨模態相似度並展示匹配照片。
```
</details>

---

## 4. MRL 向量維度縮減 (Matryoshka Representation Learning)

Gemini 向量模型支援 **MRL (Matryoshka Representation Learning)** 技術，預設輸出為 3072 維度，但可自由截斷至 **1536** 或 **768** 維，大幅節省向量資料庫儲存與索引計算成本，且檢索品質幾乎不受影響。

```python
from google import genai
from google.genai import types

client = genai.Client()

text = "深度學習與大型多模態語言模型的最新發展"

# 彈性指定輸出維度 (768, 1536, 3072)
result_768 = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    ),
)

vec = result_768.embeddings[0].values
print(f"指定 768 維度之實際長度: {len(vec)}")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：向量維度自訂與壓縮效能分析面板</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述 MRL 維度控制程式改寫為 Streamlit 評估工具：
1. 提供文字輸入區與維度選擇器（768 / 1536 / 3072）。
2. 呼叫 API 並顯示生成的向量長度、儲存空間佔用估算與相似度矩陣差異。
```
</details>

---

## 5. 繁體中文開源模型評測與 ChromaDB 向量庫整合

針對繁體中文特化檢索，本專案亦整合了開源的 `intfloat/multilingual-e5-large` 與開源向量資料庫 **ChromaDB**：

- **評測成果**：可參考本目錄下的 [`Embeddings模型評測.xlsx`](./Embeddings模型評測.xlsx)
- **ChromaDB 向量庫整合範例**：見 [`pretrain_query_chromaDb/`](./pretrain_query_chromaDb)
- **物件導向實作**：見 [`document-search-e5.py`](./document-search-e5.py)

```bash
# 執行 E5 本地端向量搜尋示範
python document-search-e5.py
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：ChromaDB 向量資料庫管理與檢索後台</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將 ChromaDB 向量資料庫整合程式改寫為 Gradio 管理後台：
1. 介面提供 CSV 匯入 ChromaDB 向量庫功能。
2. 提供語意檢索查詢框與 Top-K 滑桿。
3. 呈現檢索匹配的文件內容與元數據 (Metadata)。
```
</details>

---

## 6. 支援的任務類型對照表 (Task Types for `gemini-embedding-001`)

| Task Type | 說明 | 適用情境 |
|---|---|---|
| `SEMANTIC_SIMILARITY` | 評估文本之間的語意相近程度 | 推薦系統、重複問答偵測 |
| `RETRIEVAL_DOCUMENT` | 知識庫被搜尋文件之向量化 | 文章、書籍、Wiki 知識庫索引 |
| `RETRIEVAL_QUERY` | 使用者搜尋查詢之向量化 | 搜尋引擎、FAQ 問答查詢 |
| `QUESTION_ANSWERING` | 問答系統中針對問題優化之向量 | 客服 Chatbot 提問 |
| `CLASSIFICATION` | 文本分類任務 | 情感分析、垃圾訊息過濾 |
| `CLUSTERING` | 文本分群任務 | 主題自動分群、異常檢測 |
| `CODE_RETRIEVAL_QUERY` | 以自然語言查詢程式碼片段 | 程式碼搜尋與建議 |
| `FACT_VERIFICATION` | 事實查核與證據檢索 | 自動化事實驗證系統 |
