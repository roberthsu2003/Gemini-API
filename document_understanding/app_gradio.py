"""
app_gradio.py
實務應用整合：Gradio PDF 智能研讀與多輪問答介面
功能：上傳 PDF 文件，自動產生重點摘要，並支援即時多輪對話問答
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

current_pdf_bytes = None


def upload_pdf(file):
    global current_pdf_bytes
    if file is None:
        return "請選擇 PDF 檔案上傳", []
    
    with open(file.name, "rb") as f:
        current_pdf_bytes = f.read()

    # 自動摘要
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            types.Part.from_bytes(data=current_pdf_bytes, mime_type="application/pdf"),
            "請以繁體中文提供這份 PDF 文件的五大核心摘要與關鍵重點。"
        ]
    )
    summary = interaction.output_text
    return summary, []


def chat_with_pdf(message, history):
    global current_pdf_bytes
    if current_pdf_bytes is None:
        yield "⚠️ 請先在上方上傳 PDF 文件！"
        return

    if not message.strip():
        return

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=[
            types.Part.from_bytes(data=current_pdf_bytes, mime_type="application/pdf"),
            f"使用者問題：{message}\n請依據 PDF 內容以繁體中文詳盡解答。"
        ]
    )
    yield interaction.output_text


with gr.Blocks(title="Gemini PDF 文件智能研讀", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Gemini 3.7 Flash PDF 文件智能研讀工作台")
    gr.Markdown("原生多模態 PDF 視覺理解，支援上傳完整技術手冊、財務報表與學術論文。")

    with gr.Row():
        with gr.Column(scale=4):
            pdf_input = gr.File(label="上傳 PDF 文件", file_types=[".pdf"])
            summary_box = gr.Markdown(label="文件重點摘要")

        with gr.Column(scale=6):
            chatbot = gr.ChatInterface(
                fn=chat_with_pdf,
                title="與 PDF 文件即時問答",
                type="messages"
            )

    pdf_input.upload(fn=upload_pdf, inputs=[pdf_input], outputs=[summary_box, chatbot.chatbot])

if __name__ == "__main__":
    demo.launch()
