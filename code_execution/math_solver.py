import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = (
    "請計算前 50 個質數的總和。"
    "請務必編寫並執行 Python 程式碼來計算，並印出所有質數清單與總和。"
)

# 透過 Interactions API 啟用 code_execution 工具
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "code_execution"}],
)

print("=== 執行歷程步驟 ===")
for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- [模型編寫的 Python 程式碼] ---")
        print(step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code)
    elif step.type == "code_execution_result":
        print("\n--- [沙盒執行結果 (stdout)] ---")
        print(step.result)
    elif step.type == "model_output":
        for block in step.content:
            if hasattr(block, "text") and block.text:
                print("\n--- [最終回答] ---")
                print(block.text)
