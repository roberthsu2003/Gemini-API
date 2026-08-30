"""
app_fastapi.py
實務應用整合：FastAPI 聯網即時搜尋 API 微服務
提供：POST /api/search 端點，回傳回答文字與結構化引用來源清單
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini Ground Search API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SourceItem(BaseModel):
    title: str
    uri: str


class SearchRequest(BaseModel):
    query: str = Field(..., example="請查詢今天最新的科技重大新聞三則。")


class SearchResponse(BaseModel):
    answer: str
    search_queries: List[str] = []
    sources: List[SourceItem] = []


@app.post("/api/search", response_model=SearchResponse)
def search_endpoint(req: SearchRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=req.query + "\n（請使用繁體中文回答）",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )

        sources_list = []
        queries_list = []

        if response.candidates and response.candidates[0].grounding_metadata:
            meta = response.candidates[0].grounding_metadata
            if meta.web_search_queries:
                queries_list = meta.web_search_queries
            if meta.grounding_chunks:
                for chunk in meta.grounding_chunks:
                    if chunk.web:
                        sources_list.append(SourceItem(title=chunk.web.title or "來源網址", uri=chunk.web.uri or ""))

        return SearchResponse(
            answer=response.text or "",
            search_queries=queries_list,
            sources=sources_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ground_search.app_fastapi:app", host="127.0.0.1", port=8004, reload=True)
