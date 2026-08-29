# 圖像生成與多模態創意 (Text-to-Image Generation)

Google 提供了業界頂尖的圖像生成模型 **Imagen 3 (`imagen-3.0-generate-002`)** 與最新 **`gemini-2.5-flash-image`** 多模態生圖能力，能將純文字提示詞（Text Prompt）轉換為高解析度、光影細膩、構圖精美的視覺圖片。

---

## 核心應用場景

- 🎨 **視覺內容與社群配圖**：為文章、簡報、廣告行銷文案自動生成符合語境的插圖與封面。
- 📐 **自訂比例適配**：支援 `1:1`（正方形）、`16:9`（寬螢幕橫圖）、`9:16`（手機直式短影音封面）等多元比例。
- 🪄 **Prompt 智慧擴寫工作流**：結合 Gemini 3 的語言能力，將使用者的簡短概念自動擴寫為專業級攝影與藝術 Prompt，大幅提升生圖品質。

---

## 1. 快速開始：Imagen 3 基礎文字生成圖片 (Text-to-Image)

使用 `imagen-3.0-generate-002` 模型，根據描述文字生成單張或多張圖片。

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
    print("圖片生成完成並已儲存！")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：AI 圖像生成工作台</b></summary>

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
1. 主畫面提供 Prompt 輸入框與常用藝術風格快捷標籤（如「賽博龐克」、「水彩插畫」、「寫實攝影」）。
2. 點擊生成後顯示 st.spinner 載入動畫。
3. 使用 st.image 展示圖片，並提供一鍵下載按鈕。
```
</details>

---

## 2. 長寬比例與格式自訂 (Aspect Ratio Control)

支援彈性指定不同的長寬比例：
- `"1:1"`：社群貼文、頭像
- `"16:9"`：桌面桌布、YouTube 縮圖、橫式簡報
- `"9:16"`：手機直式桌布、IG Reels / TikTok 封面
- `"4:3"` 與 `"3:4"`：標準相片畫幅

```python
import io
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = "未來科技城市的賽博龐克夜景，飛行汽車在霓虹大樓之間穿梭，雨夜倒影，超寬螢幕電影感畫面。"

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        output_mime_type="image/jpeg",
    ),
)

for gen_image in response.generated_images:
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save("cyberpunk_city_16_9.jpg")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多畫幅桌布與海報設計器</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述比例控制生圖程式改寫為 Gradio 應用：
1. 提供 Radio 按鈕讓使用者選擇比例（1:1、16:9、9:16、4:3）。
2. 提供圖片格式下拉選單（PNG / JPEG）。
3. 產生對應畫幅的高畫質圖片並在畫面上即時展示。
```
</details>

---

## 3. Gemini 多模態圖像生成 (`gemini-2.5-flash-image`)

除了獨立的 Imagen 模型外，Gemini 也推出了原生多模態圖像生成模型，透過 `response_modalities=["IMAGE"]` 即可直接接收圖片串流。

```python
import io
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = "一隻站在木樁上的翠鳥，背景是波光粼粼的水面，微距攝影，羽毛細節清晰可辨。"

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        image = Image.open(io.BytesIO(part.inline_data.data))
        image.save("kingfisher_gemini.png")
        print("多模態圖片生成成功！")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多模態即時靈感畫板</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將 gemini-2.5-flash-image 多模態生圖改寫為 Streamlit 應用：
1. 介面以簡潔現代風排版，提供自然語言生圖輸入框。
2. 接收多模態影像資料流並在畫面上即時呈現。
```
</details>

---

## 4. AI 創意工作流：Gemini Prompt 智慧擴寫 ➔ Imagen 3 自動產圖

使用者只需要輸入簡單概念（例如：「雨夜中的咖啡館」），系統先讓 Gemini 3.7 Flash 擴寫為具備專業光影、鏡頭與藝術細節的英文提示詞，再無縫交由 Imagen 3 生成頂級畫質圖片。

```python
import io
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

user_concept = "雨夜中的咖啡館"

# 步驟 1: Gemini 擴寫為專業 Prompt
enhance_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=user_concept,
    system_instruction="請將使用者輸入的簡短概念擴寫為一段適合 Imagen 3 生成高畫質圖片的詳細英文 Prompt（包含光影、視角、藝術風格與氛圍），直接輸出英文提示詞即可。",
)
expanded_prompt = enhance_interaction.output_text.strip()
print(f"擴寫後提示詞:\n{expanded_prompt}\n")

# 步驟 2: Imagen 3 生成圖片
response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=expanded_prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="16:9",
    ),
)

for gen_image in response.generated_images:
    image = Image.open(io.BytesIO(gen_image.image.image_bytes))
    image.save("enhanced_cafe.png")
    print("圖片生成成功！")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧詠唱擴寫與一鍵生圖創作工作室</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「Prompt 擴寫 ➔ Imagen 生圖」工作流改寫為 Gradio 應用：
1. 使用者只需輸入中文簡短想法（如「森林裡的樹屋餐廳」）。
2. 點擊「一鍵創作」後，左側顯示 Gemini 自動擴寫出的專業英文 Prompt 與視覺設計理念，右側展示 Imagen 3 生成的精美高解析度圖片。
3. 支援一鍵複製英文 Prompt 與重新生成。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 創作工作室：
1. 建立兩步驟視覺化流程（Step 1: 概念擴充 ➔ Step 2: 圖片生成）。
2. 使用 st.chat_message 或卡片佈局展示擴寫前後的對比。
3. 提供下載高畫質 PNG 按鈕與分享功能。
```
</details>
