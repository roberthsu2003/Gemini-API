"""
app_fastapi.py
實務應用整合：FastAPI 非同步後端服務與 SSE 即時串流 API
整合 Gemini 3.7 Flash Interactions API
提供：
1. GET  /                : API 健康檢查與規格說明
2. POST /api/generate    : 單輪文字生成 (同步/非同步標準 JSON 回應)
3. POST /api/chat/stream : SSE (Server-Sent Events) 即時串流端點，支援 previous_interaction_id

啟動方式：
uvicorn text_generation.app_fastapi:app --reload --port 8000
"""

import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google import genai
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI(
    title="Gemini 3.7 Flash Backend API",
    description="使用 FastAPI 封裝 Google Interactions API，支援標準 JSON 回應與 SSE 即時串流。",
    version="1.0.0"
)

# 支援 CORS 跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === 請求與回應資料模型 ===
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="使用者提問或 Prompt", example="請以繁體中文說明什麼是 FastAPI？")
    model: str = Field(default="gemini-3.7-flash", description="欲呼叫的 Gemini 模型")
    system_instruction: Optional[str] = Field(default=None, description="系統指示詞")
    thinking_level: Optional[str] = Field(default="medium", description="思考深度: minimal, low, medium, high")
    temperature: Optional[float] = Field(default=1.0, description="生成溫度 (0.0 ~ 2.0)")


class GenerateResponse(BaseModel):
    interaction_id: str
    output_text: str
    model: str


class ChatStreamRequest(BaseModel):
    prompt: str = Field(..., description="使用者輸入訊息")
    previous_interaction_id: Optional[str] = Field(default=None, description="前一輪互動 ID（延續會話記憶）")
    thinking_level: Optional[str] = Field(default="medium", description="思考深度")


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Gemini Interactions API FastAPI Backend",
        "docs_url": "/docs"
    }


@app.post("/api/generate", response_model=GenerateResponse)
def generate_text(req: GenerateRequest):
    """標準 JSON 單輪文字生成端點"""
    try:
        interaction = client.interactions.create(
            model=req.model,
            input=req.prompt,
            system_instruction=req.system_instruction,
            generation_config={
                "thinking_level": req.thinking_level,
                "temperature": req.temperature
            }
        )
        return GenerateResponse(
            interaction_id=interaction.id or "",
            output_text=interaction.output_text or "",
            model=req.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
def chat_stream(req: ChatStreamRequest):
    """SSE (Server-Sent Events) 打字機即時串流端點"""
    def event_generator():
        try:
            stream = client.interactions.create(
                model="gemini-3.7-flash",
                input=req.prompt,
                previous_interaction_id=req.previous_interaction_id,
                generation_config={
                    "thinking_level": req.thinking_level,
                    "temperature": 1.0
                },
                stream=True
            )
            for event in stream:
                # 傳送 interaction_id 中繼資料
                if hasattr(event, "interaction_id") and event.interaction_id:
                    yield f"event: meta\ndata: {{\"interaction_id\": \"{event.interaction_id}\"}}\n\n"
                elif hasattr(event, "id") and event.id:
                    yield f"event: meta\ndata: {{\"interaction_id\": \"{event.id}\"}}\n\n"

                # 傳送文字 delta
                if event.event_type == "step.delta" and event.delta.type == "text":
                    # SSE 格式
                    text_chunk = event.delta.text.replace("\n", "\\n")
                    yield f"event: delta\ndata: {text_chunk}\n\n"

            yield "event: done\ndata: [DONE]\n\n"
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("text_generation.app_fastapi:app", host="127.0.0.1", port=8000, reload=True)
