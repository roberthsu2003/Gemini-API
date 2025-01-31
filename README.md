# GeminiAPI的應用
主要著重於Gemini API,如何將大語言模型導入至目前的專案中

## [何謂AI Agent](./何謂AIAgent)

## 官方測試使用網站

[Google AI Studio](https://aistudio.google.com/prompts/new_chat)

## 說明文件

[參考網址](https://github.com/googleapis/python-genai?tab=readme-ov-file)

## 套件需求
- requirements.txt

```
google-generativeai
python-dotenv
ipywidgets
```

## 1. [生成文字](./text_generation)
## 2. [讀取文件](./document_understanding)
## 3. [結構化輸出](./structure_output)
## 4. [產生程式碼](./code_execution)
## 5. [函式呼叫](./function_calling)
- [最簡單的呼叫](./function_calling/simple_sample.ipynb)
	- gradio範例1	
- [多個函式的使用](./function_calling/multiFunction.ipynb)
- [ChatSession.history](./function_calling/history.ipynb)
- [手動管理函式呼叫](./function_calling/manual_function_calling.ipynb)
- [鍊結呼叫(依順序呼叫多個function)](./function_calling/function_calling_chain.ipynb)
- [平行呼叫(同時呼叫)](./function_calling/parallel_function_call.ipynb)
- [從結構資料中截取資料](./function_calling/extract_structured_data.ipynb)

## 6. Embedings
- [文件內容搜尋](./embeddings/document_search)

## 7. [開源模型](./開源模型)



