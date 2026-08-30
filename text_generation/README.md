# ✍️ Gemini 文字生成 (Interactions API 完整指南)

本章節介紹如何使用 Google Gemini 官方最新推薦的 **Interactions API** 進行文字生成、思考控制、系統設定、多模態理解、即時串流回應與狀態化多輪對話。

> 📖 **官方 Interactions API 簡介**：
> Interactions API 是 Gemini 3 世代推薦的統一互動介面。使用 `client.interactions.create()` 即可涵蓋單輪文字生成、多輪狀態化對話（伺服器端透過 `previous_interaction_id` 自動管理對話歷史）、串流傳輸（Streaming）與多模態圖文輸入。
> 官方文件：[Text generation - Google AI for Developers](https://ai.google.dev/gemini-api/docs/text-generation)

---

## 📑 目錄導覽

1. [快速開始：基礎文字生成 (01_basic_text.py)](#1-快速開始基礎文字生成-01_basic_textpy)
2. [思考模式深度控制 (02_thinking_mode.py)](#2-思考模式深度控制-02_thinking_modepy)
3. [系統指示詞與生成參數 (03_system_and_params.py)](#3-系統指示詞與生成參數-03_system_and_paramspy)
4. [多模態圖文輸入 (04_multimodal_image.py)](#4-多模態圖文輸入-04_multimodal_imagepy)
5. [即時打字機串流輸出 (05_streaming.py)](#5-即時打字機串流輸出-05_streamingpy)
6. [伺服器端狀態化多輪對話 (06_stateful_chat.py)](#6-伺服器端狀態化多輪對話-06_stateful_chatpy)
7. [客戶端無狀態多輪對話 (07_stateless_chat.py)](#7-客戶端無狀態多輪對話-07_stateless_chatpy)
8. [課堂互動筆記本 (Jupyter Notebooks)](#8-課堂互動筆記本-jupyter-notebooks)

---

## 1. 快速開始：基礎文字生成 (`01_basic_text.py`)

最基礎的單輪文字輸入與文字生成（Zero-shot Prompting）：

- 核心程式檔案：[`01_basic_text.py`](./01_basic_text.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 調用 Interactions API 進行單輪文字生成
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請用繁體中文以三點簡要說明什麼是 AI Agent（人工智慧代理）？"
)

# 使用便利屬性 output_text 取得模型輸出文字
print(interaction.output_text)
print(f"互動 ID: {interaction.id}")
```

> **便利屬性說明**：
> - `interaction.output_text`（字串）：自動合併模型回覆中最後連續的文字區塊。
> - `interaction.id`：當前互動的唯一識別碼，用於延續下一輪對話。

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述的 Gemini 基礎文字生成程式碼改寫為 Gradio 網頁應用程式：
1. 使用 gr.Blocks 建立介面，包含一個文字輸入框、送出按鈕與清除按鈕。
2. 使用 gr.Markdown 呈現模型的回覆。
3. 整合 client.interactions.create(model="gemini-3.7-flash", input=...) 邏輯。
4. 加入常用問題範例選單（gr.Examples）供點選測試。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述的 Gemini 文字生成程式碼改寫為 Streamlit 應用程式：
1. 使用 st.set_page_config 與 st.title 建立精美標題。
2. 提供 st.chat_input 接收使用者問題，並以 st.chat_message 呈現對話訊息。
3. 點擊送出時以 st.spinner 提示，並以 st.markdown 排版呈現結果。
```

**Telegram Bot 開發 Prompt：**
```text
請幫我將上述程式碼整合為 Telegram 機器人：
1. 使用 python-telegram-bot (v20+ 非同步架構)。
2. 支援 /start 歡迎指令。
3. 接收用戶文字訊息後，呼叫 Gemini 3.7 Flash Interactions API 並將回覆發送給用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我將上述程式碼封裝為 FastAPI 後端微服務：
1. 使用 Pydantic 定義請求模型（包含 prompt、model 等欄位）。
2. 提供 POST /api/generate 端點，接收請求後呼叫 Gemini 回傳 JSON 格式結果。
3. 加入 CORS 中介軟體以支援前端跨域呼叫。
```
</details>

---

## 2. 思考模式深度控制 (`02_thinking_mode.py`)

Gemini 3 系列模型（如 `gemini-3.7-flash`）具備創新的「**思考與推理（Thinking）**」機制。您可以透過 `generation_config` 中的 `thinking_level` 控制思考深度，以平衡品質、延遲與成本：

| `thinking_level` | 適用情境 | 特性與成本考量 |
| :--- | :--- | :--- |
| `minimal` | 簡易事實查詢、簡短文字翻譯 | 最低延遲、最省 Token |
| `low` | 摘要整理、通用問答 | 具備基礎脈絡檢查，性價比高 |
| `medium` | 邏輯分析、概念解釋、寫作規劃 | 適中的推理思考深度 |
| `high` | 複雜推理、數學運算、程式碼架構設計 | 最完整深度思考，品質最佳 |

- 核心程式檔案：[`02_thinking_mode.py`](./02_thinking_mode.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py)（支援思考等級切換）｜ [`app_streamlit.py`](./app_streamlit.py)（側邊欄思考滑桿）

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="一家公司有 A、B 兩位主管與 3 位工程師，每組需 1 主管 + 2 工程師，有幾種組合？請列出完整推導歷程。",
    generation_config={
        "thinking_level": "medium",  # 可選: "minimal", "low", "medium", "high"
        "temperature": 1.0           # 官方建議思考模式下維持預設 1.0
    }
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入思考深度控制介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述思考模式程式改寫為 Gradio 應用：
1. 介面設計包含提問輸入框與 thinking_level 單選按鈕（minimal, low, medium, high）。
2. 動態將選擇的思考深度傳入 generation_config。
3. 輸出區以 Markdown 呈現 Gemini 的思考推導與解答。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 側邊欄提供 st.select_slider 讓使用者自由調節思考深度（minimal, low, medium, high）。
2. 主畫面輸入問題後，呼叫 Gemini 3.7 Flash 進行深度推理回答。
3. 生成過程使用 st.spinner("AI 深度思考中...") 提供視覺反饋。
```
</details>

---

## 3. 系統指示詞與生成參數 (`03_system_and_params.py`)

透過 `system_instruction` 與 `generation_config` 精準規範模型的人設、行事風格與隨機性：

| 參數名稱 | 說明與取值範圍 | 典型應用建議 |
| :--- | :--- | :--- |
| `temperature` | 取值 `0.0` ~ `2.0`。控制輸出隨機性：值越低越確定、值越高越具創意。 | 程式碼/資料擷取建議 `0.0~0.3`；日常寫作建議 `0.7`；腦力激盪建議 `1.0+` |
| `max_output_tokens` | 限制模型最多產生的 Token 數量。 | 防止回覆過長，精準控制費用與長度 |
| `system_instruction` | 頂層系統指示詞，定義角色定位與語言規則。 | 設定繁體中文回答、專家口氣或輸出格式要求 |

- 核心程式檔案：[`03_system_and_params.py`](./03_system_and_params.py)
- 實務應用範例：[`app_streamlit.py`](./app_streamlit.py)（側邊欄參數調節面板）

```python
from google import genai

client = genai.Client()

system_instruction = """
你是一位資深 Python 架構師。
規則：一律使用繁體中文回答，解釋直切核心，符合 Python 3.10+ 現代語法標準。
"""

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    system_instruction=system_instruction,
    input="在 Python 中，什麼時候該用 dataclass，什麼時候該用 Pydantic？",
    generation_config={
        "temperature": 0.3,
        "max_output_tokens": 800
    }
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：打造文章風格總結專家介面</b></summary>

**Gradio 風格控制應用 Prompt：**
```text
請幫我開發一個文章風格總結的 Gradio 應用：
1. 包含文字輸入框供使用者貼上長篇文章。
2. 提供風格選項單選框（口語化、學術、商業、條列式）。
3. 提供 Temperature 滑桿（0.0 ~ 2.0）。
4. 根據所選風格動態組合 system_instruction，呼叫 Gemini 3.7 Flash 產出重點總結。
```
</details>

---

## 4. 多模態圖文輸入 (`04_multimodal_image.py`)

Gemini 具備原生的多模態理解能力，可同時傳入本地圖片檔案（PIL Image）與文字 Prompt 進行圖文分析：

- 核心程式檔案：[`04_multimodal_image.py`](./04_multimodal_image.py)
- 實務應用範例：[`app_telegram_bot.py`](./app_telegram_bot.py)（支援用戶直接傳照片進行分析）

```python
from google import genai
from PIL import Image

client = genai.Client()
image = Image.open("text_generation/bear.jpg")

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        "請詳細描述這張圖片的內容、動物特徵以及周圍的環境生態，請以繁體中文回答。",
        image
    ]
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：圖文多模態分析工作台</b></summary>

**Gradio 圖片問答介面 Prompt：**
```text
請幫我製作一個 Gradio 圖文問答應用：
1. 左側提供 gr.Image 圖片上傳區，右側提供提問輸入框與分析按鈕。
2. 接收上傳的 PIL Image 並與文字 Prompt 一同傳入 client.interactions.create(input=[prompt, image])。
3. 輸出區以 Markdown 呈現視覺解析報告。
```

**Telegram 圖片辨識 Bot Prompt：**
```text
請幫我擴充 Telegram 機器人：
1. 新增 MessageHandler(filters.PHOTO, handle_photo) 處理器。
2. 當使用者傳送圖片時，下載圖片並轉為 PIL Image。
3. 讀取圖片附帶的說明文字（caption），呼叫 Gemini 多模態能力分析後回應用戶。
```
</details>

---

## 5. 即時打字機串流輸出 (`05_streaming.py`)

使用 `stream=True` 可以啟用伺服器推送串流，並在終端機或 Web 介面實現流暢的打字機效果：

- 核心程式檔案：[`05_streaming.py`](./05_streaming.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py)（即時串流） ｜ [`app_fastapi.py`](./app_fastapi.py)（SSE 串流端點）

```python
import sys
from google import genai

client = genai.Client()

stream = client.interactions.create(
    model="gemini-3.7-flash",
    input="請寫一首關於『清晨山嵐與雲海』的優美現代散文詩（約 200 字），使用繁體中文。",
    stream=True
)

for event in stream:
    if event.event_type == "step.delta" and event.delta.type == "text":
        sys.stdout.write(event.delta.text)
        sys.stdout.flush()
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：打造打字機即時串流體驗</b></summary>

**FastAPI SSE 串流端點開發 Prompt：**
```text
請幫我使用 FastAPI 建立 SSE (Server-Sent Events) 串流 API：
1. 建立 POST /api/chat/stream 端點。
2. 呼叫 Gemini Interactions API (stream=True)。
3. 將每個 event.delta.text 封裝為 SSE 格式 (data: {chunk}\n\n) 透過 StreamingResponse 串流輸出。
```
</details>

---

## 6. 伺服器端狀態化多輪對話 (`06_stateful_chat.py`)

在 Interactions API 中，只需將前一輪的 `interaction.id` 傳入下一輪的 `previous_interaction_id`，Google 伺服器端就會自動維護完整的上下文歷史，無需客戶端手動拼接歷史對話字串：

- 核心程式檔案：[`06_stateful_chat.py`](./06_stateful_chat.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py)

```python
from google import genai

client = genai.Client()

# 第一輪對話
turn_1 = client.interactions.create(
    model="gemini-3.7-flash",
    input="你好！我預計下週去日本京都旅遊 3 天，喜歡歷史古蹟與抹茶甜點。"
)
print("第一輪回覆：", turn_1.output_text)

# 第二輪對話（透過 previous_interaction_id 延續上下文）
turn_2 = client.interactions.create(
    model="gemini-3.7-flash",
    input="針對剛才推薦的景點，請幫我規劃第 2 天的詳細時間行程表。",
    previous_interaction_id=turn_1.id
)
print("第二輪回覆：", turn_2.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：伺服器端狀態對話介面</b></summary>

**Streamlit 多輪對話開發 Prompt：**
```text
請幫我開發 Streamlit 聊天應用：
1. 使用 st.session_state 儲存 last_interaction_id 與對話紀錄。
2. 每次用戶送出新訊息時，將上一輪的 interaction_id 帶入 previous_interaction_id。
3. 支援一鍵清空對話並重置 interaction_id。
```
</details>

---

## 7. 客戶端無狀態多輪對話 (`07_stateless_chat.py`)

若應用場景需要完全自主控制對話歷史（例如本地除錯、自訂快照、儲存於本機資料庫），也可以手動在客戶端維護 Message List：

- 核心程式檔案：[`07_stateless_chat.py`](./07_stateless_chat.py)

---

## 8. 課堂互動筆記本 (Jupyter Notebooks)

- [`text_generation_quickstart.ipynb`](./text_generation_quickstart.ipynb)：Interactions API 入門操作筆記本
- [`trip_planner_system_instruction.ipynb`](./trip_planner_system_instruction.ipynb)：旅遊規劃與 System Instruction 實戰
