# 程式碼執行 (Code Execution)

**Code Execution（程式碼執行）** 是 Gemini 內建的強大工具，它賦予模型**自主編寫並在安全沙盒中執行 Python 程式碼**的能力。

模型在接收到複雜問題後，能夠生成 Python 程式碼、在 Google 託管的沙盒環境中運行、讀取執行輸出（若遇到錯誤會自動反思修正，最多重試 5 次），最終根據確定性的運算結果產出精確、無幻覺的答案。

---

## 核心應用場景

- 🧮 **精確數學與符號運算**：解決微積分、統計學、質數求解、方程式與大型數字計算（徹底消除 LLM 算術幻覺）。
- 📑 **數據處理與文字分析**：清洗複雜 CSV 表格、計算詞頻、正則表達式篩選。
- 🔍 **Gemini 3 圖片程式碼縮放與視覺分析 (Code Execution with Images)**：主動編寫影像處理程式碼對圖片進行局部裁切 (Crop)、縮放 (Zoom)、物體計數與量測。
- 📈 **Matplotlib 圖表動態生成**：在沙盒內繪製高品質長條圖、散佈圖、分佈圖，並將圖表以圖片形式回傳。

---

## 快速語法概覽

```python
from google import genai

client = genai.Client()

# Interactions API 推薦寫法
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="計算前 50 個質數的總和並印出。",
    tools=[{"type": "code_execution"}]
)
print(interaction.output_text)
```

> [!TIP]
> **API 呼叫方式對照**：
> - **Interactions API**：`tools=[{"type": "code_execution"}]`
> - **GenerateContent API**：`config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution())])`
> - **回傳步驟解構**：Interactions 回應中的 `steps` 包含 `code_execution_call`（生成的程式碼）、`code_execution_result`（執行結果 stdout）與 `model_output`（最終回覆文字或圖片）。

---

## 1. 數學運算與演算法求解 (Math & Algorithm Solver)

本範例展示模型如何透過編寫並執行 Python 程式碼精確計算前 50 個質數之和。

```python
from google import genai

client = genai.Client()

prompt = (
    "請計算前 50 個質數的總和。"
    "請編寫並執行 Python 程式碼來計算，確保取出完整的 50 個質數。"
)

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "code_execution"}],
)

print("=== 執行歷程步驟 ===")
for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- [模型自主編寫的 Python 程式碼] ---")
        code = step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code
        print(code)
    elif step.type == "code_execution_result":
        print("\n--- [沙盒環境執行結果 (stdout)] ---")
        print(step.result)
    elif step.type == "model_output":
        for block in step.content:
            if hasattr(block, "text") and block.text:
                print("\n--- [模型最終結論] ---")
                print(block.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧數學與邏輯求解平台</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Gemini Code Execution 數學求解程式改寫為 Gradio 應用：
1. 介面提供數學/邏輯計算問題輸入框（如「計算前 100 個斐波那契數中的偶數總和」）。
2. 啟用 tools=[{"type": "code_execution"}]。
3. 介面分別展示三個區塊：(1) 模型文字說明、(2) 模型生成的 Python 程式碼區（帶語法高亮）、(3) 程式碼即時執行輸出的 stdout 結果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 提供計算問題輸入框與執行按鈕。
2. 呼叫 Gemini 3.7 Flash 並解析 interaction.steps。
3. 使用 st.code 顯示模型自行編寫的 Python 程式碼，使用 st.info 呈現執行結果，並以 st.markdown 呈現最終推論結論。
```
</details>

---

## 2. 多輪對話中的程式碼執行 (Multi-Turn Chat with Code Execution)

在多輪連續對話中，模型能延續前一輪的程式碼執行結果進行深入探討。

```python
from google import genai

client = genai.Client()

# 第一輪：提出初始問題
interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    input="我有關於統計分佈與數據計算的問題想請教你。",
    tools=[{"type": "code_execution"}]
)
print("Turn 1:", interaction1.output_text)

# 第二輪：延續上下文進行精確計算
interaction2 = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction1.id,
    input="請計算 1 到 1000 之間所有能被 7 整除但不能被 5 整除的整數個數與總和。",
    tools=[{"type": "code_execution"}]
)

print("\nTurn 2 最終回答:\n", interaction2.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：智慧資料科學對話助理</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述多輪對話 Code Execution 程式改寫為 Gradio Chatbot 應用：
1. 使用 gr.ChatInterface 建立對話介面。
2. 每次對話帶入 previous_interaction_id 維護上下文並啟用 code_execution 工具。
3. 使用者可連續提問複雜數據分析或計算問題，模型自動編寫並運行程式碼後回傳結果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述多輪對話改寫為 Streamlit 應用：
1. 在 st.session_state 中維護對話歷史與 previous_interaction_id。
2. 使用 st.chat_input 讓使用者進行多輪對話。
3. 支援以摺疊區塊 (st.expander) 展示每一輪對話中模型產生的可執行 Python 程式碼與運行輸出。
```
</details>

---

## 3. Gemini 3 圖片程式碼縮放與視覺分析 (Code Execution with Images)

Gemini 3 Flash 支援主動透過編寫 Python 程式碼對圖片進行局部裁切、縮放與精準檢測。

```python
import base64
import requests
from google import genai

# 載入圖片資料
image_url = "https://goo.gle/instrument-img"
image_bytes = requests.get(image_url).content
b64_image = base64.b64encode(image_bytes).decode("utf-8")

client = genai.Client()

prompt = "請放大並檢查這張管風琴下方的踏板 (Expression pedals)，數數看一共有幾個踏板？請編寫並執行 Python 程式碼進行局部裁剪與檢驗。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {"type": "image", "data": b64_image, "mime_type": "image/jpeg"},
        {"type": "text", "text": prompt},
    ],
    tools=[{"type": "code_execution"}],
)

for step in interaction.steps:
    if step.type == "code_execution_call":
        print("\n--- 影像處理程式碼 ---")
        code = step.arguments.get("code") if isinstance(step.arguments, dict) else step.arguments.code
        print(code)
    elif step.type == "code_execution_result":
        print("\n--- 執行輸出 ---")
        print(step.result)

print("\n--- 最終分析結果 ---")
print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多模態圖片局部縮放與細節量測介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Gemini 3 圖片 Code Execution 縮放分析改寫為 Gradio 應用：
1. 介面提供圖片上傳元件（gr.Image）與問題輸入框（如「請放大檢查左下角的儀表指針數值」）。
2. 呼叫 Gemini 3.7 Flash 並啟用 code_execution 工具。
3. 介面展示模型裁剪圖片的 Python 程式碼以及最終高解析度辨識結論。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述圖片程式碼縮放功能改寫為 Streamlit 應用：
1. 提供 st.file_uploader 上傳發票、工程圖或複雜照片。
2. 模型自主寫程式進行區域放大 (Crop & Zoom) 與計算。
3. 以 st.columns 分割呈現原圖、模型生成的裁切程式碼與精準辨識數據。
```
</details>

---

## 4. CSV 數據分析與精確匯率計算 (Data Analysis with CSV)

本範例結合真實臺灣銀行牌告匯率 CSV，模型自主撰寫 Python 公式完成跨幣別換匯計算。

```python
import os
from google import genai

with open("2025_01_29.csv", encoding="utf-8") as file:
    csv_content = file.read()

client = genai.Client()

system_instruction = f"""
## 請依據以下的臺灣銀行牌告匯率 CSV 表格內容回答問題：
{csv_content}

## 換算規則：
1. 外幣換台幣：使用「現金匯率(本行買入)」* 金額
2. 台幣換外幣：使用 金額 / 「現金匯率(本行賣出)」
3. 外幣 A 轉外幣 B：先轉為台幣，再轉為外幣 B。
"""

prompt = "我有 10,000 加拿大幣，如果換成美金大約是多少錢？請寫 Python 程式碼進行計算。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    system_instruction=system_instruction,
    tools=[{"type": "code_execution"}],
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：自然語言匯率精準計算機</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「透過 Code Execution 執行精準匯率計算」的程式改寫為 Gradio 應用：
1. 介面提供自然語言換匯提問輸入框（如「我有 50000 日圓想換成歐元是多少錢？」）。
2. 將牌告匯率 CSV 作為 system_instruction，並啟用 code_execution 工具，確保模型透過精確的 Python 程式碼計算而非幻覺估算。
3. 介面呈現計算過程、執行的 Python 運算式與最終兌換金額。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 載入 CSV 匯率表並注入 system_instruction。
2. 主畫面提供自然語言問題輸入框與常見提問範例按鈕。
3. 按下計算後，以 Streamlit 呈現模型調用 Code Execution 精確計算的過程與結果。
```
</details>

---

## 5. Matplotlib 動態繪圖與圖表生成 (Graph Output)

Gemini 內建沙盒支援 `matplotlib`，模型能直接生成繪圖程式碼並在回應中回傳**圖表圖片**。

```python
import base64
import io
from google import genai
from PIL import Image

client = genai.Client()

prompt = "請使用 Matplotlib 繪製常態分佈與指數分佈的機率密度比較圖，並產生圖表圖片。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[{"type": "code_execution"}],
)

for step in interaction.steps:
    if step.type == "model_output":
        for block in step.content:
            if hasattr(block, "text") and block.text:
                print(block.text)
            elif hasattr(block, "image") and block.image:
                print("[收到回傳圖表！正在儲存為圖檔...]")
                img_data = base64.b64decode(block.image.data)
                img = Image.open(io.BytesIO(img_data))
                img.save("distribution_chart.png")
                print("已儲存為 distribution_chart.png")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：自然語言自動繪圖與統計視覺化工具</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Matplotlib Code Execution 繪圖程式改寫為 Gradio 視覺化應用：
1. 使用者輸入想要的圖表主題（例如：「繪製 2024 年四大科技巨頭營收成長折線圖」）。
2. 模型撰寫 Matplotlib 程式碼並在沙盒中執行產生圖表。
3. 介面以 gr.Image 展示回傳的圖表圖片，並以 gr.Code 顯示後台繪圖程式碼。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述動態繪圖功能改寫為 Streamlit 應用：
1. 提供文字輸入框讓使用者自由描述圖表需求。
2. 接收 Code Execution 回傳的 inline image 數據，使用 st.image 即時展示高解析度圖表。
3. 提供一鍵下載圖表 PNG 檔案的按鈕。
```
</details>

---

## 6. 混合使用：Code Execution 結合 Google Search 聯網

模型可先透過 Google Search 搜尋最新即時數據，再立即撰寫 Python 程式碼進行彙整與統計計算。

```python
from google import genai

client = genai.Client()

prompt = "請搜尋 2024 年全球票房前 5 名的電影票房數字，並用 Python 程式碼計算它們的總票房與平均票房。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    tools=[
        {"type": "google_search"},
        {"type": "code_execution"}
    ],
)

print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：聯網數據即時分析與計算看板</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將「Google Search + Code Execution 混合工具」改寫為 Gradio 數據分析看板：
1. 使用者輸入包含即時搜尋與數值計算的題目。
2. 介面標註哪些資訊來自 Google 搜尋、展示模型編寫的 Python 計算過程與最終統計表格。
```
</details>

---

## 7. 環境支援與技術規格

### 內建支援的 Python 函式庫清單
沙盒環境預先安裝了常用資料科學與科學計算套件（不支援自行 pip install 外部套件）：
- **資料科學 / 數學**：`numpy`, `pandas`, `scipy`, `scikit-learn`, `sympy`, `mpmath`, `tabulate`
- **資料視覺化**：`matplotlib`, `seaborn`
- **影像與檔案處理**：`pillow (PIL)`, `opencv-python`, `imageio`, `openpyxl`, `xlrd`, `python-docx`, `python-pptx`, `PyPDF2`, `reportlab`
- **地理與結構化**：`geopandas`, `lxml`, `jsonschema`, `jinja2`, `tensorflow`

### 運行限制與規格 (Limitations & Limits)
- **執行逾時**：單次程式碼運行上限為 **30 秒**。
- **自動自我修正**：若程式碼發生錯誤 (Runtime Error / Syntax Error)，模型最多會**自動重新編寫與重試 5 次**。
- **檔案輸入支援**：支援傳入 CSV、文字檔與圖片；圖表輸出以 inline image 形式傳回。

---

## 8. 計費機制 (Billing & Tokens)

- 啟用 Code Execution **無需額外附加功能費用**，費用依據所使用模型的標準 Input / Output Token 費率計費。
- **中間 Token (Intermediate Tokens)**：模型生成的程式碼與沙盒執行輸出會被歸類為 Intermediate Tokens，計入 Input Tokens 費用。
- **最終 Token**：最終回傳給使用者的摘要、程式碼與輸出結果計入 Output Tokens 費用。
