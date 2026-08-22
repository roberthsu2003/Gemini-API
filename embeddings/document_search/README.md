## 語意搜尋

> **模型更新（2026-07）**：舊的 `text-embedding-004` 已淘汰，請改用 `gemini-embedding-001`（支援 `task_type`、可調 `output_dimensionality`）。若需多模態（文字/圖片/影片/音訊）嵌入，可用最新的 `gemini-embedding-2`（但不支援 `task_type`）。本章範例已更新為新版 `google-genai` SDK 寫法。

新版 SDK 產生嵌入的方式：

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="要建立向量的文字內容",
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",   # 查詢時改用 RETRIEVAL_QUERY
        output_dimensionality=768         # 可選:768 / 1536 / 3072
    )
)
print(result.embeddings[0].values)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入語意搜尋與知識庫檢索介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Embedding 語意搜尋程式改寫為 Gradio 知識庫搜尋應用：
1. 介面提供 CSV / TXT 文件上傳區，系統自動調用 `client.models.embed_content` 計算每筆文件的向量並建立索引。
2. 提供「語意查詢輸入框」，使用者輸入任意自然語言問題後，將查詢轉為向量（task_type="RETRIEVAL_QUERY"）並計算餘弦相似度（Cosine Similarity）。
3. 使用 `gr.Dataframe` 呈現 Top-K 相似度最高的文件段落與相似度分數。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 語意搜尋應用：
1. 側邊欄支援使用者上傳 FAQ 或產品說明 CSV 檔，一鍵生成向量並快取在 `st.session_state`。
2. 主畫面提供搜尋列（`st.text_input`），即時進行語意比對。
3. 以卡片方式列出最相關的前 3 名結果，並以進度條（`st.progress`）視覺化展示相似度匹配百分比。
```
</details>


### 使用 gemini 提供的 `gemini-embedding-001` 建立的 embedding
**注意:Gemini 嵌入對繁體中文的檢索效果一般，繁體中文語意搜尋建議搭配下方的多語 E5 模型評估**
- [最簡單的範例](./document_search.ipynb)
- [使用csv檔](./document_search1.ipynb)

### [適合繁體中文的embedding模型評估表](./Embeddings模型評測.xlsx)

> 資料來源[使用繁體中文評測各家 Embedding 模型的檢索能力](https://ihower.tw/blog/archives/12167)

### 使用Microsoft開源的intfloat/multilingual-e5-large

- [測試1對繁體中文的檢索能力](./document_search2.ipynb)
- [測試2對繁體中文的檢索能力](./document_search3.ipynb)
- [測試3對繁體中的的檢索能力(使用物件導向)](./document-search-e5.py)
- [預訓練和要求](./pretrain_and_query)
	- 使用csv檔
	- 將dataframe儲存為pkl檔
- [預訓練和要求](./pretrain_query_chromaDb)
	- 使用csv匯入向量資料庫
	- 使用chromaDb
