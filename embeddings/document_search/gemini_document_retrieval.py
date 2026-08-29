import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 知識庫文件庫 (Documents)
documents = [
    {
        "title": "空調日常保養",
        "text": "定期清洗空氣過濾網能維持最佳冷房效果並節省電力。建議每兩週拆下水洗並陰乾。",
    },
    {
        "title": "定時與睡眠模式",
        "text": "使用遙控器的定時關機與睡眠功能，可在就寢時自動微調溫度，提升舒適度並達到節能效果。",
    },
    {
        "title": "異常故障處理",
        "text": "若運轉指示燈閃爍且無法吹出冷風，請先拔掉電源插頭並聯絡授權維修人員，切勿自行拆解機身。",
    },
    {
        "title": "咖啡豆烘焙指南",
        "text": "中度烘焙能保留咖啡豆的果香與酸甜感，適合手沖與虹吸壺萃取。",
    },
]

print("=== 1. 為知識庫文件建立向量索引 (RETRIEVAL_DOCUMENT) ===")
doc_texts = [f"Title: {d['title']}\nContent: {d['text']}" for d in documents]

doc_result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=doc_texts,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=768,
    ),
)
doc_embeddings = np.array([e.values for e in doc_result.embeddings])

query = "冷氣如果壞掉不會冷該怎麼辦？"
print(f"\n=== 2. 使用者查詢問題 (RETRIEVAL_QUERY) ===")
print(f"查詢字串: 「{query}」")

query_result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY",
        output_dimensionality=768,
    ),
)
query_embedding = np.array(query_result.embeddings[0].values).reshape(1, -1)

# 計算相似度排序
similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
ranked_indices = np.argsort(similarities)[::-1]

print("\n=== 3. 語意搜尋匹配排序 (Top-K) ===")
for rank, idx in enumerate(ranked_indices, 1):
    print(f"Rank {rank} [相似度: {similarities[idx]:.4f}]")
    print(f"  標題: {documents[idx]['title']}")
    print(f"  內容: {documents[idx]['text']}\n")
