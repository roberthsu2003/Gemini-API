"""
02_advanced_schemas.py
Gemini 結構化輸出核心教學：進階 Schema（條件多態 Union、遞迴樹狀結構與列舉 Enum）
"""

from enum import Enum
import os
from typing import List, Optional, Union
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class Priority(str, Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    URGENT = "緊急"


class TaskNode(BaseModel):
    task_id: str = Field(description="任務編號，如 TASK-001")
    title: str = Field(description="任務標題")
    priority: Priority = Field(description="優先權等級")
    subtasks: Optional[List["TaskNode"]] = Field(default=None, description="子任務列表（遞迴樹狀結構）")


TaskNode.model_rebuild()

prompt = "請幫一家電商公司規劃『雙 11 購物節活動上線』的專案 WBS 樹狀任務分解圖，包含主任務與子任務，並標註優先級。"
print(f"💬 提問：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TaskNode,
    )
)

print("✅ 遞迴樹狀結構 JSON 輸出：")
print(response.text)
