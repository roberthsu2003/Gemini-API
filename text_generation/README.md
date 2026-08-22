# Gemini 文字生成 (Interactions API)

本章節介紹如何使用 Google Gemini 官方最新推薦的 **Interactions API** 進行文字生成、多模態理解、串流回應與多輪對話。

> **Interactions API 簡介**：
> Interactions API 是 Gemini 3 系列模型推薦的統一互動介面。使用 `client.interactions.create()` 即可涵蓋單輪文字生成、多輪狀態化對話（由伺服器端透過 `previous_interaction_id` 自動管理對話歷史）、串流傳輸（Streaming）與多模態輸入。
> 官方文件：[Text generation - Interactions API](https://ai.google.dev/gemini-api/docs/interactions/text-generation)

---

## 1. 快速開始：基本文字生成 (Zero-shot)

最基礎的單輪文字輸入與文字生成：

```python
from google import genai
from IPython.display import display, Markdown

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請問你的姓名（請使用繁體中文回答）？"
)

# 使用便利屬性 output_text 取得模型最終輸出文字
display(Markdown(interaction.output_text))

# ====output=====
# 您好，我是由 Google 訓練的大型語言模型。
```

> **便利屬性說明**：
> - `interaction.output_text`（字串）：會自動合併模型回覆中最後連續的文字區塊。
> - `interaction.output_image`：取得最後產生的圖片。
> - `interaction.output_audio`：取得最後產生的音訊。

### Zero-shot 整合 Gradio 介面

程式檔案：[`zero_shot.py`](./zero_shot.py)

```python
from google import genai
import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Zero-shot Text Generation (Interactions API)")
    
    input_text = gr.Textbox(
        label="prompt",
        placeholder="請輸入問題",
        submit_btn=True
    )
    with gr.Accordion("**懶得輸入可以點選以下問題**", open=False):
        gr.Examples(
            examples=["請問台灣的首都是哪裡？", "請問台灣的國土面積有多大？", "請問台灣的人口有多少？"], 
            label="問題範例",
            inputs=input_text
        )
    output_text = gr.Markdown()

    @input_text.submit(inputs=input_text, outputs=[input_text, output_text])
    def generate_text(input_str: str):
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=input_str
        )
        return (None, f"## {input_str}\n" + (interaction.output_text or ""))

demo.launch(share=True)
```

![](./images/pic1.png)

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入 Gradio / Streamlit 介面</b></summary>

**Gradio 介面改寫 Prompt：**
```text
請幫我將上述的 Zero-shot 文字生成範例改寫為美觀的 Gradio 應用：
1. 使用 gr.Blocks 排版，左側放置問題輸入框與常見預設問題按鈕（gr.Examples），右側即時以 Markdown 呈現 Gemini 回答。
2. 整合 client.interactions.create(model="gemini-3.7-flash", input=...)。
3. 加入清除按鈕與送出時的 loading 指示器。
```

**Streamlit 介面改寫 Prompt：**
```text
請幫我將上述的 Zero-shot 文字生成範例改寫為 Streamlit 網頁應用：
1. 使用 st.title 與 st.caption 建立頁面標題與簡介。
2. 提供 st.chat_input 接收使用者輸入，並用 st.session_state 儲存問答結果。
3. 呼叫 Gemini 3.7 Flash API 生成回覆，並以 st.markdown 渲染。
4. 側邊欄提供快捷提問按鈕，點擊後自動填入問題並執行。
```
</details>

---

## 2. 思考設定 (Thinking with Gemini)

Gemini 3 世代模型具備「思考（Thinking）」能力。您可以透過 `generation_config` 中的 `thinking_level` 控制思考深度（`minimal` / `low` / `medium` / `high`），以平衡品質、延遲與成本：

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="AI 是如何工作的？（請使用繁體中文簡要說明）",
    generation_config={
        "thinking_level": "low",
        "temperature": 1.0
    }
)
print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入思考深度控制介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述思考模式範例改寫為 Gradio 應用：
1. 設計包含問題輸入框、thinking_level 單選按鈕（minimal, low, medium, high）的控制面板。
2. 整合 Gemini Interactions API，將使用者選取的思考深度動態傳入 generation_config。
3. 回覆區以 Markdown 呈現，並顯示當前所使用的思考深度。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述思考模式範例改寫為 Streamlit 應用：
1. 側邊欄提供 st.select_slider 選擇思考深度（minimal, low, medium, high），並附上各等級說明。
2. 主畫面提供 st.text_area 與 st.button。
3. 按下生成時呼叫 Gemini 3.7 Flash 並顯示思考中狀態動畫（st.spinner），回覆完成後以 st.markdown 展示。
```
</details>

---

## 3. 系統指示 (System Instructions) 與風格控制

透過 `system_instruction` 參數引導模型的角色與輸出規範。

### 文章總結與翻譯 (整合 Gradio)

程式檔案：[`text_to_summarization.py`](./text_to_summarization.py)

```python
from google import genai
import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Text To Summarization (總結)")
    style_radio = gr.Radio(['學術', '商業', '專業', '口語化', '條列式'], label='風格', info="請選擇總結風格", value='口語化') 
    input_text = gr.Textbox(
        label="請輸入文章",
        lines=10,
        submit_btn=True
    )
    output_md = gr.Markdown()

    @input_text.submit(inputs=[style_radio, input_text], outputs=[output_md])
    def generate_text(style: str, input_str: str):
        if style == "口語化":
            style_prompt = "請使用口語化的風格\n"
        elif style == "學術":
            style_prompt = "請使用專業學術的風格\n"
        elif style == "商業":
            style_prompt = "請使用商業文章的風格\n"
        elif style == "專業":
            style_prompt = "請使用專業風格\n"
        elif style == "條列式":
            style_prompt = "請條列式重點\n"
        else:
            style_prompt = f"請使用{style}風格\n"

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            system_instruction=f"""
            你是一位文章的總結專家，也是一位繁體中文的高手。你的任務是: 
            1. 請將內容`總結`
            2. {style_prompt}
            """,
            input=input_str
        )

        return f"{style_prompt}\n\n### 總結內容如下:\n" + (interaction.output_text or "")

demo.launch(share=True)
```

![](./images/pic4.png)

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入文章總結與風格轉換介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述的文章總結與風格控制程式改寫為功能更完整的 Gradio 應用：
1. 介面提供長文本輸入框（Multiline Textbox）、目標風格單選框（學術/商業/專業/口語化/條列式），並新增「目標語言（繁中/英文/日文）」下拉選單。
2. 透過 Gemini Interactions API 的 system_instruction 設定角色與風格規則。
3. 輸出區包含總結結果、字數統計及一鍵複製按鈕。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述文章總結程式改寫為 Streamlit 應用：
1. 使用兩欄版面（st.columns）：左欄為原文輸入區（可貼上文字或上傳 txt 檔）與風格設定（st.segmented_control 或 st.radio），右欄為即時總結產出區。
2. 使用 st.button("開始摘要") 觸發，並以 st.spinner 顯示處理進度。
3. 生成後提供下載摘要文字檔按鈕（st.download_button）。
```
</details>

---

## 4. 多模態輸入 (Multimodal Inputs)

Gemini API 支援結合文字與圖片輸入。可透過 Base64 資料或 Files API 上傳之 URI 傳入圖片：

### 基本 Python 範例

```python
import PIL.Image
import io, base64
from google import genai
from IPython.display import display, Markdown

client = genai.Client()

image = PIL.Image.open('bear.jpg')
buffered = io.BytesIO()
image.save(buffered, format="JPEG")
img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {"type": "text", "text": "請告訴我這是什麼動物，還有關於它的一些資訊（請使用繁體中文回答）"},
        {"type": "image", "data": img_b64, "mime_type": "image/jpeg"}
    ]
)

display(Markdown(interaction.output_text))
```

### 多模態圖文問答整合 Gradio

程式檔案：[`image_text.py`](./image_text.py)

```python
import gradio as gr
import os
import io
import base64
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

with gr.Blocks() as demo:
    gr.Markdown('''
        1. 請先上傳圖片
        2. 再詢問 AI 對於圖片的問題
    ''')
    with gr.Row():
        image = gr.Image(type='pil')
        text_box = gr.Textbox(placeholder="請輸入對圖片的說明:", submit_btn=True)
    answer = gr.Markdown(min_height=100, container=True)

    @text_box.submit(inputs=[image, text_box], outputs=[answer, answer])
    def image_to_text(image, text_box, progress=gr.Progress()):
        if not image:
            gr.Warning("沒有圖片")
            return gr.Markdown(container=False), ""            
            
        if text_box == "":
            gr.Warning("請輸入文字")
            return gr.Markdown(container=False), ""
        progress(0.5, desc="請稍後")

        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                {"type": "text", "text": text_box},
                {"type": "image", "data": img_b64, "mime_type": "image/jpeg"}
            ]
        )
        progress(1, desc="完成")
        return gr.Markdown(container=True), (interaction.output_text or "")

    @image.upload(outputs=[answer, answer])
    def clear_answer():
        return gr.Markdown(container=False), ""

demo.launch()
```

![](./images/pic3.png)

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入多模態圖文辨識介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述多模態圖文辨識程式改寫為 Gradio 應用：
1. 介面分為左右兩欄，左側提供圖片上傳元件（gr.Image）與預設提問選項（如「辨識圖中物體」、「翻譯圖中文字」、「描述場景」），右側為問題輸入框與 Markdown 分析結果展示。
2. 整合 Gemini Interactions API 傳入 Base64 圖片與提示詞。
3. 上傳新圖片時自動清空舊的回覆並提示使用者提問。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述多模態圖文辨識程式改寫為 Streamlit 應用：
1. 使用 st.file_uploader 支援使用者上傳 JPG/PNG 圖片，並使用 st.image 即時預覽上傳圖片。
2. 提供 st.text_input 讓使用者輸入針對該圖片的提問（預設為「請詳細分析這張圖片的內容」）。
3. 將圖片轉為 Base64 後呼叫 Gemini 3.7 Flash Interactions API，並使用 st.chat_message 或 st.markdown 呈現圖文辨識結果。
```
</details>

---

## 5. 串流回應 (Streaming Responses)

設定 `stream=True`，並在迴圈中處理 `step.delta` 事件（當 `delta.type == "text"` 時取得即時文字）：

```python
from google import genai

client = genai.Client()
stream = client.interactions.create(
    model="gemini-3.7-flash",
    input="AI 是如何工作的（請使用繁體中文回答）？",
    stream=True
)

for event in stream:
    if event.event_type == "step.delta" and event.delta.type == "text":
        print(event.delta.text, end="", flush=True)
```

### 串流總結整合 Gradio

程式檔案：[`text_streaming.py`](./text_streaming.py)

```python
import os
import gradio as gr
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with gr.Blocks(title="Example") as demo:
    gr.Markdown("# Text To Summarization (串流總結)")
    style_radio = gr.Radio(['學術', '商業', '專業', '口語化', '條列式'], label='風格', info="請選擇總結風格", value='口語化') 
    input_text = gr.Textbox(
        label="請輸入文章",
        lines=10,
        submit_btn=True
    )
    output_md = gr.Markdown()

    @input_text.submit(inputs=[style_radio, input_text], outputs=[output_md])
    def generate_text(style: str, input_str: str):
        if style == "口語化":
            style_prompt = "請使用口語化的風格\n"
        elif style == "學術":
            style_prompt = "請使用專業學術的風格\n"
        elif style == "商業":
            style_prompt = "請使用商業文章的風格\n"
        elif style == "專業":
            style_prompt = "請使用專業風格\n"
        elif style == "條列式":
            style_prompt = "請條列式重點\n"
        else:
            style_prompt = f"請使用{style}風格\n"

        stream = client.interactions.create(
            model="gemini-3.7-flash",
            system_instruction=f"""
            你是一位文章的總結專家，也是一位繁體中文的高手。
            你的任務是:
            1. 請將內容`總結`
            2. {style_prompt}
            """,
            input=input_str,
            stream=True
        )

        result_text = ""
        for event in stream:
            if event.event_type == "step.delta" and event.delta.type == "text":
                result_text += event.delta.text
                yield f"{style_prompt}\n\n### 總結內容如下:\n" + result_text

demo.launch()
```

![](./images/pic5.png)

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入打字機串流效果介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述程式改寫為具有即時串流（Streaming / 打字機效果）的 Gradio 應用：
1. 建立文字輸入框與風格選單，按下送出後呼叫 stream=True 的 client.interactions.create。
2. 使用 Python generator 的 `yield` 語法，逐字更新輸出區的 Markdown 內容，實現流暢的打字機效果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為支援打字機串流輸出的 Streamlit 應用：
1. 使用 `st.write_stream` 或逐字迭代器（Generator）接收 Gemini API 串流事件。
2. 當 event.delta.type == "text" 時 yield 文字內容，讓 Streamlit 前端以原生打字機動畫流暢輸出。
3. 介面提供文章輸入與風格切換控制項。
```
</details>

---

## 6. 多輪對話 (Multi-turn Conversations)

Interactions API 支援**伺服器端狀態管理**。在呼叫時傳入上一輪的 `previous_interaction_id=interaction1.id`，伺服器會自動串接歷史上下文，客戶端不需每次傳遞完整對話歷史。

### 多輪對話基礎範例

```python
from google import genai
from IPython.display import display, Markdown

client = genai.Client()

# 第 1 輪
interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    input="我有 2 隻狗在我的房子內"
)
display(Markdown(interaction1.output_text))

# 第 2 輪（伺服器記住第 1 輪上下文）
interaction2 = client.interactions.create(
    model="gemini-3.7-flash",
    input="在我家裡有多少爪子？",
    previous_interaction_id=interaction1.id
)
display(Markdown(interaction2.output_text))
```

### 多輪對話結合串流 (Streaming)

```python
from google import genai

client = genai.Client()

interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    input="我有 2 隻狗在我的房子內"
)
print("第 1 輪回答：", interaction1.output_text)

print("\n第 2 輪回答（串流）：", end="")
stream = client.interactions.create(
    model="gemini-3.7-flash",
    input="在我家裡有多少爪子？",
    previous_interaction_id=interaction1.id,
    stream=True
)

for event in stream:
    if event.event_type == "step.delta" and event.delta.type == "text":
        print(event.delta.text, end="", flush=True)
```

### Chat 對話介面整合 Gradio

程式檔案：[`chat.py`](./chat.py)

```python
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
    fn=processing_chat,
    type="messages"
)

demo.launch()
```

![](./images/pic6.png)

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入多輪對話聊天機器人介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述多輪對話程式改寫為 Gradio Chat 應用程式：
1. 使用 `gr.ChatInterface` 或 `gr.Chatbot` 建立 ChatGPT 風格的聊天室介面。
2. 整合 Gemini Interactions API 的伺服器端狀態維護功能（利用 `previous_interaction_id` 紀錄前一輪 ID）。
3. 支援串流打字機回覆效果（在 fn 中使用 yield）。
4. 包含「重設對話 / 清空歷史」按鈕，重設時將 last_interaction_id 清空為 None。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述多輪對話程式改寫為 Streamlit 聊天機器人（Chatbot）：
1. 使用 `st.chat_message` 與 `st.chat_input` 構建現代化聊天介面。
2. 使用 `st.session_state` 儲存對話訊息列表與 `last_interaction_id`。
3. 呼叫 Gemini 3.7 Flash API 時帶入 `previous_interaction_id`，並支援 `stream=True` 即時輸出。
4. 側邊欄提供「清空對話」按鈕，點擊後重設對話紀錄與 ID。
```
</details>

---

## 7. 無狀態對話 (Stateless Conversations)

若需要由客戶端自行掌控對話歷史或不儲存於伺服器：
1. 在請求中設定 `store=False`。
2. 在客戶端維護 `steps` 陣列。
3. 後續請求將累計的步驟作為 `input` 傳入。

```python
from google import genai

client = genai.Client()

history = [
    {
        "type": "user_input",
        "content": [{"type": "text", "text": "我有 2 隻狗在我的房子內"}]
    }
]

# 第 1 輪
interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    store=False,
    input=history
)
print("第 1 輪：", interaction1.output_text)

# 將模型產生的 steps 記錄進歷史
for step in interaction1.steps:
    history.append(step.model_dump())

# 加入使用者第 2 輪問題
history.append({
    "type": "user_input",
    "content": [{"type": "text", "text": "在我家裡有多少爪子？"}]
})

# 第 2 輪
interaction2 = client.interactions.create(
    model="gemini-3.7-flash",
    store=False,
    input=history
)
print("第 2 輪：", interaction2.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入自訂歷史管理介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述無狀態對話（store=False）範例改寫為 Gradio Chatbot：
1. 在客戶端以 `gr.State` 維護對話步驟列表（steps）。
2. 每次送出訊息時，呼叫 `client.interactions.create(store=False, input=history)`，並將模型回傳的 steps 加回 state 中。
3. 支援查看與下載完整對話 JSON 結構。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述無狀態對話（store=False）範例改寫為 Streamlit 應用：
1. 在 `st.session_state` 中完全掌控對話步驟歷史（steps / history）。
2. 送出時以 `store=False` 呼叫 Gemini Interactions API，並展示聊天泡泡。
3. 側邊欄提供「檢視底層對話 JSON 結構」展開區塊（st.expander + st.json），方便教學與觀察模型輸入輸出結構。
```
</details>

---

## 8. 專案範例 Notebook

- [`quickstart.ipynb`](./quickstart.ipynb)：Interactions API 完整語法互動體驗
- [`tripPlanner.ipynb`](./tripPlanner.ipynb)：旅遊規劃與長文本結構化轉型範例

