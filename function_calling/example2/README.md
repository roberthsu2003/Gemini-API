## 匯率-(手動呼叫function)

### 定義function

```python
#定義function calling
import google.generativeai as genai
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

```
#手動呼叫function,手動產生response
#為什麼要如此做呢?因為如果執行function有raise exception,我們可以手動處理
#可以加強程式的可靠度

import google.generativeai as genai
import os
from IPython.display import display,Markdown 

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[get_exchange_rate],
    system_instruction='''
    如果沒有指定日期,請設定date='latest'
    '''
)

chat = model.start_chat() #手動呼叫
response = chat.send_message('2024-12-04,200歐幣對換澳幣是多少錢?')
try:
    if answer := response.text: #如果有text,代表prompt的文字有問題,檢查response,只有text,沒有function_call,如果正常呼叫時會沒有text,會raise錯誤
        print(answer)
        print(response)      
except:
    for part in response.parts: #手動取出所有的引數值和function名稱
            if fn := part.function_call:
                print(fn)
                args = {key:val for key,val in fn.args.items()}
                try:
                    return_values = get_exchange_rate(**args)#手動呼叫function,如果有出錯會raise錯誤
                    print(return_values)
                except:
                    print("目前系統有問題")

                

```

## 手動產生part內的response

```python
#手動產生response
response_parts = genai.protos.Part(function_response=genai.protos.FunctionResponse(name='get_exchange_rate', response={'result':return_values}))
response = chat.send_message(response_parts)
print(response.text)
```

**回覆**

```
200歐元在2024-12-04的匯率為1歐元兌1.6384澳元，因此200歐元可兌換327.68澳元。
```


