"""
app_gradio.py
實務應用整合：Gradio Google Search 聯網搜尋與事實查核介面
功能：即時搜尋最新資訊，並在介面右側完整列出引用來源與網址
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def perform_ground_search(query: str):
    if not query.strip():
        return "請輸入問題！", ""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=query + "\n（請使用繁體中文回答）",
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    answer = response.text or "無回答內容"
    sources_md = "### 📚 引用來源網址 (Sources)\n"

    if response.candidates and response.candidates[0].grounding_metadata:
        meta = response.candidates[0].grounding_metadata
        if meta.web_search_queries:
            sources_md += f"**搜尋查詢關鍵字**：`{', '.join(meta.web_search_queries)}`\n\n"
        if meta.grounding_chunks:
            for i, chunk in enumerate(meta.grounding_chunks, 1):
                if chunk.web:
                    sources_md += f"{i}. [{chunk.web.title}]({chunk.web.uri})\n"

    return answer, sources_md


with gr.Blocks(title="Google Search 聯網接地搜尋", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌐 Gemini 3.7 Flash 聯網即時搜尋 (Search Grounding)")
    gr.Markdown("自主連接 Google Search 即時取得最新新聞動態、賽事結果與科技趨勢，並標註真實參考來源。")

    with gr.Row():
        query_input = gr.Textbox(
            label="請輸入即時問題",
            placeholder="例如：請查詢今天最新的國際科技新聞頭條三則...",
            lines=3
        )

    search_btn = gr.Button("🔍 聯網搜尋回答", variant="primary")

    with gr.Row():
        with gr.Column(scale=6):
            answer_output = gr.Markdown(label="Gemini 總結回答")
        with gr.Column(scale=4):
            sources_output = gr.Markdown(label="查核來源與網址")

    search_btn.click(fn=perform_ground_search, inputs=[query_input], outputs=[answer_output, sources_output])

if __name__ == "__main__":
    demo.launch()
