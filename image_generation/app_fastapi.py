"""
app_fastapi.py
實務應用整合：FastAPI 圖像生成後端微服務
提供：POST /api/generate-image 端點，回傳 base64 圖片編碼
"""

import base64
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Imagen 3 Image Generation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageGenRequest(BaseModel):
    prompt: str = Field(..., example="一隻戴著耳機聽音樂的柴犬，霓虹插畫風")
    aspect_ratio: str = Field(default="1:1", example="1:1")
    enhance_prompt: bool = Field(default=False, description="是否啟用 Gemini 提示詞擴寫")


class ImageGenResponse(BaseModel):
    prompt_used: str
    image_base64: str
    mime_type: str = "image/png"


@app.post("/api/generate-image", response_model=ImageGenResponse)
def generate_image_endpoint(req: ImageGenRequest):
    try:
        final_prompt = req.prompt
        if req.enhance_prompt:
            enhancer = client.interactions.create(
                model="gemini-3.7-flash",
                system_instruction="請將用戶概念擴寫為高品質英文生圖 Prompt，直接輸出英文提示詞。",
                input=req.prompt
            )
            final_prompt = enhancer.output_text.strip()

        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=final_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=req.aspect_ratio,
                output_mime_type="image/png",
            ),
        )

        image_bytes = response.generated_images[0].image.image_bytes
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")

        return ImageGenResponse(
            prompt_used=final_prompt,
            image_base64=img_b64,
            mime_type="image/png"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("image_generation.app_fastapi:app", host="127.0.0.1", port=8001, reload=True)
