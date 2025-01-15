# 產生程式碼和執行程式碼

模型能夠產生和運行 Python 程式碼，並從結果中迭代學習，直到得出最終輸出。您可以使用此代碼執行功能來建立應用程式，從代碼推理中獲益，並產生文字輸出。例如，您可以在解決方程式或處理文字的應用程式中使用代碼執行。

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools='code_execution'
    )
response = model.generate_content(
    ('What is the sum of the first 50 prime numbers? ',
    'Generate and run code for the calculation, and make sure you get all 50.')
)

print(response.text)

```

**另一種寫法**

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel(model_name='gemini-1.5-pro')

response = model.generate_content(
    ('What is the sum of the first 50 prime numbers? '
    'Generate and run code for the calculation, and make sure you get all 50.'),
    tools='code_execution')

print(response.text)
```

## chat內使用code execution

```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ['API_KEY'])

model = genai.GenerativeModel(model_name='gemini-1.5-pro',
                              tools='code_execution')

chat = model.start_chat()

response = chat.send_message((
    'What is the sum of the first 50 prime numbers? '
    'Generate and run code for the calculation, and make sure you get all 50.'))

print(response.text)
```