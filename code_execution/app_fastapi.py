"""
app_fastapi.py
實務應用整合：FastAPI 程式碼沙盒運算 API 微服務
提供：POST /api/execute 端點，接收計算問題並回傳解答與執行歷程
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini Code Execution API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeExecRequest(BaseModel):
    prompt: str = Field(..., example="請用 Python 計算第 100 個費氏數列數值。")


class CodeExecResponse(BaseModel):
    result: str


@app.post("/api/execute", response_model=CodeExecResponse)
def execute_endpoint(req: CodeExecRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=req.prompt + "\n（請使用 Python 程式碼演算，並使用繁體中文解釋）",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution())],
            ),
        )
        return CodeExecResponse(result=response.text or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("code_execution.app_fastapi:app", host="127.0.0.1", port=8005, reload=True)
