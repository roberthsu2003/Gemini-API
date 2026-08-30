# ⚡ 程式碼執行 (Code Execution 沙盒運算)

Gemini 具備**自主撰寫並在 Google 安全沙盒中執行 Python 程式碼**的能力。當遇到精確數值計算、演算法推導、統計分析、CSV 資料處理或 Matplotlib 圖表繪製時，模型會自動編寫 Python 程式並即時運行取得真實輸出，徹底杜絕大語言模型的算術幻覺。

> 📖 **官方說明**：
> 只需在 `GenerateContentConfig` 中加入 `types.Tool(code_execution=types.ToolCodeExecution())` 即可啟用。
> 官方文件：[Code execution - Google AI for Developers](https://ai.google.dev/gemini-api/docs/code-execution)

---

## 📑 目錄導覽

1. [數學運算與演算法求解 (01_math_solver.py)](#1-數學運算與演算法求解-01_math_solverpy)
2. [載入 CSV 數據進行 Python 換匯計算 (02_currency_calculator.py)](#2-載入-csv-數據進行-python-換匯計算-02_currency_calculatorpy)
3. [Matplotlib 動態視覺化圖表生成 (03_matplotlib_plotter.py)](#3-matplotlib-動態視覺化圖表生成-03_matplotlib_plotterpy)
4. [圖片局部裁切縮放與視覺檢測 (04_image_zoom_inspection.py)](#4-圖片局部裁切縮放與視覺檢測-04_image_zoom_inspectionpy)
5. [課堂互動筆記本 (Jupyter Notebooks)](#5-課堂互動筆記本-jupyter-notebooks)

---

## 1. 數學運算與演算法求解 (`01_math_solver.py`)

啟用 `code_execution` 讓模型撰寫 Python 程式碼並在沙盒中執行：

- 核心程式檔案：[`01_math_solver.py`](./01_math_solver.py)
- 實務應用範例：[`app_gradio.py`](./app_gradio.py) ｜ [`app_streamlit.py`](./app_streamlit.py) ｜ [`app_telegram_bot.py`](./app_telegram_bot.py) ｜ [`app_fastapi.py`](./app_fastapi.py)

```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "請問第 50 個質數是多少？請使用 Python 程式碼演算並驗證，最後輸出答案。"

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉化為 Web / Bot / API 應用</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述程式碼執行範例改寫為 Gradio 應用：
1. 輸入框接收使用者的數學或演算法問題。
2. 啟用 code_execution 工具，輸出區以 Markdown 呈現 Python 執行歷程與最終結論。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我開發 Streamlit Python 沙盒運算儀表板：
1. 主畫面提供計算問題輸入與常用任務範例下拉選單。
2. 點擊按鈕後呼叫 Gemini 執行 Python 程式並將運算歷程動態呈現。
```

**Telegram Bot 運算小幫手 Prompt：**
```text
請幫我封裝為 Telegram 機器人：
1. 接收數學計算提問，在沙盒中執行 Python 程式碼。
2. 將運算解答回應用戶。
```

**FastAPI 後端 API 開發 Prompt：**
```text
請幫我建立 POST /api/execute 端點：
1. 接收運算 prompt，呼叫 Gemini 執行 Python 程式碼。
2. 將執行結果封裝為 JSON 回傳。
```
</details>

---

## 2. 載入 CSV 數據進行 Python 換匯計算 (`02_currency_calculator.py`)

- 核心程式檔案：[`02_currency_calculator.py`](./02_currency_calculator.py)

---

## 3. Matplotlib 動態視覺化圖表生成 (`03_matplotlib_plotter.py`)

- 核心程式檔案：[`03_matplotlib_plotter.py`](./03_matplotlib_plotter.py)

---

## 4. 圖片局部裁切縮放與視覺檢測 (`04_image_zoom_inspection.py`)

- 核心程式檔案：[`04_image_zoom_inspection.py`](./04_image_zoom_inspection.py)

---

## 5. 課堂互動筆記本 (Jupyter Notebooks)

- [`math_and_code_execution.ipynb`](./math_and_code_execution.ipynb)：程式碼執行互動教學筆記本
- [`currency_calculator.ipynb`](./currency_calculator.ipynb)：牌告匯率 CSV 程式碼計算筆記本
