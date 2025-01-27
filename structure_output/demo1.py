import google.generativeai as genai
import os
import json
"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    description = "Return some of the most popular cookie recipes",
    properties = {
      "recipes": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.OBJECT,
          properties = {
            "recipe_name": content.Schema(
              type = content.Type.STRING,
              description = "name of the recipe",
            ),
          },
        ),
      ),
    },
  ),
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
    history = [
    {
      "role": "model",
      "parts": [
        "請取出食物的名字",
      ],
    },
  ]
)

response = chat_session.send_message("過年零嘴「花生酥餅」做法超簡單！\n香脆應景一口接一口,棉花糖香蕉巧克力吐司 | 零技巧療癒甜點\n黃金鯧魚米粉 | 古早味台式開運年菜暖呼呼上桌")

print(response.text)