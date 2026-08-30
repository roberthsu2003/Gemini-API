"""
app_streamlit.py
實務應用整合：Streamlit 語意檢索與知識庫問答儀表板
功能：自訂知識庫內容、維度縮減選項 (MRL) 與 Top-K 檢索結果排行
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="語意檢索儀表板", page_icon="🧠", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


st.title("🧠 Gemini 向量嵌入與語意檢索 (Embeddings RAG)")
st.caption("支援 Matryoshka 維度縮減與非對稱檢索")

DEFAULT_DOCS = """公司差旅報銷政策：住宿每晚最高 3,000 元，檢附發票次月 5 日前核銷。
遠端工作規範：每週至多 2 天居家辦公，需前一日於系統打卡申請。
特休假規定：年資滿半年享 3 天，滿一年享 7 天特休。
資安政策：密碼每季強制更換，長度不得少於 12 碼。"""

docs_text = st.text_area("知識庫文件內容（每行一條）：", value=DEFAULT_DOCS, height=120)
doc_list = [d.strip() for d in docs_text.strip().split("\n") if d.strip()]

with st.sidebar:
    st.header("⚙️ 向量維度設定")
    dim_choice = st.selectbox("自訂輸出維度 (MRL)", [3072, 1536, 768, 512], index=0)

query = st.text_input("輸入查詢問題：", value="去外地出差住飯店最高可以報多少費用？")

if st.button("🔍 執行語意檢索 (Top-K)", type="primary"):
    with st.spinner("正在生成向量並計算相似度..."):
        try:
            # 建立文件向量
            doc_res = client.models.embed_content(
                model="gemini-embedding-001",
                contents=doc_list,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=dim_choice if dim_choice != 3072 else None
                )
            )
            doc_embs = [np.array(e.values) for e in doc_res.embeddings]

            # 建立查詢向量
            q_res = client.models.embed_content(
                model="gemini-embedding-001",
                contents=query,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY",
                    output_dimensionality=dim_choice if dim_choice != 3072 else None
                )
            )
            q_emb = np.array(q_res.embeddings[0].values)

            # 排名
            scores = [cosine_similarity(q_emb, d_emb) for d_emb in doc_embs]
            results = []
            for doc, score in zip(doc_list, scores):
                results.append({"文件內容": doc, "相似度分數": round(score, 4)})

            df = pd.DataFrame(results).sort_values(by="相似度分數", ascending=False)
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"檢索失敗：{str(e)}")
