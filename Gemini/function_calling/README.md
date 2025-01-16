# 函式呼叫

使用 Gemini API 函數呼叫功能，您可以為模型提供自訂函數定義。模型不會直接呼叫這些函數，而是產生指定函數名稱和建議參數的結構化輸出。然後您可以使用函數名稱和參數來呼叫外部 API，然後，您可以使用函數名稱和參數來呼叫外部 API，並將產生的 API 輸出合併到對模型的進一步查詢中，從而使模型提供更全面的回應並採取其他操作。函數呼叫使用戶能夠與資料庫、客戶關係管理系統和文件儲存庫等即時資訊和服務進行互動。該功能還增強了模型提供相關和上下文答案的能力。函數呼叫最適合與外部系統互動。如果您的用例需要模型執行計算但不涉及外部系統或 API，則應該考慮使用程式碼執行。

## 如何呼叫function

## function calling的講解

函式呼叫使您更容易從生成模型中獲取結構化資料輸出。然後，您可以使用這些輸出來呼叫其他 API 並將相關回應資料傳回給模型。換句話說，函數呼叫可以幫助您將產生模型連接到外部系統，以便產生的內容包含最新、最準確的資訊。

您可以為 Gemini 模型提供功能描述。這些是您使用應用語言編寫的函數（也就是說，它們不是 Google Cloud Functions）。模型可能會要求您呼叫函數並傳回結果以幫助模型處理您的查詢。

### 光線控制的API
想像你有一個基本控制光線的應用程式(api)和您允許使用者使用輸入的文字控制光線的明亮度和溫度.可以使用函數呼叫功能了解使用者改變亮度的要求和轉換它們進入到api.

| Parameter | Type | Required | Description |
|:--|:--|:--|:--|
| brightness | number | yes | Light level from 0 to 100. Zero is off and 100 is full brightness. |
| colorTemperature | string | yes | Color temperature of the light fixture which can be daylight, cool or warm. |

```python
{
  "brightness": "50",
  "colorTemperature": "daylight"
}
```

### 定義一個自訂的函式
建立一個符合API需求的函式,這個function一定是被定義在我們應用程式內,function內的程式可以呼叫外部的API.模型不會直接呼叫我們的函式,所以只是註冊一個function.這個function要有很明確的描素

**英文**
- 自訂function的參數和傳出值要描素清楚
- 建立模型時的tools引數值
- enable_automatic_function_calling=True,此設定會由model決定是否執行function

```python
import os
import google.generativeai as genai

def set_light_value(brightness:int, color_temp:str):
    """Set the brightness and color temperature of a room light. (mock API).

    Args:
        brightness: Light level from 0 to 100. Zero is off and 100 is full brightness
        color_temp: Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.

    Returns:
        A dictionary containing the set brightness and color temperature.
    """
    return {
        "brightness":brightness,
        "colorTemperature":color_temp
    }

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[set_light_value]
    )
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message('Dim the lights so the room feels cozy and warm.')
response.text
```

**中文版**

```python
import os
import google.generativeai as genai

def set_light_value(brightness:int, color_temp:str)->str:
    """設定房間的光線亮度和光線溫度 (模擬的API).

    Parameters:
        brightness: 亮度的等級從0~100,如果為0代表關閉光線,如果為100代表光線全開
        color_temp: 代表光線的溫度,有3個等線 `正常光線`, `冷光線` or `溫暖光線`.

    Returns:
        一個詞典物件設定光線高度和光線溫度.
    """
    print(brightness)
    print(color_temp)
    return {
        "brightness":brightness,
        "colorTemperature":color_temp
    }

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=[set_light_value]
    )
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message('開啟光線至50和設定為正常')
response.text
```










