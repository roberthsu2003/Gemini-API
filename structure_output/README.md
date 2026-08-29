# 產生結構化輸出 (Structured Outputs)

Gemini 預設會產生自然語言的非結構化文字，但在許多實際應用中（如自動化管線、資料庫寫入、API 串接、UI 動態渲染等），我們需要模型嚴格依照預定義的資料格式進行回應。

透過 **Structured Outputs（結構化輸出）**，您可以限制 Gemini 模型強制輸出符合 **JSON Schema** 的內容，確保輸出具備**型別安全 (Type-Safe)**、**結構確定**且**易於自動化解析**的特點。

---

## 核心應用場景

- **資料擷取 (Data Extraction)**：從新聞、合約或雜亂文章中擷取人名、日期、公司、金額等特定欄位。
- **結構化分類 (Classification)**：將內容分類至預先定義的類別或列舉 (Enum)，並回傳分類理由。
- **代理與工具工作流程 (Agentic Workflows)**：為下游的 Function Calling、資料庫或第三方 REST API 產生結構化參數。
- **階層與遞迴關係 (Hierarchical & Recursive Structures)**：萃取組織架構圖、心智圖、AST 語法樹等具備父子嵌套關係的資料。

---

## 支援的 SDK 與語法規範

目前 Google GenAI SDK 原生支援以下方式定義 Schema：
- **Python**：使用 [Pydantic](https://docs.pydantic.dev/latest/) (`BaseModel`, `Field`) 或原生 TypedDict / Enum。
- **JavaScript / TypeScript**：使用 [Zod](https://zod.dev/) 或標準 JSON Schema 物件。
- **REST API**：直接傳入 JSON Schema 定義。

> [!TIP]
> **API 呼叫方式說明**：
> - **Interactions API（推薦）**：透過 `client.interactions.create` 搭配 `response_format={"type": "text", "mime_type": "application/json", "schema": ...}`。
> - **GenerateContent API**：透過 `client.models.generate_content` 搭配 `config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=...)`。
> - 目前推薦模型：`gemini-3.7-flash` 或 `gemini-3.5-flash-lite`。

---

## 1. 快速開始：食譜資料擷取 (Recipe Extractor)

本範例示範如何從非結構化的食譜描述中，擷取並轉換為包含 `object`、`array`、`string`、`integer` 等型別的標準 JSON。

### Python (Interactions API 推薦寫法)

```python
from typing import List, Optional
from google import genai
from pydantic import BaseModel, Field

# 1. 定義資料結構模型
class Ingredient(BaseModel):
    name: str = Field(description="食材名稱")
    quantity: str = Field(description="食材份量與單位，例如：2 湯匙、100g")

class Recipe(BaseModel):
    recipe_name: str = Field(description="食譜名稱")
    prep_time_minutes: Optional[int] = Field(description="預估準備時間（分鐘）")
    ingredients: List[Ingredient] = Field(description="食材清單")
    instructions: List[str] = Field(description="料理步驟清單")

client = genai.Client()

prompt = """
請從以下文字中擷取美味巧克力豆餅乾的食譜：
這道巧克力豆餅乾需要中筋麵粉 2 又 1/4 杯、小蘇打粉 1 茶匙、鹽 1 茶匙、
軟化無鹽奶油 1 杯、細砂糖 3/4 杯、黑糖 3/4 杯、香草精 1 茶匙與 2 顆大雞蛋。
最後加入 2 杯半甜巧克力豆。
步驟：首先將烤箱預熱至 190°C (375°F)。在小碗中將麵粉、小蘇打和鹽混合均勻。
在另一個大碗中將奶油與兩種糖打發至蓬鬆。依序打入香草精與雞蛋。
分次拌入乾粉料，最後倒入巧克力豆。用湯匙舀至烤盤上，烘烤 9 至 11 分鐘。
預估準備時間約 15 分鐘。
"""

# 2. 呼叫 Interactions API
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Recipe.model_json_schema()
    },
)

# 3. 解析並轉為型別安全的 Pydantic 物件
recipe = Recipe.model_validate_json(interaction.output_text)
print(f"食譜名稱: {recipe.recipe_name}")
print(f"準備時間: {recipe.prep_time_minutes} 分鐘")
print("食材清單:")
for item in recipe.ingredients:
    print(f"  - {item.name}: {item.quantity}")
```

### Python (GenerateContent API 對照寫法)

```python
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class Recipe(BaseModel):
    recipe_name: str = Field(description="食譜名稱")
    ingredients: list[str] = Field(description="食材清單")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="請列出3道熱門的台灣夜市小吃食譜",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=list[Recipe],
    ),
)

# 直接透過 response.parsed 取得解析後的物件
recipes: list[Recipe] = response.parsed
for r in recipes:
    print(r.recipe_name, r.ingredients)
```

### JavaScript / TypeScript (Zod)

```typescript
import { GoogleGenAI } from "@google/genai";
import * as z from "zod";

const recipeJsonSchema = {
  type: "object",
  properties: {
    recipe_name: { type: "string", description: "食譜名稱" },
    prep_time_minutes: { type: "integer", description: "準備時間（分鐘）" },
    ingredients: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string", description: "食材名稱" },
          quantity: { type: "string", description: "份量" },
        },
        required: ["name", "quantity"],
      },
    },
    instructions: {
      type: "array",
      items: { type: "string" },
    },
  },
  required: ["recipe_name", "ingredients", "instructions"],
};

const recipeSchema = z.fromJSONSchema(recipeJsonSchema);
const client = new GoogleGenAI({});

const interaction = await client.interactions.create({
  model: "gemini-3.7-flash",
  input: "請擷取巧克力豆餅乾的食譜...",
  response_format: {
    type: "text",
    mime_type: "application/json",
    schema: recipeJsonSchema,
  },
});

const recipe = recipeSchema.parse(JSON.parse(interaction.output_text));
console.log(recipe);
```

### REST API

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -H "Api-Revision: 2026-05-20" \
    -d '{
      "model": "gemini-3.7-flash",
      "input": "請擷取巧克力豆餅乾的食譜...",
      "response_format": {
        "type": "text",
        "mime_type": "application/json",
        "schema": {
          "type": "object",
          "properties": {
            "recipe_name": { "type": "string" },
            "prep_time_minutes": { "type": "integer" },
            "ingredients": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "name": { "type": "string" },
                  "quantity": { "type": "string" }
                },
                "required": ["name", "quantity"]
              }
            },
            "instructions": {
              "type": "array",
              "items": { "type": "string" }
            }
          },
          "required": ["recipe_name", "ingredients", "instructions"]
        }
      }
    }'
```

---

## 2. 進階場景：條件結構與多態分類 (`anyOf` / `Union`)

在內容審查或分類情境中，輸出格式可能根據判定結果而有不同欄位。可使用 `Union` 或 `anyOf` 達成多態分支。

```python
from typing import Literal, Union
from google import genai
from pydantic import BaseModel, Field

class SpamDetails(BaseModel):
    reason: str = Field(description="判定為垃圾/釣魚內容的具體原因")
    spam_type: Literal["phishing", "scam", "unsolicited_promotion", "other"] = Field(
        description="垃圾訊息類型"
    )

class SafeDetails(BaseModel):
    summary: str = Field(description="安全內容的簡要摘要")
    is_safe: bool = Field(description="是否適合全年齡閱覽")

class ModerationResult(BaseModel):
    decision: Union[SpamDetails, SafeDetails] = Field(
        description="根據內容自動判斷為垃圾或正常安全訊息"
    )

client = genai.Client()

prompt = """
請審查以下訊息：
'恭喜！您已獲選為本年度幸運得主，可獲得免費郵輪旅遊！請立即點擊連結領獎：www.definitely-not-a-scam.com'
"""

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ModerationResult.model_json_schema(),
    },
)

result = ModerationResult.model_validate_json(interaction.output_text)
print(result.model_dump_json(indent=2))
```

---

## 3. 進階場景：遞迴樹狀結構 (Recursive Hierarchy)

Gemini 支援定義遞迴資料模型（例如組織架構樹、目錄樹或留言回覆串）：

```python
from typing import List
from google import genai
from pydantic import BaseModel, Field

class Employee(BaseModel):
    name: str = Field(description="員工姓名")
    employee_id: int = Field(description="員工編號")
    reports: List["Employee"] = Field(
        default_factory=list,
        description="向該員工直接匯報的下屬清單（遞迴結構）"
    )

client = genai.Client()

prompt = """
請根據以下描述建立團隊組織架構：
Alice (ID: 101) 是總監，底下管理 Bob (ID: 102) 與 Charlie (ID: 103)。
Bob 底下管理工程師 David (ID: 104)。
"""

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Employee.model_json_schema(),
    },
)

org_chart = Employee.model_validate_json(interaction.output_text)
print(org_chart.model_dump_json(indent=2))
```

---

## 4. 進階場景：結構化串流輸出 (Streaming)

若要在生成的同時逐步接收 JSON 數據，可啟用 `stream=True`。伺服器會串流傳送合法的 partial JSON 片段：

```python
from google import genai
from pydantic import BaseModel
from typing import Literal

class Feedback(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str

client = genai.Client()

stream = client.interactions.create(
    model="gemini-3.7-flash",
    input="請為最新一代的智慧手錶撰寫一段詳細的使用者評價。",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Feedback.model_json_schema(),
    },
    stream=True,
)

print("即時串流接收中: ", end="", flush=True)
for event in stream:
    if event.event_type == "step.delta" and event.delta.text:
        print(event.delta.text, end="", flush=True)
print()
```

---

## 5. 進階場景：結構化輸出結合內建工具 (With Tools)

Gemini 3 世代模型支援將結構化輸出與內建工具結合（例如 **Google Search 聯網搜尋**、**URL Context**、**Code Execution** 或 **Function Calling**）。模型會先透過工具獲取最新聯網資料，再將最終答案整理成指定的 JSON Schema：

```python
from google import genai
from pydantic import BaseModel, Field
from typing import List

class MatchResult(BaseModel):
    winner: str = Field(description="獲勝隊伍名稱")
    final_match_score: str = Field(description="最終比分")
    scorers: List[str] = Field(description="進球或得分球員名單")

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請搜尋最新一屆歐洲國家盃 (UEFA Euro) 決賽的完整戰報。",
    tools=[{"type": "google_search"}, {"type": "url_context"}],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": MatchResult.model_json_schema(),
    },
)

result = MatchResult.model_validate_json(interaction.output_text)
print(result)
```

---

## 6. 使用列舉 (Enum) 限制輸出選項

當只需要模型從固定清單中擇一回答時，可以使用 Enum 或 `text/x.enum`：

```python
import enum
from google import genai
from google.genai import types

class InstrumentType(enum.Enum):
    PERCUSSION = "Percussion"
    STRING = "String"
    WOODWIND = "Woodwind"
    BRASS = "Brass"
    KEYBOARD = "Keyboard"

client = genai.Client()
organ_image = client.files.upload(file="organ.jpg")

result = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=["請問這張圖片中的樂器屬於哪一種類型？", organ_image],
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum",
        response_schema=InstrumentType,
    ),
)
print(f"樂器分類結果: {result.text}")
```

---

## 7. 實戰範例：牌告匯率轉換與 Gradio / Streamlit 介面

本範例結合爬蟲資料與 Gemini 結構化輸出，動態分析支援的貨幣並提供即時換算功能。

```python
import os
import gradio as gr
from google import genai
from pydantic import BaseModel, Field

with open("2025_01_29.csv", encoding="utf-8") as file:
    csv_content = file.read()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

base_instruction = f"""
## 請依據以下的 CSV 表格內容回答問題：
{csv_content}
## 換算規則：
1. 台幣換外幣：金額 / 現金賣出匯率
2. 外幣換台幣：金額 * 現金買入匯率
"""

class CurrencyList(BaseModel):
    currencies: list[str] = Field(description="支援換算的幣別名稱清單")

# 透過結構化輸出取得幣別清單
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="請列出資料中所有可供換算的幣別清單，並加入「台幣」",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": CurrencyList.model_json_schema(),
    },
    system_instruction=base_instruction,
)

currency_data = CurrencyList.model_validate_json(interaction.output_text)
currencies = currency_data.currencies

with gr.Blocks(title="Gemini 牌告匯率換算") as demo:
    gr.Markdown("# 💱 智慧匯率換算助理")
    in_radio = gr.Radio(currencies, label="持有幣別", value="台幣")
    out_radio = gr.Radio(currencies, label="兌換幣別")
    number = gr.Number(value=1000, label="兌換金額")
    btn = gr.Button("開始計算", variant="primary")
    result_markdown = gr.Markdown()

    def calculate(num, curr_in, curr_out):
        if not curr_in or not curr_out:
            return "請選擇持有幣別與兌換幣別！"
        prompt = f"請將 {num} {curr_in} 轉換為 {curr_out}，並以 Markdown 詳細列出計算步驟。"
        res = client.interactions.create(
            model="gemini-3.7-flash",
            input=prompt,
            system_instruction=base_instruction,
        )
        return res.output_text

    btn.click(calculate, inputs=[number, in_radio, out_radio], outputs=result_markdown)

if __name__ == "__main__":
    demo.launch()
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：快速轉為 Streamlit 介面</b></summary>

```text
請幫我將上述 Gradio 匯率試算程式改寫為 Streamlit 應用程式：
1. 使用 st.selectbox 選擇持有幣別與兌換幣別。
2. 使用 st.number_input 輸入換算金額。
3. 點擊「計算」按鈕後，呼叫 Gemini 3.7 Flash 執行匯率試算，並以 st.success 與 st.markdown 呈現排版結果。
```
</details>

---

## 8. JSON Schema 支援規格詳細說明

Gemini 的結構化輸出支援 [JSON Schema](https://json-schema.org/) 的核心子集：

### 支援型別 (`type`)
- `string`：字串文字
- `number`：浮點數
- `integer`：整數
- `boolean`：布林值 (`true` / `false`)
- `object`：包含鍵值對的結構化物件
- `array`：清單陣列
- `null`：支援空值（例如 `{"type": ["string", "null"]}`）

### 描述與型別屬性
| 屬性 | 適用型別 | 說明 |
|---|---|---|
| `title` | 所有型別 | 屬性簡稱 |
| `description` | 所有型別 | 詳細屬性說明，**強烈建議撰寫**以提高模型精確度 |
| `properties` | `object` | 物件所包含的各欄位 Schema |
| `required` | `object` | 必填欄位清單 |
| `additionalProperties` | `object` | 是否允許額外未定義的鍵值 |
| `enum` | `string` / `number` | 列舉限定的合法取值清單 |
| `format` | `string` | 格式約束（如 `date-time`, `date`, `time` 等） |
| `minimum` / `maximum` | `number` / `integer` | 數值範圍限制 |
| `items` | `array` | 陣列元素的 Schema 定義 |
| `minItems` / `maxItems` | `array` | 陣列元素長度上下限 |

---

## 9. 結構化輸出 (Structured Outputs) vs 函式呼叫 (Function Calling)

| 特性 | Structured Outputs (結構化輸出) | Function Calling (函式呼叫) |
|---|---|---|
| **主要定位** | **格式化最終回答** | **對話中的即時動作與工具調度** |
| **使用時機** | 需要模型輸出固定格式（如 JSON、表格）供前端或資料庫存取時 | 模型需要呼叫外部 API/資料庫查詢資訊後再回答使用者時 |
| **執行流程** | 單次生成或串流直接返回 JSON 資料 | 產生 Function Call 請求 ➔ 客戶端執行並回傳 Function Result ➔ 模型產出最終解答 |

---

## 10. 最佳實踐 (Best Practices)

1. **詳盡的欄位說明 (`description`)**：在 Pydantic `Field(description=...)` 或 JSON Schema `description` 中提供清晰說明，能大幅提升提取準確度。
2. **優先使用強型別 (`Strong Typing`)**：使用 `integer`、`enum`、`Literal`、`bool` 而非一律使用 `string`。
3. **客戶端資料驗證**：模型輸出的 JSON 語法一定符合 Schema，但業務邏輯或數值合理性仍建議在應用層進行驗證（例如使用 `model_validate_json`）。
4. **控制 Schema 複雜度**：避免過於深層的巢狀結構，可適度拆分模型以維持最佳推理效能與回應速度。
