import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

sentences = [
    "生命的意義是什麼？",
    "人類存在的目的是什麼？",
    "如何烤出美味的巧克力蛋糕？",
    "製作甜點與烘焙蛋糕的食譜有哪些？",
    "量子電腦如何改變加密技術？",
]

print("=== 1. 計算文本的語意向量 (SEMANTIC_SIMILARITY) ===")
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=sentences,
    config=types.EmbedContentConfig(
        task_type="SEMANTIC_SIMILARITY",
        output_dimensionality=768,
    ),
)

# 提取向量數據
embeddings = [e.values for e in result.embeddings]

# 計算餘弦相似度矩陣
sim_matrix = cosine_similarity(embeddings)

df_sim = pd.DataFrame(
    sim_matrix,
    index=[f"S{i+1}" for i in range(len(sentences))],
    columns=[f"S{i+1}" for i in range(len(sentences))],
)

print("\n=== 句子對照表 ===")
for i, s in enumerate(sentences):
    print(f"S{i+1}: {s}")

print("\n=== 餘弦相似度矩陣 ===")
print(df_sim.round(4))
