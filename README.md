# GeminiAPI的應用
主要著重於Gemini API,如何將大語言模型導入至目前的專案中

## [何謂AI Agent](./何謂AIAgent)

## 官方測試使用網站

[Google AI Studio](https://aistudio.google.com/prompts/new_chat)

## 說明文件

[參考網址](https://github.com/googleapis/python-genai?tab=readme-ov-file)

## python版本需求

```
python 3.9
```

## 套件需求
- requirements.txt

```
google-genai
python-dotenv
ipywidgets
```

## 發出第一項要求

以下範例使用 generateContent 方法，透過 Gemini 2.5 Flash 模型傳送要求至 Gemini API。

如果您將 API 金鑰設為環境變數 GEMINI_API_KEY，使用 Gemini API 程式庫時，用戶端會自動取得該金鑰。否則，您需要在初始化用戶端時傳遞 API 金鑰做為引數。

請注意，Gemini API 文件中的所有程式碼範例，都假設您已設定環境變數 GEMINI_API_KEY。

```python
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

## 許多程式碼範例預設會開啟「思考」功能

本網站上的許多程式碼範例都使用 Gemini 2.5 Flash 模型，這個模型預設啟用「思考」功能，可提升回覆品質。請注意，這可能會增加回應時間和權杖用量。如果您優先考量速度或希望盡量降低成本，可以將思考預算設為零，停用這項功能，如下列範例所示。

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
)
print(response.text)
```

## 1. [生成文字](./text_generation)
## 2. [讀取文件](./document_understanding)
## 3. [結構化輸出](./structure_output)
## 4. [產生程式碼](./code_execution)
## 5. [函式呼叫](./function_calling)
- [最簡單的呼叫](./function_calling/simple_sample.ipynb)
	- [範例1-匯率(自動呼叫)](./function_calling/example1)
	- [範例2-匯率(手動呼叫)](./function_calling/example2)
	- [gradio範例](./function_calling/gradio_example1)	
- [多個函式的使用](./function_calling/multiFunction.ipynb)
- [ChatSession.history](./function_calling/history.ipynb)
- [手動管理函式呼叫](./function_calling/manual_function_calling.ipynb)
- [鍊結呼叫(依順序呼叫多個function)](./function_calling/function_calling_chain.ipynb)
- [平行呼叫(同時呼叫)](./function_calling/parallel_function_call.ipynb)
- [從結構資料中截取資料](./function_calling/extract_structured_data.ipynb)

## 6. Embedings
- [文件內容搜尋](./embeddings/document_search)

## 7. [開源模型](./開源模型)



