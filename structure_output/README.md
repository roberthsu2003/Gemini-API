# 產生結構化的資料

Gemini 預設產生非結構化文本，但某些應用程式需要結構化文字。對於這些用例，您可以限制 Gemini 使用 JSON（一種適合自動處理的結構化資料格式）進行回應。您也可以限制模型符合列舉中指定的選項之一進行回應。

- 從報紙文章中提取公司訊息，建立公司資料庫。
- 從簡歷中提取標準化訊息
- 從食譜中提取原料並顯示每種原料的雜貨網站連結。

在您的提示中，您可以要求 Gemini 產生 JSON 格式的輸出，但請注意，該模型並不保證一定會產生 JSON 且只產生 JSON。為了獲得更確定的回應，您可以在回應 Schema 欄位中傳遞特定的 JSON 模式，以便 Gemini 始終以預期的結構進行回應。

本指南向您展示如何透過您選擇的 SDK 使用 generateContent 方法或直接使用 REST API 產生 JSON。這些範例展示了純文字輸入，但 Gemini 還可以對包含圖像、視訊和音訊的多模式請求產生 JSON 回應。


## 產生json格式
當模型配置為輸出 JSON 時，它會以 JSON 格式的輸出回應任何提示。您可以透過提供模式來控制 JSON 回應的結構。有兩種方法可以為模型提供架構：

- 使用文字敘述的提示
- 使用json格式的文字化圖例

這兩種方法都適用於 Gemini 1.5 Flash 和 Gemini 1.5 Pro。

### prompt中提供json文字的描素

- **使用英文**

```
import google.generativeai as genai
import os
import json
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash-exp')
prompt = """List a few popular cookie recipes in JSON format.

Use this JSON schema:

Recipe = {'recipe_name':str, 'ingredients':list[str]}
Return: list[Recipe]"""

result = model.generate_content(prompt)
json_str:str = result.text.replace('```json','') #去除最前面的一行
json_str = json_str.replace('```','') #去除最後面的一行
json_structure:list[dict] = json.loads(json_str) #轉換成資料結構
json_structure
```

- **使用中文**

```
import google.generativeai as genai
import os
import json
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash-exp')
prompt = """最常見的5種中式料理食譜,請條列式的方法列出食材,並使用json的格式輸出

Use this JSON schema:

Recipe = {'recipe_name':str, 'ingredients':list[str]}
Return: list[Recipe]"""

result = model.generate_content(prompt)
json_str:str = result.text.replace('```json','') #去除最前面的一行
json_str = json_str.replace('```','') #去除最後面的一行
json_structure:list[dict] = json.loads(json_str) #轉換成資料結構
json_structure
```

### 提供json schema給model配置(比較精準)

**英文**

```
import google.generativeai as genai
import typing_extensions as typing
import os
import json

class Recipe(typing.TypedDict):
    recipe_name:str
    ingredients:list[str]

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')
result = model.generate_content(
    'List a few popular cookie recipes.',
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[Recipe]
    )
)
json_structure = json.loads(result.text)
json_structure
```

**中文**

```python
import google.generativeai as genai
import typing_extensions as typing
import os
import json

class Recipe(typing.TypedDict):
    recipe_name:str
    ingredients:list[str]

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')
result = model.generate_content(
    '最常見的5種中式料理食譜,請條列式的方法列出食材和食材的份量,並使用json的格式輸出,請使用繁體中文',
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[Recipe]
    )
)
json_structure = json.loads(result.text)
json_structure
```

### 使用列舉(enum)限定結果輸出

在某些情況下，您可能希望模型從選項清單中選擇選項。為了實現此行為，您可以在配置設定中傳遞一個列舉。您可以在 response_schema 中任何地方使用列舉,列舉實際上是字串清單。

```python
import google.generativeai as genai
import enum
import os



class Choice(enum.Enum):
    PERCUSSION = "Percussion"
    STRING = "String"
    WOODWIND = "Woodwind"
    BRASS = "Brass"
    KEYBOARD = "Keyboard"

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-2.0-flash-exp")
organ = genai.upload_file('organ.jpg')
result = model.generate_content(
    ['What kind of instrument is this:',organ],
    generation_config=genai.GenerationConfig(
        response_mime_type="text/x.enum",
        response_schema=Choice
    )
)
print(result.text)

```

### 使用dict代替例舉

```
import google.generativeai as genai
import enum
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel("gemini-2.0-flash-exp")
organ = genai.upload_file('organ.jpg')
result = model.generate_content(
    ['What kind of instrument is this:',organ],
    generation_config=genai.GenerationConfig(
        response_mime_type="text/x.enum",
        response_schema={
            'type': 'STRING',
            'enum':["Percussion", "String", "Woodwind", "Brass", "Keyboard"]
        }
    )
)
print(result.text)

```

### 整合json schema 和 enum的應用

```
import google.generativeai as genai
from typing_extensions import TypedDict
import enum

class Grade(enum.Enum):
    A_PLUS = "a+"
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    F = "f"

class Recipe(TypedDict):
    recipe_name:str
    grade:Grade

model = genai.GenerativeModel("gemini-2.0-flash-exp")
result = model.generate_content(
    "List about 10 cookie recipes, grade them based on popularity",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[Recipe]
    )
)
print(result.text)
```







