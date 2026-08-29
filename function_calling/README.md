# Gemini 函式呼叫 (Function Calling)

**Function Calling（函式呼叫）** 讓您可以將 Gemini 模型連接到自訂的外部工具、資料庫與第三方 API。

模型本身**不會直接執行**您的程式碼，而是會依據使用者的自然語言需求，判斷在何時應該呼叫哪個函式，並自動生成滿足該函式參數要求的**結構化參數 (Arguments)**。您的應用程式負責在本地端或伺服器執行該函式，再將結果回傳給模型，模型隨後整合執行結果產出自然流暢的最終回覆。

---

## 核心應用場景 (Primary Use Cases)

- ⚡ **執行實體動作 (Take Actions)**：透過 API 與外部系統互動，例如建立行事曆會議、發送 Email、控制智慧家庭裝置、新增訂單。
- 🌐 **擴充即時知識 (Augment Knowledge)**：存取模型訓練資料以外的即時資料，例如查詢即時天氣、連線內部關聯式資料庫、呼叫股票即時 API。
- 📊 **擴展運算能力 (Extend Capabilities)**：調用外部工具克服純語言模型的數學或繪圖限制，例如科學計算機、動態生成圖表、繪製資料視覺化圖形。

---

## 運作流程 (How Function Calling Works)

![Function Calling 工作流程](https://ai.google.dev/static/gemini-api/docs/images/function-calling-overview.png)

完整的 Function Calling 互動包含 4 個標準步驟：
1. **宣告函式 (Define Declaration)**：向模型提供函式名稱、用途說明與參數規格（JSON Schema 或 Python 函式 Docstring）。
2. **傳入模型 (Call Model with Tools)**：將使用者 Prompt 與工具宣告（`tools`）一同送給 Gemini。
3. **本機執行 (Execute Function)**：模型回傳 `function_call` 步驟，應用程式提取函式名稱與參數並執行實體邏輯。
4. **回傳結果 (Send Result Back)**：將函式輸出以 `function_result` 步驟傳回模型，模型產出整合後的最終答案。

> [!IMPORTANT]
> **Gemini 3 世代重要更新**：
> 1. 模型會為每次函式呼叫產生唯一的 `id`（如 `call_id`）。回傳結果時請務必帶入對應的 `call_id`。
> 2. 原生支援平行呼叫（單一請求發出多個 `function_call`）與思考模式（Thinking Models / Thought Signatures）。
> 3. 建議使用新一代 Interactions API 或最新版 `google-genai` SDK。

---

## 1. 執行實體動作：預約會議 (Schedule Meeting)

本範例示範如何透過函式宣告讓模型精準解析自然語言中的人名、日期與時間，並觸發外部會議建立邏輯。

### Python (Interactions API 推薦寫法)

```python
import json
import os
from google import genai

# 1. 定義函式宣告 (JSON Schema)
schedule_meeting_function = {
    "type": "function",
    "name": "schedule_meeting",
    "description": "在指定的日期與時間，為指定的與會人員安排會議。",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "與會人員姓名清單",
            },
            "date": {"type": "string", "description": "會議日期，格式 YYYY-MM-DD"},
            "time": {"type": "string", "description": "會議時間，格式 HH:MM"},
            "topic": {"type": "string", "description": "會議主題"},
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# 2. 實作本地端執行函式
def schedule_meeting(attendees: list[str], date: str, time: str, topic: str) -> dict:
    print(f"[系統執行] 已在行事曆中建立「{topic}」，與會者：{', '.join(attendees)}")
    return {"status": "success", "meeting_id": "mtg-20250314-001", "message": "預約成功"}

client = genai.Client()

# 步驟 1: 發送請求與工具宣告
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請幫我和 Bob、Alice 安排一場 2025-03-14 上午 10:00 的會議，討論 Q3 產品規劃。",
    tools=[schedule_meeting_function],
)

# 步驟 2: 檢查模型是否發出函式呼叫
fc_step = next((s for s in interaction.steps if s.type == "function_call"), None)

if fc_step:
    print(f"模型呼叫函式: {fc_step.name} (Call ID: {fc_step.id})")
    print(f"引數: {fc_step.arguments}")

    # 步驟 3: 執行本地函式
    result = schedule_meeting(**fc_step.arguments)

    # 步驟 4: 將結果回傳給模型產出最終回覆
    final_interaction = client.interactions.create(
        model="gemini-3.7-flash",
        previous_interaction_id=interaction.id,
        tools=[schedule_meeting_function],
        input=[
            {
                "type": "function_result",
                "name": fc_step.name,
                "call_id": fc_step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            }
        ],
    )
    print("\n最終回答:")
    print(final_interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧會議預約助理介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「會議預約 Function Calling」改寫為 Gradio 應用：
1. 介面提供對話框（gr.ChatInterface），使用者可以用口語輸入預約需求（例如「下週二下午三點找 David 討論預算」）。
2. 當模型觸發 schedule_meeting 時，在右側面板即時顯示「預約確認卡片」（包含主題、日期時間、與會者名單）。
3. 支援一鍵點擊確認將行程存入模擬行事曆表格（gr.Dataframe）。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述會議預約程式改寫為 Streamlit 應用：
1. 介面提供 st.chat_input 接收自然語言會議指令。
2. 呼叫 Gemini Function Calling 提取會議參數。
3. 介面以 st.status 呈現函式呼叫執行進度，並以 st.success 呈現預約成功細節與會議日曆卡片。
```
</details>

---

## 2. 擴充即時知識：即時天氣查詢 (Get Weather)

透過自訂的天氣 API 函式，使模型具備回答即時氣候資訊的能力。

### Python 範例

```python
import json
from google import genai

weather_function = {
    "type": "function",
    "name": "get_current_temperature",
    "description": "取得指定城市的即時溫度與天氣狀況。",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "城市名稱，如：台北、東京、倫敦"}
        },
        "required": ["location"],
    },
}

def get_current_temperature(location: str) -> dict:
    return {"location": location, "temperature": "24°C", "condition": "晴時多雲"}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請問台北今天天氣如何？",
    tools=[weather_function],
)

fc_step = next(s for s in interaction.steps if s.type == "function_call")
result = get_current_temperature(**fc_step.arguments)

final_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction.id,
    tools=[weather_function],
    input=[
        {
            "type": "function_result",
            "name": fc_step.name,
            "call_id": fc_step.id,
            "result": [{"type": "text", "text": json.dumps(result)}],
        }
    ],
)
print(final_interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：全球即時天氣查詢儀表板</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述天氣查詢 Function Calling 程式改寫為 Gradio 儀表板：
1. 提供城市名稱輸入框與熱門城市按鈕（台北、紐約、巴黎、東京）。
2. 當模型執行 get_current_temperature 後，以漂亮的氣候卡片展示氣溫、濕度與天氣圖示。
3. 根據氣候狀態提供穿衣與攜帶雨具之智慧建議。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述天氣程式改寫為 Streamlit 應用：
1. 使用 st.text_input 輸入查詢城市或自然語言問句。
2. 透過 Function Calling 獲取結構化氣溫數據。
3. 使用 st.metric 展示當前氣溫與溫差，並以 st.info 呈現模型生成的出行建議。
```
</details>

---

## 3. 擴展運算與視覺化：動態圖表生成 (Create Chart)

透過函式呼叫讓模型將自然語言中的統計數據整理成圖表參數，再由前端繪製。

```python
import json
from google import genai

create_chart_function = {
    "type": "function",
    "name": "create_bar_chart",
    "description": "根據給定的標題、標籤與數值建立長條圖。",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "圖表標題"},
            "labels": {"type": "array", "items": {"type": "string"}, "description": "各長條標籤"},
            "values": {"type": "array", "items": {"type": "number"}, "description": "各長條對應數值"},
        },
        "required": ["title", "labels", "values"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請為我建立一份 2025 各季營收長條圖：Q1 是 5000 萬、Q2 是 7500 萬、Q3 是 6200 萬、Q4 是 8800 萬。",
    tools=[create_chart_function],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"呼叫圖表繪製: {step.name}")
        print(f"圖表參數: {step.arguments}")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：自然語言智慧圖表生成平台</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「圖表生成 Function Calling」改寫為 Gradio 應用：
1. 使用者輸入任何包含統計數據的文章或對話。
2. 模型呼叫 create_bar_chart 提取 labels 與 values。
3. 本地使用 Plotly 或 Matplotlib 繪製高品質長條圖，並以 gr.Plot 即時呈現。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述圖表生成程式改寫為 Streamlit 應用：
1. 提供文字輸入框輸入財務或銷售數據描述。
2. 取得圖表參數後，使用 st.bar_chart 或 Plotly 動態渲染互動式長條圖。
3. 同步以 st.dataframe 展示原始數據表格並提供 CSV 下載。
```
</details>

---

## 4. 平行函式呼叫 (Parallel Function Calling)

當使用者的單一請求包含多個獨立動作時，Gemini 可以在單次回應中**同時觸發多個函式呼叫**。

```python
import json
from google import genai

power_disco_ball = {
    "type": "function",
    "name": "power_disco_ball",
    "description": "開啟或關閉旋轉迪斯可球燈電源。",
    "parameters": {
        "type": "object",
        "properties": {"power": {"type": "boolean"}},
        "required": ["power"],
    },
}

start_music = {
    "type": "function",
    "name": "start_music",
    "description": "播放派對音樂。",
    "parameters": {
        "type": "object",
        "properties": {
            "energetic": {"type": "boolean"},
            "loud": {"type": "boolean"},
            "bpm": {"type": "integer"},
        },
        "required": ["energetic", "loud"],
    },
}

dim_lights = {
    "type": "function",
    "name": "dim_lights",
    "description": "調整室內主燈亮度。",
    "parameters": {
        "type": "object",
        "properties": {"brightness": {"type": "number"}},
        "required": ["brightness"],
    },
}

tools = [power_disco_ball, start_music, dim_lights]
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="把家裡切換成派對模式！",
    tools=tools,
)

fc_steps = [s for s in interaction.steps if s.type == "function_call"]
print(f"一次觸發了 {len(fc_steps)} 個設備動作！")

results_payload = []
for step in fc_steps:
    print(f"執行動作: {step.name}({step.arguments})")
    results_payload.append({
        "type": "function_result",
        "name": step.name,
        "call_id": step.id,
        "result": [{"type": "text", "text": json.dumps({"status": "ok"})}]
    })

# 批量回傳平行結果
final = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction.id,
    tools=tools,
    input=results_payload
)
print(final.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧家庭場景聯動控制台</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述平行呼叫程式改寫為 Gradio 智慧家庭控制面板：
1. 介面提供預設情境按鈕（「派對模式」、「睡眠模式」、「離家模式」、「觀影模式」）與自訂文字輸入。
2. 偵測並平行執行多個家電指令。
3. 介面以狀態開關與燈光顏色即時反應用戶家中各設備的最新運作狀態。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述平行控制程式改寫為 Streamlit 應用：
1. 介面提供語音/文字指令輸入框。
2. 觸發平行 Function Calling 時，使用 st.columns 分割顯示各智慧設備（燈光、音樂、空調）的執行動畫與狀態 Badge。
```
</details>

---

## 5. 組合式與多步驟呼叫 (Compositional Function Calling)

針對具備先後順序或邏輯依賴的複雜需求（例如「先查詢倫敦天氣，若大於 20 度則將冷氣調至 20 度，否則設為 18 度」），模型會依序分步發出呼叫。

```python
from google import genai

get_weather_declaration = {
    "type": "function",
    "name": "get_weather_forecast",
    "description": "取得指定地點的即時氣溫。",
    "parameters": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"],
    },
}

set_thermostat_declaration = {
    "type": "function",
    "name": "set_thermostat_temperature",
    "description": "設定溫控器目標溫度（攝氏）。",
    "parameters": {
        "type": "object",
        "properties": {"temperature": {"type": "integer"}},
        "required": ["temperature"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="如果倫敦現在氣溫高於 20 度，請將空調設為 20 度；否則設為 18 度。",
    tools=[get_weather_declaration, set_thermostat_declaration],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"第一階段呼叫: {step.name}({step.arguments})")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多步驟自動化決策工作流</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述組合式呼叫改寫為 Gradio 自動化決策流程圖：
1. 使用者輸入帶有條件判斷的指令。
2. 介面以逐步展開的 Accordion 展示多輪 Function Call 執行歷程。
3. 最終展示自動化執行的決策路徑與結果摘要。
```
</details>

---

## 6. 工具呼叫模式設定 (Tool Choice Modes)

可透過 `generation_config` 控制模型呼叫工具的行為模式：

- **`auto` (預設)**：由模型自主判斷是否呼叫函式或直接文字回答。
- **`any`**：強制模型**必須**呼叫函式，不可直接文字回答（可限定特定函式清單）。
- **`none`**：禁止模型呼叫任何函式，僅進行標準文字回答。
- **`validated`**：嚴格驗證函式參數 Schema 符合性。

```python
from google import genai

client = genai.Client()

# 強制要求模型必須呼叫 get_current_temperature 工具
generation_config = {
    "tool_choice": {
        "allowed_tools": {
            "mode": "any",
            "tools": ["get_current_temperature"]
        }
    }
}

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="紐約的即時氣溫",
    tools=[weather_function],
    generation_config=generation_config,
)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：工具模式切換與限制測試介面</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述 Tool Choice 控制改寫為 Streamlit 測試平台：
1. 介面提供單選按鈕讓使用者切換模式（AUTO / ANY / NONE）。
2. 在 ANY 模式下提供多選核取方塊指定允許呼叫的 Tool 清單。
3. 測試並檢視不同模式下模型輸出的行為差異（是否產生 function_call 或直接回覆文字）。
```
</details>

---

## 7. 混合使用：自訂函式結合 Google Search 聯網搜尋

Gemini 3 世代模型支援將內建工具（如 Google Search 聯網搜尋）與自訂 Function Calling 混合使用。

```python
import json
from google import genai

get_weather = {
    "type": "function",
    "name": "get_weather",
    "description": "取得特定地區的即時氣候資料。",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}

tools = [
    {"type": "google_search"},  # 內建 Google 搜尋
    get_weather                # 自訂函式
]

client = genai.Client()

prompt = "美國最北端的城市是哪裡？那裡現在的天氣如何？"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=tools,
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"模型搜尋後決定呼叫: {step.name} -> {step.arguments}")
        result = {"temperature": "-10°C", "condition": "大雪"}

        interaction_2 = client.interactions.create(
            model="gemini-3.7-flash",
            previous_interaction_id=interaction.id,
            tools=tools,
            input=[{
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}]
            }]
        )
        print(interaction_2.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：全方位聯網與工具整合助理</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將「Google Search + 自訂 Function Calling」改寫為 Gradio 應用：
1. 使用者輸入複雜查詢（如包含未知知識與實體動作）。
2. 介面以狀態標籤標示：哪些資訊由 Google Search 提供、哪些數據由自訂 Function 呼叫取得。
3. 整合為完整的圖文回答卡片。
```
</details>

---

## 8. 多模態函式回傳 (Multimodal Function Responses)

Gemini 3 支援在函式回傳（`function_result`）中包含**圖片**或**音訊**等多模態數據，模型能在後續對話中理解並分析該圖片：

```python
import base64
import requests
from google import genai

client = genai.Client()

# 假設函式執行後下載了一張圖片
image_bytes = requests.get("https://goo.gle/instrument-img").content
base64_image = base64.b64encode(image_bytes).decode("utf-8")

# 將圖片作為 function_result 回傳給模型
final_interaction = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction.id,
    input=[
        {
            "type": "function_result",
            "name": "fetch_instrument_image",
            "call_id": tool_call.id,
            "result": [
                {"type": "text", "text": "成功取得樂器照片"},
                {
                    "type": "image",
                    "mime_type": "image/jpeg",
                    "data": base64_image,
                },
            ],
        }
    ],
)
print(final_interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多模態圖片生成與檢索檢視介面</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述多模態 Function Result 改寫為 Streamlit 圖片分析應用：
1. 輸入想要搜尋或生成的商品描述。
2. 函式回傳商品圖片 Base64 數據。
3. 介面同時呈現回傳的圖片預覽與 Gemini 針對該圖片的細節分析解說。
```
</details>

---

## 9. 最佳實踐 (Best Practices)

1. **清晰明確的函式與參數描述 (`description`)**：
   - 描述中應清楚說明「何時該呼叫此函式」以及「參數格式與單位」（如：`YYYY-MM-DD`、`攝氏溫度`）。
2. **謹慎設定必要參數 (`required`)**：
   - 將核心參數標記為必填，選填參數請標示預設值行為。
3. **避免過度龐大的工具清單**：
   - 單次對話傳入 10~20 個以內最相關的函式，能有效維持模型的路由精確度。
4. **驗證與防呆處理**：
   - 在本地執行函式前，務必對模型傳入的參數進行型別與業務邏輯驗證，防範意外呼叫。
