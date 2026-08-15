import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

# 使用 Interactions API 伺服器端狀態管理 (previous_interaction_id)
last_interaction_id = None

def processing_chat(message, history):
    global last_interaction_id
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=message,
        previous_interaction_id=last_interaction_id
    )
    last_interaction_id = interaction.id
    return interaction.output_text

demo = gr.ChatInterface(
    fn = processing_chat,
    type="messages"
)

demo.launch()
