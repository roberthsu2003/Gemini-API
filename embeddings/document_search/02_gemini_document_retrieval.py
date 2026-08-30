"""
02_gemini_document_retrieval.py
Gemini 向量檢索核心教學：非對稱知識庫語意檢索 (Task Type: RETRIEVAL_QUERY vs RETRIEVAL_DOCUMENT)
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 知識庫文件資料庫
documents = [
    "公司差旅報銷政策：員工搭乘高鐵需檢附票根，住宿每晚上限 3,000 元新台幣，於次月 5 日前送交財務部審核。",
    "遠端工作規範：每週可申請至多 2 天居家辦公，需於前一日向直屬主管提出並完成系統打卡登記。",
    "資訊安全守則：嚴禁將未經許可之隨身碟插入公司電腦，密碼每季需強制更換且長度不得低於 12 碼。",
    "特休請假規定：任職滿半年享 3 天特休，滿一年享 7 天特休，請假應於 3 日前由差勤系統送出申請。"
]

print(f"📚 知識庫收錄文件筆數：{len(documents)}")

# 建立文件向量庫 (Task Type: RETRIEVAL_DOCUMENT)
doc_response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=documents,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT"
    )
)
doc_embeddings = [np.array(e.values) for e in doc_response.embeddings]

# 查詢提問 (Task Type: RETRIEVAL_QUERY)
query = "如果去外縣市出差住飯店，最多可以報銷多少錢？"
print(f"\n🔍 使用者提問：{query}")

query_response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_QUERY"
    )
)
query_embedding = np.array(query_response.embeddings[0].values)

# 計算相似度並排序 (Top-K)
scores = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
best_idx = np.argmax(scores)

print(f"\n🎯 最佳檢索命中文件 (相似度分數: {scores[best_idx]:.4f})：")
print(f"👉 {documents[best_idx]}")
