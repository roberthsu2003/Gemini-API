# 🌐 聯網搜尋與事實接地 (Google Search Grounding)

透過啟用 **Google Search Grounding（搜尋接地）**，讓 Gemini 3 世代模型在回答時能即時聯網搜尋 Google 搜尋引擎上的最新真實資料，突破模型訓練資料的截止時間限制，自動標註參考來源網址（Sources & Citations），有效消除事實幻覺。

> 📖 **官方說明**：
> Google Search Grounding 可與 Code Execution（程式碼執行）或 Structured Outputs（結構化輸出）無縫混合調用，實現「先聯網搜尋即時數據、再透過 Python 運算或結構化提取」的強大能力。
> 官方文件：[Grounding with Google Search - Google AI for Developers](https://ai.google.dev/gemini-api/docs/grounding)

---

## 📑 目錄導覽

1. [基礎 Google Search 聯網搜尋 (01_basic_search.py)](#1-基礎-google-search-聯網搜尋-01_basic_searchpy)
2. [解析搜尋步驟與引用來源網址 (02_search_citations.py)](#2-解析搜尋步驟與引用來源網址-02_search_citationspy)
3. [聯網搜尋 + 程式碼執行混合模式 (03_search_with_code_execution.py)](#3-聯網搜尋--程式碼執行混合模式-03_search_with_code_executionpy)
4. [聯網搜尋 + 結構化資料提取 (04_search_structured_output.py)](#4-聯網搜尋--結構化資料提取-04_search_structured_outputpy)

---

## 1. 基礎 Google Search 聯網搜尋 (`01_basic_search.py`)

在 `GenerateContentConfig` 中加入 `types.Tool(google_search=types.GoogleSearch())` 即可啟用聯網：

- 核心程式檔案：[`01_basic_search.py`](./01_basic_search.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="請查詢今天最新的重要國際科技新聞頭條三則，使用繁體中文。",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
    ),
)

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我開發 Gradio 聯網搜尋應用：
1. 提供問題輸入框，按下搜尋後呼叫 Gemini Google Search Grounding。
2. 回答區呈現 Markdown 報告，右側卡片列出所有引用來源與網址連結。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit 時事情報儀表板：
1. 側邊欄提供開關「啟用 Google Search 聯網」。
2. 主畫面輸入問題，以兩欄排版（左欄為回答，右欄為參考來源卡片）。
```

**Telegram Bot 查證機器人 Prompt：**
```text
請幫我建立 Telegram 即時查證機器人：
1. 用戶發送新聞或時事提問時，調用 Google Search 工具。
2. 回應用戶並在訊息底部附上最多三條來源新聞連結。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/search 端點：
1. 接收 query，呼叫 Gemini 聯網搜尋。
2. 將回答文字與 grounding_chunks 中的來源清單封裝為 JSON 回傳。
```
</details>

---

## 2. 解析搜尋步驟與引用來源網址 (`02_search_citations.py`)

從 `grounding_metadata` 提取搜尋關鍵字與參考網頁清單：

- 核心程式檔案：[`02_search_citations.py`](./02_search_citations.py)

---

## 3. 聯網搜尋 + 程式碼執行混合模式 (`03_search_with_code_execution.py`)

- 核心程式檔案：[`03_search_with_code_execution.py`](./03_search_with_code_execution.py)

---

## 4. 聯網搜尋 + 結構化資料提取 (`04_search_structured_output.py`)

- 核心程式檔案：[`04_search_structured_output.py`](./04_search_structured_output.py)
