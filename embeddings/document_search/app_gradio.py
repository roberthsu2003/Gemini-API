"""
app_gradio.py
實務應用整合：Gradio 語意相似度與知識庫搜尋工作台
功能：輸入句子計算相似度矩陣，或輸入問題搜尋最匹配的知識庫條目
"""

import os
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types
import numpy as np
import pandas as pd

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def calculate_similarity(text1: str, text2: str):
    if not text1.strip() or not text2.strip():
        return "請輸入兩個句子進行比對"

    res = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text1, text2],
    )
    e1 = np.array(res.embeddings[0].values)
    e2 = np.array(res.embeddings[1].values)

    score = cosine_similarity(e1, e2)
    return f"### 📊 語意相似度分數：`{score:.4f}`\n\n- 分數越接近 1.0 代表語意越相似\n- 向量維度大小：`{len(e1)}`"


with gr.Blocks(title="Gemini 向量語意相似度分析", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 Gemini Embedding 語意相似度分析工作台")
    gr.Markdown("使用 `gemini-embedding-001` 模型將文本轉換為語意向量，進行精確相似度比對與語意搜尋。")

    with gr.Row():
        t1 = gr.Textbox(label="句子 A", value="大語言模型正在改變軟體開發架構與工程師生產力。", lines=2)
        t2 = gr.Textbox(label="句子 B", value="AI Agent 與程式碼生成工具大幅提升了開發效率。", lines=2)

    btn = gr.Button("⚡ 計算向量語意相似度", variant="primary")
    result_box = gr.Markdown(label="分析結果")

    btn.click(fn=calculate_similarity, inputs=[t1, t2], outputs=[result_box])

if __name__ == "__main__":
    demo.launch()
