"""
app_fastapi.py
實務應用整合：FastAPI 向量嵌入與語意相似度 API 微服務
提供：
1. POST /api/embed : 取得文字向量清單
2. POST /api/similarity : 比對兩組文字的語意相似度
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import numpy as np
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini Embeddings API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class EmbedRequest(BaseModel):
    texts: List[str] = Field(..., example=["人工智慧", "機器學習"])
    dimensionality: Optional[int] = Field(default=None, description="自訂維度: 768, 512 等")


class SimilarityRequest(BaseModel):
    text_a: str = Field(..., example="這部電影非常感人好看。")
    text_b: str = Field(..., example="這部片催淚精彩，值得推薦。")


@app.post("/api/embed")
def embed_endpoint(req: EmbedRequest):
    try:
        cfg = types.EmbedContentConfig(output_dimensionality=req.dimensionality) if req.dimensionality else None
        res = client.models.embed_content(
            model="gemini-embedding-001",
            contents=req.texts,
            config=cfg
        )
        return {
            "dimension": len(res.embeddings[0].values),
            "embeddings": [e.values for e in res.embeddings]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/similarity")
def similarity_endpoint(req: SimilarityRequest):
    try:
        res = client.models.embed_content(
            model="gemini-embedding-001",
            contents=[req.text_a, req.text_b],
        )
        e1 = np.array(res.embeddings[0].values)
        e2 = np.array(res.embeddings[1].values)
        score = cosine_similarity(e1, e2)
        return {
            "text_a": req.text_a,
            "text_b": req.text_b,
            "similarity_score": round(score, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("embeddings.document_search.app_fastapi:app", host="127.0.0.1", port=8007, reload=True)
