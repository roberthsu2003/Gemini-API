import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 全域記錄前一次互動 ID（伺服器端狀態管理）
last_interaction_id = None

def chat_response(message, history):
    global last_interaction_id
    
    # 支援串流生成，逐字回傳
    stream = client.interactions.create(
        model="gemini-3.7-flash",
        input=message,
        previous_interaction_id=last_interaction_id,
        stream=True
    )
    
    accumulated_text = ""
    for event in stream:
        # 捕捉 interaction_id 以延續下一輪對話
        if hasattr(event, "interaction_id") and event.interaction_id:
            last_interaction_id = event.interaction_id
        elif hasattr(event, "id") and event.id:
            last_interaction_id = event.id
            
        if event.event_type == "step.delta" and event.delta.type == "text":
            accumulated_text += event.delta.text
            yield accumulated_text

demo = gr.ChatInterface(
    fn=chat_response,
    title="Gemini Multi-turn Chat (Interactions API)",
    description="利用 Google Interactions API 的伺服器端狀態管理（`previous_interaction_id`）維護歷史上下文，並支援即時串流。",
    type="messages"
)

if __name__ == "__main__":
    demo.launch()
