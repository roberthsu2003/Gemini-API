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
