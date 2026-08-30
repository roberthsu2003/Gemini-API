"""
03_dimension_reduction.py
Gemini 向量檢索核心教學：Matryoshka (MRL) 向量維度彈性縮減
透過 output_dimensionality 將 3072 維度縮減為 768 或 512 維度，大幅節省向量資料庫儲存空間
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

text = "Google Gemini Embedding 支援 Matryoshka Representation Learning (MRL) 彈性自訂維度。"

# 1. 預設 3072 維度
resp_default = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
)
dim_default = len(resp_default.embeddings[0].values)
print(f"📏 預設向量維度: {dim_default}")

# 2. 縮減至 768 維度
resp_768 = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
    config=types.EmbedContentConfig(
        output_dimensionality=768
    )
)
dim_768 = len(resp_768.embeddings[0].values)
print(f"📏 縮減後向量維度: {dim_768} (節省 75% 儲存空間與檢索計算量)")
