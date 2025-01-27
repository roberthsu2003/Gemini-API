import google.generativeai as genai
import os
import gradio as gr

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-2.0-flash-exp")
chat = model.start_chat()

def processing_chat(message, history):
    response = chat.send_message(message)
    return response.text

demo = gr.ChatInterface(
    fn = processing_chat,
    type="messages"
)

demo.launch()


