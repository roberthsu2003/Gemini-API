## 匯率-(手動呼叫function)

### 定義function

```python
#定義function calling
import os
from IPython.display import display,Markdown
import requests

def get_exchange_rate(currency_from:str,currency_to:str,date:str='latest'):
    '''
    1. 取得目前查詢貨幣的匯率  
    2. 如果沒有指定日期,請設定currency_date=latest

	Args:  
        currency_date:如果沒有指定日期,請設定currency_date=latest,日期,格式必需是YYYY-MM-DD  
        currency_from:要被轉換的貨幣名稱,必需附合`ISO 4217`  
        currency_from:要轉換成為的貨敝名稱,必需附合`ISO 4217`

	Returns:  
        傳出一指定的dictionary,各個key的說明如下  
        date:查詢的日期  
        from_currency:當作基準貨幣名稱  
        to_currency:當作要轉換成為的貨幣名稱  
        rate:匯率
    '''
    if not date:
        date = 'latest' 
    url = f'https://api.frankfurter.app/{date}?base={currency_from}&symbols={currency_to}'
    response = requests.get(url)
    rate = response.json()['rates'][currency_to]
    return{
        "date":date,
        "from_currency":currency_from,
        "to_currency":currency_to,
        "rate":rate
    }
```

## 手動呼叫function

```python
#手動呼叫function,手動產生response
#為什麼要如此做呢?因為如果執行function有raise exception,我們可以手動處理
#可以加強程式的可靠度

from google import genai
from google.genai import types
import os
from IPython.display import display,Markdown 

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

# 手動函式呼叫:把「自動函式呼叫」關閉,模型只會回傳 function_call,不會自己執行
config = types.GenerateContentConfig(
    tools=[get_exchange_rate],
    system_instruction="如果沒有指定日期,請設定date='latest'",
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

chat = client.chats.create(model='gemini-flash-latest', config=config)
response = chat.send_message('2024-12-04,200歐幣對換澳幣是多少錢?')

return_values = None
for part in response.candidates[0].content.parts: #手動取出所有的引數值和function名稱
    if part.function_call:
        fn = part.function_call
        print(fn)
        args = {key: val for key, val in fn.args.items()}
        try:
            return_values = get_exchange_rate(**args) #手動呼叫function,如果有出錯會raise錯誤
            print(return_values)
        except Exception:
            print("目前系統有問題")
    elif part.text:
        print(part.text) #如果只有 text,代表模型沒有觸發 function_call
```

## 手動產生part內的response

```python
#手動把函式的傳回值送回模型,由模型整理成最終文字
function_response_part = types.Part.from_function_response(
    name='get_exchange_rate',
    response={'result': return_values}
)
response = chat.send_message(function_response_part)
print(response.text)
```

**回覆**

```
200歐元在2024-12-04的匯率為1歐元兌1.6384澳元，因此200歐元可兌換327.68澳元。
```


