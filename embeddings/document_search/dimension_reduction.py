import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

text = "人工智慧與多模態大型語言模型的發展與應用趨勢"

print("=== 比較 Matryoshka 向量維度裁切 (MRL) ===")

for dim in [768, 1536, 3072]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=dim,
        ),
    )
    vec = result.embeddings[0].values
    print(f"指定維度: {dim:4d} | 實際向量長度: {len(vec):4d} | 前 3 個維度數值: {[round(x, 4) for x in vec[:3]]}")
