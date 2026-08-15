import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


# 使用 Pydantic 定義輸出結構(新版 google-genai 推薦寫法)
class Recipe(BaseModel):
    recipe_name: str


class Recipes(BaseModel):
    recipes: list[Recipe]


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat = client.chats.create(
    model="gemini-flash-latest",
    config=types.GenerateContentConfig(
        system_instruction="請取出食物的名字",
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=Recipes,
    ),
)

response = chat.send_message(
    "過年零嘴「花生酥餅」做法超簡單！\n"
    "香脆應景一口接一口,棉花糖香蕉巧克力吐司 | 零技巧療癒甜點\n"
    "黃金鯧魚米粉 | 古早味台式開運年菜暖呼呼上桌"
)

print(response.text)
print(json.loads(response.text))
