# 產生程式碼

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

**台灣銀行匯率換算**

```
import google.generativeai as genai
import os

with open('2025_01_29.csv',encoding='utf-8') as file:
    csv_content = file.read()
    
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction='''
    ## 請依據以下的csv格式的文字回答問題
    ## 這個表格是銀行的台幣和各幣值的轉換匯率
    ## 如果沒有資料,請輸出`沒有相關幣的資料`
    ## 規則:
        1.如果使用者輸入的是台幣要換取美金,換算公式為:
        `台幣/現金匯率本行賣出的美金價格=`
        2.如果使用者輸入的是美金換取台幣,換算公式為:
        `現金匯率本行買入美金*美金的金額=`
        3.如果不是換成台幣,請先將金額換成台幣後,再轉換為使用者要求的幣值   
    
    ''' + csv_content,
    tools = 'code_execution'
    
)

response = model.generate_content('我有10000的加拿大幣,換成美金幣是多少錢?')
print(response.text)

#=====output===========
好的，我來幫你計算。

首先，我需要將你的加拿大幣換算成台幣，然後再將台幣換算成美金。

從提供的資料中，我找到加拿大幣的現金匯率(本行買入)為22.2，即期匯率(本行買入)為22.53，現金匯率(本行賣出)為23.11，即期匯率(本行賣出)為22.86，因為你是拿加拿大幣換成台幣，所以要使用現金匯率(本行買入)，因此計算公式是:

`10000 * 22.2 = 222000 台幣`

接下來，將台幣換算成美金，由於是台幣換成美金，所以要使用現金匯率(本行賣出)，美金的現金匯率(本行賣出)是32.95。計算公式如下:

`222000 / 32.95 = 美金`


``` python
cad_to_twd = 10000 * 22.2
usd_amount = cad_to_twd / 32.95
print(f'{usd_amount=}')

```
```
usd_amount=6737.481031866464

```
因此，10000 加拿大幣大約可以換成 6737.48 美金。
```

