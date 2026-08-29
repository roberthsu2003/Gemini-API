import os
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


# 定義食譜模型
class Recipe(BaseModel):
    recipe_name: str = Field(description="食物或料理的名稱")
    category: str = Field(description="料理類型或分類，例如：年菜、甜點、零嘴")


class RecipeList(BaseModel):
    recipes: list[Recipe] = Field(description="食物食譜清單")


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
請從以下文字中取出所有食物料理名稱與分類：
1. 過年零嘴「花生酥餅」做法超簡單！香脆應景一口接一口
2. 棉花糖香蕉巧克力吐司 | 零技巧療癒甜點
3. 黃金鯧魚米粉 | 古早味台式開運年菜暖呼呼上桌
"""

# 使用 Interactions API 與 response_format 生成結構化輸出
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": RecipeList.model_json_schema(),
    },
)

# 使用 Pydantic 驗證並解析結果
result = RecipeList.model_validate_json(interaction.output_text)
print("--- 解析結果 (Pydantic 物件) ---")
for r in result.recipes:
    print(f"料理: {r.recipe_name} | 分類: {r.category}")

print("\n--- 原始 JSON 輸出 ---")
print(interaction.output_text)
