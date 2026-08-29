import os
from typing import Literal, Union
from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


# 範例 1: 條件分類結構 (anyOf / Union)
class SpamDetails(BaseModel):
    reason: str = Field(description="判定為垃圾/釣魚內容的原因")
    spam_type: Literal["phishing", "scam", "unsolicited_promotion", "other"] = Field(
        description="垃圾訊息類型"
    )


class SafeDetails(BaseModel):
    summary: str = Field(description="內容摘要")
    is_safe: bool = Field(description="是否適合所有讀者閱讀")


class ModerationResult(BaseModel):
    decision: Union[SpamDetails, SafeDetails] = Field(
        description="審查決定，根據內容為垃圾或安全訊息回傳對應結構"
    )


# 範例 2: 遞迴結構 (組織架構圖)
class Employee(BaseModel):
    name: str = Field(description="員工姓名")
    role: str = Field(description="職稱")
    reports: list["Employee"] = Field(
        default_factory=list, description="下屬員工清單 (遞迴結構)"
    )


def demo_moderation(client: genai.Client):
    print("=== 1. 條件結構 (anyOf / Union 內容審查) ===")
    prompt = """
    請審查以下訊息並輸出審查結果：
    恭喜您！您已被抽中獲得免費豪華郵輪雙人遊，請立即點擊連結領取：http://definitely-not-a-scam.example.com
    """
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ModerationResult.model_json_schema(),
        },
    )
    result = ModerationResult.model_validate_json(interaction.output_text)
    print("輸出結果:", result.model_dump_json(indent=2))


def demo_recursive(client: genai.Client):
    print("\n=== 2. 遞迴結構 (組織架構圖) ===")
    prompt = """
    請根據以下描述建立團隊組織架構圖：
    Alice 是技術長 (CTO)，底下管理研發主管 Bob 與架構師 Charlie。
    Bob 底下有後端工程師 David 和前端工程師 Eve。
    """
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Employee.model_json_schema(),
        },
    )
    employee = Employee.model_validate_json(interaction.output_text)
    print("輸出結果:", employee.model_dump_json(indent=2))


def demo_streaming(client: genai.Client):
    print("\n=== 3. 結構化串流輸出 (Streaming) ===")
    prompt = "請針對「新上線的 AI 助理功能」提供一篇詳細的正向使用者回饋摘要。"
    stream = client.interactions.create(
        model="gemini-3.7-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": SafeDetails.model_json_schema(),
        },
        stream=True,
    )
    for event in stream:
        if event.event_type == "step.delta" and event.delta.text:
            print(event.delta.text, end="", flush=True)
    print()


if __name__ == "__main__":
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    demo_moderation(client)
    demo_recursive(client)
    demo_streaming(client)
