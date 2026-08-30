# 🛠️ 函式呼叫 (Function Calling & Tool Use)

透過 **函式呼叫 (Function Calling)**，您可以將自訂的 Python 函式、外部 API、資料庫操作或物聯網設備控制介面提供給 Gemini。模型能根據使用者的自然語言提問，**智慧判斷是否需要調用工具、提取精確參數並自動執行**，是打造自主 AI Agent 的核心支柱。

> 📖 **官方說明**：
> Google GenAI SDK 支援將 Python 函式直接傳入 `tools` 清單，SDK 會自動解析函式的 Docstring 與型別標註生成 JSON Schema，並支援平行工具調用（Parallel Function Calling）與 Google Search 聯網混合。
> 官方文件：[Function calling - Google AI for Developers](https://ai.google.dev/gemini-api/docs/function-calling)

---

## 📑 目錄導覽

1. [會議預約外部動作執行 (01_meeting_scheduler.py)](#1-會議預約外部動作執行-01_meeting_schedulerpy)
2. [即時天氣查詢工具整合 (02_weather_assistant.py)](#2-即時天氣查詢工具整合-02_weather_assistantpy)
3. [多工具平行呼叫 (03_parallel_function_calling.py)](#3-多工具平行呼叫-03_parallel_function_callingpy)
4. [聯網搜尋 + 自訂工具混合調用 (04_multi_tool_search_and_function.py)](#4-聯網搜尋--自訂工具混合調用-04_multi_tool_search_and_functionpy)
5. [課堂互動筆記本 (Jupyter Notebooks)](#5-課堂互動筆記本-jupyter-notebooks)

---

## 1. 會議預約外部動作執行 (`01_meeting_scheduler.py`)

定義外部 Python 函式並交由 Gemini 決定何時調用與提取參數：

- 核心程式檔案：[`01_meeting_scheduler.py`](./01_meeting_scheduler.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

def schedule_meeting(topic: str, date: str, participants_count: int) -> dict:
    """在行事曆中預約新會議。"""
    return {"status": "success", "room": "101 會議室", "topic": topic}

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="請幫我預約下週三 2026-09-02 的『Q4 產品策略會議』，預計 8 人參加。",
    config=types.GenerateContentConfig(
        tools=[schedule_meeting],
    ),
)

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我開發 Gradio 智慧控制台：
1. 定義航班查詢與冷氣控制函式。
2. 傳入 Gemini Function Calling，介面接收用戶指令並展示工具執行的總結回覆。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit AI 智慧管家：
1. 定義飯店查詢與電影票訂購函式。
2. 使用 st.chat_input 接收用戶需求，調用 Gemini 執行對應工具並以 Markdown 渲染。
```

**Telegram Bot 工具管家 Prompt：**
```text
請幫我將 Function Calling 整合至 Telegram 機器人：
1. 定義天氣查詢與提醒設定函式。
2. 接收用戶訊息自動調用函式並將結果回應用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/agent 端點：
1. 傳入即時加密貨幣價格查詢函式。
2. 呼叫 Gemini 執行函式並將回覆封裝為 JSON 回傳。
```
</details>

---

## 2. 即時天氣查詢工具整合 (`02_weather_assistant.py`)

- 核心程式檔案：[`02_weather_assistant.py`](./02_weather_assistant.py)

---

## 3. 多工具平行呼叫 (`03_parallel_function_calling.py`)

- 核心程式檔案：[`03_parallel_function_calling.py`](./03_parallel_function_calling.py)

---

## 4. 聯網搜尋 + 自訂工具混合調用 (`04_multi_tool_search_and_function.py`)

- 核心程式檔案：[`04_multi_tool_search_and_function.py`](./04_multi_tool_search_and_function.py)

---

## 5. 課堂互動筆記本 (Jupyter Notebooks)

- [`basic_function_calling.ipynb`](./basic_function_calling.ipynb)：基礎函式呼叫教學筆記本
- [`multi_function_calling.ipynb`](./multi_function_calling.ipynb)：多函式自動路由筆記本
- [`parallel_function_calling.ipynb`](./parallel_function_calling.ipynb)：平行函式呼叫筆記本
- [`chat_function_history.ipynb`](./chat_function_history.ipynb)：對話歷史與函式呼叫整合筆記本
