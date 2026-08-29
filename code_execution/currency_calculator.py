import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

with open("2025_01_29.csv", encoding="utf-8") as file:
    csv_content = file.read()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

system_instruction = f"""
## 請依據以下的臺灣銀行牌告匯率 CSV 內容回答問題：
{csv_content}

## 換算規則：
1. 若要將外幣換成台幣：使用「現金匯率(本行買入)」* 金額
2. 若要將台幣換成外幣：使用 金額 / 「現金匯率(本行賣出)」
3. 若為兩種非台幣外幣相互兌換：先將外幣 A 轉為台幣，再將台幣轉為外幣 B。
"""

prompt = "我有 10,000 加拿大幣，如果全部換成美金，大約可以換得多少美金？請編寫並執行 Python 程式碼進行精確計算。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    system_instruction=system_instruction,
    tools=[{"type": "code_execution"}],
)

print("=== Gemini Code Execution 匯率換算 ===")
for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- 產生的計算程式碼 ---")
        code = step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code
        print(code)
    elif step.type == "code_execution_result":
        print("\n--- 程式碼執行輸出 ---")
        print(step.result)

print("\n=== 模型完整回覆 ===")
print(interaction.output_text)
