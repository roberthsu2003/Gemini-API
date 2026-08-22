# 產生程式碼

模型能夠產生和運行 Python 程式碼，並從結果中迭代學習，直到得出最終輸出。您可以使用此代碼執行功能來建立應用程式，從代碼推理中獲益，並產生文字輸出。例如，您可以在解決方程式或處理文字的應用程式中使用代碼執行。

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
response = client.models.generate_content(
    model='gemini-3.7-flash',
    contents='What is the sum of the first 50 prime numbers? '
             'Generate and run code for the calculation, and make sure you get all 50.',
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())]
    )
)

print(response.text)
```

> 新版 `google-genai` 以 `config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution())])` 啟用程式碼執行工具；舊版的 `tools='code_execution'` 字串寫法已淘汰。

**讀取產生的程式碼與執行結果**

回應會拆成多個 `part`，可分別取出模型文字、產生的程式碼與執行輸出：

```python
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print("文字:", part.text)
    if part.executable_code is not None:
        print("程式碼:\n", part.executable_code.code)
    if part.code_execution_result is not None:
        print("執行結果:\n", part.code_execution_result.output)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入程式碼執行與即時結果展示介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 Gemini Code Execution 程式改寫為 Gradio 應用：
1. 介面提供數學/邏輯計算問題輸入框（如「計算前 100 個斐波那契數中的質數」）。
2. 啟用 tools=[types.Tool(code_execution=types.ToolCodeExecution())]。
3. 介面分別展示三個區塊：(1) 模型文字說明、(2) 模型生成的 Python 程式碼區（帶語法高亮）、(3) 程式碼即時執行輸出的 stdout 結果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 提供計算問題輸入框與執行按鈕。
2. 呼叫 Gemini 3.7 Flash 並解析 candidates[0].content.parts。
3. 使用 `st.code` 顯示模型自行編寫的 Python 程式碼，使用 `st.info` 呈現執行結果，並以 `st.markdown` 呈現最終推論結論。
```
</details>

## chat內使用code execution

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

chat = client.chats.create(
    model='gemini-3.7-flash',
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())]
    )
)

response = chat.send_message(
    'What is the sum of the first 50 prime numbers? '
    'Generate and run code for the calculation, and make sure you get all 50.')

print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入支援 Code Execution 的 Chat 介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述在 Chat 中啟用 Code Execution 的程式改寫為 Gradio Chatbot 應用：
1. 使用 `gr.ChatInterface` 建立對話介面。
2. 後端建立具備 code_execution 工具的 client.chats.create 實例。
3. 使用者可連續提問複雜數據分析或計算問題，模型自動編寫並運行程式碼後回傳結果。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 對話介面：
1. 在 `st.session_state` 中維護 `client.chats.create` 物件與訊息歷史。
2. 使用 `st.chat_input` 讓使用者進行多輪對話，每次送出時呼叫 `chat.send_message`。
3. 支援展示對話中模型產生的可執行程式碼與運行結果。
```
</details>

**台灣銀行匯率換算**

```python
import os
from google import genai
from google.genai import types

with open('2025_01_29.csv',encoding='utf-8') as file:
    csv_content = file.read()

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
system_instruction = '''
    ## 請依據以下的csv格式的文字回答問題
    ## 這個表格是銀行的台幣和各幣值的轉換匯率
    ## 如果沒有資料,請輸出`沒有相關幣的資料`
    ## 規則:
        1.如果使用者輸入的是台幣要換取美金,換算公式為:
        `台幣/現金匯率本行賣出的美金價格=`
        2.如果使用者輸入的是美金換取台幣,換算公式為:
        `現金匯率本行買入美金*美金的金額=`
        3.如果不是換成台幣,請先將金額換成台幣後,再轉換為使用者要求的幣值

    ''' + csv_content

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents='我有10000的加拿大幣,換成美金幣是多少錢?',
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[types.Tool(code_execution=types.ToolCodeExecution())]
    )
)
print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：加入自然語言匯率精準計算介面</b></summary>

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

**輸出範例**：

```markdown
好的，我來幫你計算。

首先，我需要將你的加拿大幣換算成台幣，然後再將台幣換算成美金。

從提供的資料中，我找到加拿大幣的現金匯率(本行買入)為22.2，即期匯率(本行買入)為22.53，現金匯率(本行賣出)為23.11，即期匯率(本行賣出)為22.86，因為你是拿加拿大幣換成台幣，所以要使用現金匯率(本行買入)，因此計算公式是:

`10000 * 22.2 = 222000 台幣`

接下來，將台幣換算成美金，由於是台幣換成美金，所以要使用現金匯率(本行賣出)，美金的現金匯率(本行賣出)是32.95。計算公式如下:

`222000 / 32.95 = 美金`

```python
cad_to_twd = 10000 * 22.2
usd_amount = cad_to_twd / 32.95
print(f'{usd_amount=}')
```

```
usd_amount=6737.481031866464
```

因此，10000 加拿大幣大約可以換成 6737.48 美金。
```


