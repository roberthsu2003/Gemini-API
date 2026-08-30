"""
app_fastapi.py
實務應用整合：FastAPI 結構化輸出 API 端點
提供：POST /api/extract-recipe 端點，直接回傳強型別 Pydantic JSON 物件
"""

import json
import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="Gemini Structured Output API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Ingredient(BaseModel):
    name: str
    quantity: str


class RecipeModel(BaseModel):
    recipe_name: str
    cooking_time_minutes: int
    difficulty: str
    ingredients: List[Ingredient]
    steps: List[str]


class ExtractRequest(BaseModel):
    text: str = Field(..., example="請給我一道番茄炒蛋的做法與食材。")


@app.post("/api/extract-recipe", response_model=RecipeModel)
def extract_recipe(req: ExtractRequest):
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=[req.text, "請將內容轉為標準食譜結構。"],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeModel,
            )
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("structure_output.app_fastapi:app", host="127.0.0.1", port=8003, reload=True)
