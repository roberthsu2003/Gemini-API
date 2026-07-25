import os
import gradio as gr
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
chat = client.chats.create(model="gemini-flash-latest")

def processing_chat(message, history):
    response = chat.send_message(message)
    return response.text

demo = gr.ChatInterface(
    fn = processing_chat,
    type="messages"
)

demo.launch()
