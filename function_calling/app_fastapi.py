"""
app_fastapi.py
實務應用整合：FastAPI 函式呼叫與工具執行 API 微服務
提供：POST /api/agent 端點，支援工具自動執行並回傳結構化解答
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

app = FastAPI(title="Gemini Function Calling API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_crypto_price(symbol: str) -> dict:
    """查詢加密貨幣最新價格。"""
    prices = {"BTC": "88,500 USD", "ETH": "3,200 USD", "SOL": "190 USD"}
    return {"symbol": symbol.upper(), "price": prices.get(symbol.upper(), "未知幣別")}


class AgentRequest(BaseModel):
    prompt: str = Field(..., example="請問現在比特幣 (BTC) 與以太幣 (ETH) 的最新價格分別是多少？")


class AgentResponse(BaseModel):
    reply: str


@app.post("/api/agent", response_model=AgentResponse)
def agent_endpoint(req: AgentRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=req.prompt + "\n（請使用繁體中文親切回答）",
            config=types.GenerateContentConfig(
                tools=[get_crypto_price],
            ),
        )
        return AgentResponse(reply=response.text or "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("function_calling.app_fastapi:app", host="127.0.0.1", port=8006, reload=True)
