# Google Search 聯網搜尋與即時查核 (Search Grounding)

大型語言模型（LLM）的最大限制之一是**訓練資料的截止時間**與**缺乏即時最新資訊**。

**Google Search Grounding（搜尋接地）** 讓 Gemini 能夠在推論過程中**自主判斷並發起 Google 搜尋**，從網際網路上檢索最新、權威的即時資訊，並在回覆中自動附帶**引用來源網址 (Sources & Citations)**，徹底消除資訊過期與事實幻覺問題。

---

## 核心優勢與應用場景

- ⚡ **即時動態資訊**：查詢今日頭條新聞、即時天氣、股價走勢、體育賽事即時比分。
- 🛡️ **事實查核與溯源 (Fact Checking)**：為回答提供權威佐證連結，增加回答的可信度。
- 🔄 **跨工具協同**：支援與 **Code Execution（程式碼執行）** 或 **Structured Output（結構化輸出）** 混合使用，實現「聯網搜尋 ➔ 數據清洗 ➔ 程式碼運算」的一條龍自動化。

---

## 快速語法概覽

```python
from google import genai

client = genai.Client()

# Interactions API 推薦寫法：啟用 Google Search 工具
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請查詢今天全球最熱門的科技新聞是什麼？",
    tools=[{"type": "google_search"}],
)
print(interaction.output_text)
```

---

## 1. 基礎聯網搜尋：查詢最新即時資訊 (Basic Search)

```python
import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = "請查詢今天台灣以及全球的最新科技要聞（包含 AI 最新進展），並條列式摘要。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：即時新聞與事實查核情報站</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Google Search 聯網程式改寫為 Gradio 即時情報站：
1. 提供搜尋關鍵字或問題輸入框（如「今天美股大盤走勢與關鍵原因」）。
2. 啟用 tools=[{"type": "google_search"}] 進行聯網搜尋。
3. 輸出區以 gr.Markdown 呈現結構化即時要聞，並以側邊欄附帶快捷熱門查詢按鈕（如「今日科技要聞」、「熱門國際焦點」）。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 介面提供搜尋列與自動重新整理按鈕。
2. 呼叫 Gemini 3.7 Flash 進行 Google Search 接地搜尋。
3. 主畫面以卡片排版呈現最新資訊摘要，並標記搜尋時間戳記。
```
</details>

---

## 2. 來源引用與事實溯源 (Citations & Sources)

模型在回答時會根據搜尋到的網頁提供事實佐證。

```python
from google import genai

client = genai.Client()

prompt = "2024 年奧運男子百米金牌得主是誰？成績是多少？請提供出處與相關新聞來源。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
)

print("=== 回答內容 ===")
print(interaction.output_text)

print("\n=== 執行歷程與 Grounding 步驟 ===")
for step in interaction.steps:
    print(f"步驟類型: {step.type}")
    if hasattr(step, "grounding_metadata") and step.grounding_metadata:
        print("搜尋元數據:", step.grounding_metadata)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧事實查核與引文溯源助理</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「Google Search 事實查核」改寫為 Gradio 查核助理：
1. 使用者輸入待驗證的陳述或問題（例如「某某公司是否真的被收購了？」）。
2. 模型聯網查證並給出真實性評估（真實 / 存疑 / 假消息）。
3. 在回答下方清楚列出參考來源網站與網址連結清單。
```
</details>

---

## 3. 混合使用：Google Search 結合 Code Execution

先聯網搜尋最新數據，再立即撰寫 Python 程式碼進行精確計算。

```python
from google import genai

client = genai.Client()

prompt = (
    "請搜尋 2024 年全球票房前 3 名的電影名稱與票房數字（美元），"
    "然後編寫並執行 Python 程式碼，計算它們的總票房以及若換算為新台幣（以 1:32.5 匯率計算）是多少億元。"
)

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[
        {"type": "google_search"},
        {"type": "code_execution"},
    ],
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：即時數據動態分析與試算面板</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將「Google Search + Code Execution 混合應用」改寫為 Streamlit 應用：
1. 提供輸入框讓使用者提問包含即時數據搜尋與統計計算的問題（如「比較各大金控今年前三季獲利與成長率」）。
2. 模型自主搜尋最新即時數據後，編寫 Python 進行統計試算。
3. 介面以 st.metric 與 st.dataframe 呈現精準數據計算結果。
```
</details>

---

## 4. 混合使用：Google Search 結合 Pydantic 結構化輸出

聯網搜尋即時市場資料，並自動轉化為型別安全、可直接入庫的結構化 JSON 資料。

```python
from typing import List
from google import genai
from pydantic import BaseModel, Field

class StockInfo(BaseModel):
    company_name: str = Field(description="公司名稱")
    stock_symbol: str = Field(description="股票代號")
    current_price: float = Field(description="最新股價 (USD)")
    price_change: str = Field(description="今日漲跌幅")
    recent_key_news: List[str] = Field(description="近期 2~3 則關鍵新聞摘要")

client = genai.Client()

prompt = "請搜尋 Apple (AAPL) 的最新即時股價與今日重要財經要聞，並整理為結構化資料。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "google_search"}],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": StockInfo.model_json_schema(),
    },
)

stock = StockInfo.model_validate_json(interaction.output_text)
print(stock.model_dump_json(indent=2))
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：即時金融與市場情資結構化看板</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述即時股價結構化擷取改寫為 Gradio 儀表板：
1. 提供股票代號/名稱輸入框（如 TSMC, NVDA, AAPL）。
2. 模型聯網抓取最新盤價與新聞並以 Pydantic JSON Schema 結構化輸出。
3. 介面以 gr.JSON 與 gr.Dataframe 呈現整齊的財務情報卡片。
```
</details>
