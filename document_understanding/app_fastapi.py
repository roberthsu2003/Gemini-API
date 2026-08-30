"""
app_fastapi.py
實務應用整合：FastAPI PDF 文件分析與問答微服務
提供：
1. POST /api/pdf/analyze : 上傳 PDF 檔案並提供 Prompt 進行分析
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini PDF Understanding API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/pdf/analyze")
async def analyze_pdf(
    prompt: str = Form(default="請總結這份文件的五大關鍵重點，使用繁體中文。"),
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="僅支援 PDF 檔案上傳")

    try:
        pdf_bytes = await file.read()

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                prompt
            ]
        )

        return {
            "filename": file.filename,
            "prompt": prompt,
            "analysis": interaction.output_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("document_understanding.app_fastapi:app", host="127.0.0.1", port=8002, reload=True)
