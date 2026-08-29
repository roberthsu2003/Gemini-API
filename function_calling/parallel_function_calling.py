import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 定義多個獨立的智慧家庭設備控制函式宣告
power_disco_ball = {
    "type": "function",
    "name": "power_disco_ball",
    "description": "開啟或關閉旋轉迪斯可球燈電源。",
    "parameters": {
        "type": "object",
        "properties": {
            "power": {"type": "boolean", "description": "True 為開啟，False 為關閉"}
        },
        "required": ["power"],
    },
}

start_music = {
    "type": "function",
    "name": "start_music",
    "description": "播放指定風格的派對音樂。",
    "parameters": {
        "type": "object",
        "properties": {
            "energetic": {"type": "boolean", "description": "是否為動感風格"},
            "loud": {"type": "boolean", "description": "是否大聲播放"},
            "bpm": {"type": "integer", "description": "音樂每分鐘拍數 (BPM)"},
        },
        "required": ["energetic", "loud"],
    },
}

dim_lights = {
    "type": "function",
    "name": "dim_lights",
    "description": "調整室內主燈亮度。",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "number",
                "description": "亮度比例，0.0 為全暗，1.0 為全亮",
            }
        },
        "required": ["brightness"],
    },
}

tools = [power_disco_ball, start_music, dim_lights]

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "把房間切換成超嗨的狂歡派對模式！"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=tools,
)

fc_steps = [s for s in interaction.steps if s.type == "function_call"]
print(f"=== 偵測到 {len(fc_steps)} 個平行函式呼叫請求 ===")

results_input = []
for step in fc_steps:
    print(f"函式: {step.name} (ID: {step.id}) | 參數: {step.arguments}")
    # 模擬執行並收集結果
    res_data = {"status": "success", "message": f"{step.name} 已成功執行"}
    results_input.append(
        {
            "type": "function_result",
            "name": step.name,
            "call_id": step.id,
            "result": [{"type": "text", "text": json.dumps(res_data)}],
        }
    )

# 一次性將所有平行執行的結果回傳給模型
final_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction.id,
    tools=tools,
    input=results_input,
)

print("\n=== 模型最終狀態回覆 ===")
print(final_interaction.output_text)
