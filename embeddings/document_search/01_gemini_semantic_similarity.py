"""
01_gemini_semantic_similarity.py
Gemini 向量檢索核心教學：Gemini Embedding 文本向量嵌入與語意相似度計算
使用 gemini-embedding-001 模型將文本轉換為 3072 維語意向量，並計算餘弦相似度 (Cosine Similarity)
"""

import os
from dotenv import load_dotenv
from google import genai
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


texts = [
    "人工智慧正在改變軟體開發流程與工程師工作方式。",
    "大語言模型與 AI Agent 正在重塑現代程式設計架構。",
    "今天台北的天氣非常晴朗，適合去陽明山賞花步道走走。"
]

print("📝 待分析句子：")
for i, t in enumerate(texts, 1):
    print(f"  {i}. {t}")

print("\n⚡ 正在呼叫 gemini-embedding-001 取得向量嵌入...")
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
)

embeddings = [np.array(e.values) for e in response.embeddings]
print(f"✅ 成功取得向量，維度大小：{len(embeddings[0])}\n")

sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
sim_1_3 = cosine_similarity(embeddings[0], embeddings[2])

print(f"📊 句子 1 與 句子 2 (皆為 AI 主題) 相似度: {sim_1_2:.4f} (高度語意相關)")
print(f"📊 句子 1 與 句子 3 (AI vs 天氣) 相似度: {sim_1_3:.4f} (低相關)")
