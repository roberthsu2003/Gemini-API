"""
03_parallel_function_calling.py
Gemini 函式呼叫核心教學：多工具平行呼叫 (Parallel Function Calling)
模型單次自動分析並同時調用多個設備或 API
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def control_smart_device(device_name: str, action: str, level: int = 0) -> dict:
    """控制智慧家庭設備（如冷氣、電燈、窗簾）。

    Args:
        device_name: 設備名稱，如 '客廳大燈', '主臥冷氣', '客廳窗簾'
        action: 操作動作，如 'turn_on', 'turn_off', 'set_level'
        level: 設定數值（如冷氣溫度 26 度，或亮度 80%）
    """
    print(f"⚡ [執行智慧家庭指令] 设备: {device_name}, 動作: {action}, 數值: {level}")
    return {"status": "success", "device": device_name, "message": f"{device_name} 已成功執行 {action}"}


prompt = "我要出門了，請幫我關掉客廳大燈、把客廳窗簾拉下，並將主臥冷氣關閉。"
print(f"💬 用戶指令：{prompt}\n")

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[control_smart_device],
    ),
)

print("\n🤖 Gemini 平行控制回覆：")
print(response.text)
