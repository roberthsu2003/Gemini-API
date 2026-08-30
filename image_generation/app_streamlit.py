"""
app_streamlit.py
實務應用整合：Streamlit 圖像生成與擴寫儀表板
功能：側邊欄比例與風格配置、Gemini 智慧擴寫預覽與圖檔下載
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Imagen 3 生圖工作室", page_icon="🎨", layout="wide")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ 請在 .env 設定 GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🎨 Google Imagen 3 藝術生圖工作室")
st.caption("結合 Gemini 語言模型擴寫與 Imagen 3 高畫質算圖引擎")

with st.sidebar:
    st.header("⚙️ 生成參數配置")
    aspect_ratio = st.selectbox("長寬比例 (Aspect Ratio)", ["1:1", "16:9", "9:16", "4:3", "3:4"], index=0)
    num_images = st.slider("生成張數", min_value=1, max_value=4, value=1)
    auto_enhance = st.toggle("啟用 Gemini 智慧 Prompt 擴寫", value=True)

user_prompt = st.text_area("請輸入畫面概念描述：", placeholder="例如：浩瀚星空下的未來科技綠洲城市...", height=100)

if st.button("🚀 開始算圖", type="primary", use_container_width=True):
    if not user_prompt.strip():
        st.warning("請先輸入描述！")
    else:
        final_prompt = user_prompt
        if auto_enhance:
            with st.spinner("🪄 Gemini 正在為您擴寫專業 Prompt..."):
                enhancer = client.interactions.create(
                    model="gemini-3.7-flash",
                    system_instruction="請將用戶概念擴寫為高品質英文生圖 Prompt，直接輸出英文提示詞。",
                    input=user_prompt
                )
                final_prompt = enhancer.output_text.strip()
                st.info(f"✨ **擴寫 Prompt**：{final_prompt}")

        with st.spinner("🎨 Imagen 3 正在繪製高畫質圖片..."):
            try:
                response = client.models.generate_images(
                    model="imagen-3.0-generate-002",
                    prompt=final_prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=num_images,
                        aspect_ratio=aspect_ratio,
                        output_mime_type="image/png",
                    ),
                )
                cols = st.columns(num_images)
                for idx, gen_image in enumerate(response.generated_images):
                    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
                    with cols[idx]:
                        st.image(image, caption=f"圖 #{idx+1}", use_container_width=True)
                        st.download_button(
                            label=f"💾 下載圖 #{idx+1}",
                            data=gen_image.image.image_bytes,
                            file_name=f"imagen_{idx+1}.png",
                            mime="image/png"
                        )
            except Exception as e:
                st.error(f"生成失敗：{str(e)}")
