## 語意搜尋
### 使用gemini內提供的models/text-embedding-004建立的embedding
**注意不適合建立繁體中文語意搜尋,但適合英文的語意**
- [最簡單的範例](./document_search.ipynb)
- [使用csv檔](./document_search1.ipynb)

### [適合繁體中文的embedding模型評估表](./Embeddings模型評測.xlsx)

> [使用繁體中文評測各家 Embedding 模型的檢索能力](https://ihower.tw/blog/archives/12167)

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
