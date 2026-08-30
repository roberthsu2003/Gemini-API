# 🎨 圖像生成與多模態創意 (Text-to-Image Generation)

Google 提供了業界頂尖的圖像生成模型 **Imagen 3 (`imagen-3.0-generate-002`)** 與最新 **`gemini-2.5-flash-image`** 多模態生圖能力，能將純文字提示詞（Text Prompt）轉換為高解析度、光影細膩、構圖精美的視覺圖片。

> 📖 **官方說明**：
> Imagen 3 具備高度文字渲染能力與細節豐富度，支援多種長寬比自訂；亦可結合 Gemini 3 世代語言模型進行 Prompt 智慧擴寫，實現高品質生圖工作流。
> 官方文件：[Image generation - Google AI for Developers](https://ai.google.dev/gemini-api/docs/imagen)

---

## 📑 目錄導覽

1. [Imagen 3 基礎文字生圖 (01_text_to_image.py)](#1-imagen-3-基礎文字生圖-01_text_to_imagepy)
2. [長寬比例與格式控制 (02_aspect_ratio.py)](#2-長寬比例與格式控制-02_aspect_ratiopy)
3. [Gemini 2.5 Flash Image 多模態生圖 (03_gemini_flash_image.py)](#3-gemini-25-flash-image-多模態生圖-03_gemini_flash_imagepy)
4. [Gemini 擴寫提示詞 ➔ Imagen 3 一條龍產圖 (04_prompt_enhancer.py)](#4-gemini-擴寫提示詞--imagen-3-一條龍產圖-04_prompt_enhancerpy)

---

## 1. Imagen 3 基礎文字生圖 (`01_text_to_image.py`)

使用 `imagen-3.0-generate-002` 模型，根據描述文字生成單張或多張圖片：

- 核心程式檔案：[`01_text_to_image.py`](./01_text_to_image.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
import io
import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "一隻穿著太空衣的可愛橘貓漂浮在浩瀚星空中，身旁有發光的星雲與星球，8k 超高畫質電影感寫實風格。"

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="1:1",
        output_mime_type="image/png",
    ),
)

for i, gen_image in enumerate(response.generated_images):
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save(f"space_cat_{i+1}.png")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Imagen 3 圖像生成程式改寫為 Gradio 網頁應用：
1. 介面提供文字輸入框（Prompt）、生成張數滑桿（1~4 張）與「開始生成」按鈕。
2. 呼叫 imagen-3.0-generate-002 生成圖片。
3. 輸出區以 gr.Gallery 展示生成的圖片，支援點擊放大預覽與下載。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 主畫面提供 Prompt 輸入框與常用藝術風格快捷標籤。
2. 點擊生成後顯示 st.spinner 載入動畫。
3. 使用 st.image 展示圖片，並提供一鍵下載按鈕。
```

**Telegram Bot 算圖 Prompt：**
```text
請幫我將上述程式碼封裝為 Telegram 機器人：
1. 使用 python-telegram-bot (v20+)。
2. 當用戶發送畫面描述文字時，呼叫 Imagen 3 算圖。
3. 將產生的圖檔透過 reply_photo 發送給用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我將上述程式碼改寫為 FastAPI 後端微服務：
1. 建立 POST /api/generate-image 端點接收 Prompt。
2. 呼叫 Imagen 3 產圖並將圖片轉為 Base64 字串回傳。
```
</details>

---

## 2. 長寬比例與格式控制 (`02_aspect_ratio.py`)

支援多元長寬比配置（`1:1`、`16:9`、`9:16`、`4:3`、`3:4`）：

- 核心程式檔案：[`02_aspect_ratio.py`](./02_aspect_ratio.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="未來科技城市的賽博龐克夜景，飛行汽車在霓虹大樓之間穿梭，超寬螢幕電影感畫面。",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        output_mime_type="image/jpeg",
    ),
)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：長寬比例選擇面板</b></summary>

**Streamlit 長寬比控制 Prompt：**
```text
請幫我在 Streamlit 應用中加入側邊欄下拉選單，讓使用者可在 1:1, 16:9, 9:16, 4:3, 3:4 之間切換長寬比，並動態傳入 types.GenerateImagesConfig。
```
</details>

---

## 3. Gemini 2.5 Flash Image 多模態生圖 (`03_gemini_flash_image.py`)

使用 Gemini 內建原生圖像生成模型：

- 核心程式檔案：[`03_gemini_flash_image.py`](./03_gemini_flash_image.py)

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-2.5-flash-image",
    input="一隻站在雪地上的可愛企鵝，戴著紅色毛線帽與圍巾，溫暖色調插畫風格。"
)

if hasattr(interaction, "output_image") and interaction.output_image:
    interaction.output_image.save("penguin.png")
```

---

## 4. Gemini 擴寫提示詞 ➔ Imagen 3 一條龍產圖 (`04_prompt_enhancer.py`)

利用 Gemini 3.7 Flash 的文字理解與擴寫能力，將簡短 Idea 轉化為專業級 Prompt 並交由 Imagen 3 產圖：

- 核心程式檔案：[`04_prompt_enhancer.py`](./04_prompt_enhancer.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

# 步驟 1：Gemini 智慧擴寫
enhanced = client.interactions.create(
    model="gemini-3.7-flash",
    system_instruction="請將用戶概念擴寫為高品質英文生圖 Prompt，直接輸出英文提示詞。",
    input="一間在雨林深處的未來樹屋實驗室"
)

# 步驟 2：Imagen 3 產圖
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=enhanced.output_text.strip(),
    config=types.GenerateImagesConfig(aspect_ratio="16:9")
)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧擴寫工作台</b></summary>

**Gradio 一條龍擴寫產圖 Prompt：**
```text
請幫我開發 Gradio 應用：
1. 包含一個核取方塊「啟用 Gemini 提示詞智慧擴寫」。
2. 若啟用，先呼叫 Gemini 3.7 Flash 擴寫 Prompt 並於介面展示擴寫結果。
3. 接著調用 Imagen 3 產生最終圖片並於畫廊展示。
```
</details>
