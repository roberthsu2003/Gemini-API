# 文件理解 (Document Understanding)

Gemini 模型原生支援 **PDF 文件深度理解**，利用原生多模態視覺能力解析整個文件上下文。這遠超越傳統的純文字 OCR 辨識，使模型能夠：

- 📊 **圖文混排與視覺解析**：理解文件中的排版佈局、複雜表格、曲線圖、流程圖、建築工程圖與手繪草圖，最高支援高達 **1,000 頁** 或 **50MB** 的長篇文件。
- 📑 **結構化資料萃取**：將掃描件、發票、合約與規格書內容直接轉換為符合 **JSON Schema**（如 Pydantic BaseModel）的結構化資料。
- 🔍 **跨頁長文問答與摘要**：基於整份文件的文字與視覺圖表進行多輪深度問答。
- 📝 **精確版面轉錄**：將文件內容轉錄為保有排版結構的 HTML、Markdown 或 LaTeX 格式。

---

## Gemini 3 世代處理與計費重大更新

1. **原生內嵌文字免費提取 (Native Text Inclusion)**：
   - PDF 檔案中內嵌的純文字會被直接提取並傳給模型，且**完全不計入 Token 費用**。
2. **視覺頁面以 IMAGE 模態計算**：
   - PDF 頁面影像以每頁約 **258 tokens** 計費，並在 `usage_metadata` 中歸類於 `IMAGE` 模態。
3. **支援多模態解析度控制 (`media_resolution`)**：
   - 可在請求中針對個別文件設定 `low`、`medium` 或 `high`，彈性平衡視覺細節與 Token 消耗。

---

## 1. 快速開始：Inline 傳入 PDF 數據 (Passing PDF Data Inline)

適合小型文件（或臨時單次處理），直接將 PDF 以 Base64 編碼內嵌於請求中。

### Python (Interactions API 推薦寫法)

```python
import base64
from google import genai

client = genai.Client()

with open("說明書.pdf", "rb") as f:
    pdf_bytes = f.read()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_bytes).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {"type": "text", "text": "請簡要總結這份文件的重點，並列出三大安全注意事項。"},
    ],
)

print(interaction.output_text)
```

### Python (GenerateContent API 對照寫法)

```python
from google import genai
from google.genai import types

client = genai.Client()

with open("說明書.pdf", "rb") as f:
    pdf_bytes = f.read()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "請總結這份文件的重點",
    ],
)
print(response.text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：PDF 即時摘要與問答介面</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「PDF 讀取與總結」程式碼改寫為 Gradio 應用：
1. 介面提供 gr.File(file_types=['.pdf']) 讓使用者上傳本地 PDF。
2. 提供提問輸入框（預設提示為「請條列摘要本文重點」）。
3. 讀取 PDF bytes 並調用 Gemini 3.7 Flash 進行多模態視覺理解。
4. 輸出區以 gr.Markdown 呈現結構化總結。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 使用 st.file_uploader 上傳 PDF 檔案。
2. 上傳完成後，顯示檔案名稱與大小，並提供提問文字輸入框。
3. 點擊「開始分析」按鈕後，以 st.spinner 提示載入，最後以 st.markdown 呈現排版結果。
```
</details>

---

## 2. 透過 Files API 上傳大型 PDF (Files API Upload)

對於較大檔案（超過 20MB）或需要在**多輪對話中重複引用**的文件，建議使用 **Files API**。它能將檔案上傳與模型推論解耦，節省網路頻寬並加速後續推論反應。

> [!NOTE]
> Files API 在支援 Gemini API 的所有地區均**免費提供**，上傳的檔案會在 Google 伺服器暫存 **48 小時**。

```python
import time
from google import genai

client = genai.Client()

# 1. 上傳大型 PDF
uploaded_file = client.files.upload(file="說明書.pdf")
print(f"檔案上傳成功: {uploaded_file.name} (URI: {uploaded_file.uri})")

# 2. 等待檔案處理完成
file_info = client.files.get(name=uploaded_file.name)
while file_info.state == "PROCESSING":
    time.sleep(2)
    file_info = client.files.get(name=uploaded_file.name)

# 3. 第一輪對話提問
interaction1 = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "uri": uploaded_file.uri,
            "mime_type": uploaded_file.mime_type,
        },
        {"type": "text", "text": "這台機器的濾網該如何拆卸與清洗？"},
    ],
)
print("Turn 1 回覆:\n", interaction1.output_text)

# 4. 第二輪追問（伺服器端維持上下文）
interaction2 = client.interactions.create(
    model="gemini-3.7-flash",
    previous_interaction_id=interaction1.id,
    input="清洗後需要多久時間晾乾？如何裝回？",
)
print("\nTurn 2 追問回覆:\n", interaction2.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：大型 PDF 智慧分析與多輪對話助手</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述使用 Files API 的 PDF 程式改寫為 Gradio 多輪對話應用：
1. 側邊欄提供檔案上傳區，上傳完成後呼叫 client.files.upload 並顯示上傳成功狀態。
2. 主畫面提供 gr.ChatInterface 對話框，讓使用者針對已上傳的 PDF 進行多輪深入提問。
3. 每次對話自動帶入 previous_interaction_id 維護上下文。
```

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述程式改寫為 Streamlit 應用：
1. 在側邊欄上傳 PDF，上傳後存入 client.files.upload 並將 URI 存入 st.session_state。
2. 主畫面使用 st.chat_message 建立多輪對話問答介面。
3. 支援快速切換預設常見問題按鈕。
```
</details>

---

## 3. 透過 URL 遠端載入長篇 PDF 論文 (Remote PDFs from URLs)

直接從網路上下載 arXiv 或其他學術論文的 PDF，並交由 Gemini 進行深入研讀分析。

```python
import io
import httpx
from google import genai

client = genai.Client()

paper_url = "https://arxiv.org/pdf/2312.11805"
pdf_content = httpx.get(paper_url, follow_redirects=True).content

uploaded_paper = client.files.upload(
    file=io.BytesIO(pdf_content),
    config={"mime_type": "application/pdf"},
)

prompt = """
請閱讀這篇 Gemini 技術報告論文，針對以下三點提供繁體中文深入分析：
1. 核心模型架構設計
2. 各項基準測試 (MMLU, GSM8K 等) 的亮點表現
3. 總結其對多模態 AI 的主要貢獻
"""

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "uri": uploaded_paper.uri,
            "mime_type": uploaded_paper.mime_type,
        },
        {"type": "text", "text": prompt},
    ],
)
print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：學術論文與線上 PDF 研讀助理</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述「遠端 PDF 論文分析」改寫為 Gradio 論文研讀助手：
1. 介面提供 URL 輸入框（支援直接貼上 arXiv PDF 連結）。
2. 提供下拉選單選擇分析模式（「論文快速摘要」、「方法論剖析」、「實驗結果評估」、「關鍵公式解讀」）。
3. 點擊按鈕後自動下載、上傳並產生繁體中文分析報告。
```
</details>

---

## 4. 跨多份 PDF 綜合比對與表格輸出 (Passing Multiple PDFs)

Gemini 支援在單一請求中傳入**多份 PDF 文件**（總頁數最高 1000 頁），並進行跨文件交叉比對。

```python
import base64
from google import genai

client = genai.Client()

with open("說明書.pdf", "rb") as f:
    pdf_bytes = f.read()

prompt = """
請比對這份說明書中的「安全操作規範」與「日常保養清潔」兩個章節：
1. 彙整各自的主要風險與防範措施。
2. 以一張清楚的 Markdown 表格輸出比較。
"""

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_bytes).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {"type": "text", "text": prompt},
    ],
)
print(interaction.output_text)
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：多文件智慧比對與差異分析看板</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將多文件比對程式改寫為 Streamlit 應用：
1. 支援同時上傳 2~3 份 PDF 文件（例如兩份合約版本或兩篇競品規格書）。
2. 呼叫 Gemini 3.7 Flash 進行深度差異分析。
3. 介面以 st.table 呈現關鍵條款對照表，並以 st.warning 標記高風險差異項。
```
</details>

---

## 5. PDF 結構化資訊萃取 (Structured Outputs with PDFs)

結合 **Pydantic BaseModel** 與 `response_format`，模型能直接從 PDF 掃描檔或規格書中提取型別安全的結構化 JSON 資料。

```python
import base64
from typing import List, Optional
from google import genai
from pydantic import BaseModel, Field

class ProductSpec(BaseModel):
    product_name: str = Field(description="產品名稱與品牌型號")
    category: str = Field(description="產品類別，例如：壁掛式空調機")
    safety_warnings: List[str] = Field(description="重要安全警告清單")
    maintenance_tips: List[str] = Field(description="定期保養與清潔要點")
    customer_support_phone: Optional[str] = Field(description="客戶服務或維修聯絡電話")

client = genai.Client()

with open("說明書.pdf", "rb") as f:
    pdf_bytes = f.read()

prompt = "請詳細閱讀這份說明書 PDF，將關鍵產品資訊、安全注意事項與維護重點提取為結構化資料。"

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "document",
            "data": base64.b64encode(pdf_bytes).decode("utf-8"),
            "mime_type": "application/pdf",
        },
        {"type": "text", "text": prompt},
    ],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": ProductSpec.model_json_schema(),
    },
)

spec = ProductSpec.model_validate_json(interaction.output_text)
print(spec.model_dump_json(indent=2))
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：發票與合約欄位自動萃取系統</b></summary>

**Gradio 介面開發 Prompt：**
```text
請幫我將上述 PDF 結構化擷取程式改寫為 Gradio 應用：
1. 介面提供 PDF 上傳框。
2. 呼叫 Gemini 進行 Pydantic Schema 結構化提取。
3. 介面左側展示 PDF 預覽，右側以 gr.JSON 與 gr.Dataframe 呈現提取出的結構化欄位。
```
</details>

---

## 6. Context Caching 內容快取加速 (Context Caching with Documents)

對於**超長文件（如數百頁手冊）**或**需要頻繁查詢的大型文件**，啟用 **Context Caching** 可以將文件預先快取在伺服器端，不僅推論速度大幅加快，還可**省下高達 75% 的 Token 費用**。

```python
from google import genai
from google.genai import types

client = genai.Client()

uploaded_doc = client.files.upload(file="說明書.pdf")

# 建立快取 (TTL 設定為 1 小時)
cache = client.caches.create(
    model="gemini-3.7-flash",
    config=types.CreateCachedContentConfig(
        system_instruction="你是一位專業的家電工程顧問與說明書專家。",
        contents=[uploaded_doc],
        ttl="3600s",
    ),
)

print(f"快取建立成功: {cache.name}")

# 使用快取進行快速低成本查詢
response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="這台機器在什麼情況下必須立即停止運轉並拔掉電源？",
    config=types.GenerateContentConfig(cached_content=cache.name),
)

print(response.text)
if response.usage_metadata:
    print(f"快取命中 Token 數: {response.usage_metadata.cached_content_token_count}")
```

<details>
<summary>🤖 <b>AI 賦能提示詞 (Prompts)：超長文件 Context Caching 深度研讀儀表板</b></summary>

**Streamlit 介面開發 Prompt：**
```text
請幫我將上述 Context Caching 程式改寫為 Streamlit 應用：
1. 側邊欄提供 PDF 上傳並一鍵建立 Context Cache。
2. 顯示快取過期倒數計時與已省下的 Token 數量 (st.metric)。
3. 主畫面以聊天室形式快速回應使用者的各種深入問題。
```
</details>

---

## 7. 技術規格與最佳實踐 (Technical Details & Best Practices)

### 技術規格與限制
- **檔案大小與頁數**：單一 PDF 最大支援 **50MB** 或 **1,000 頁**。
- **Token 計算**：每一頁 PDF 約換算為 **258 tokens**（視覺模態）。
- **解析度自動縮放**：頁面會自動等比例縮放至 768×768 到 3072×3072 像素之間。

### 最佳實踐 (Best Practices)
1. **校正旋轉方向**：上傳前確保頁面方向為正向（未倒置或傾斜 90 度）。
2. **避免模糊影像**：掃描文件請維持適當解析度，確保細小文字清晰可辨。
3. **提示詞順序**：在輸入陣列中，**將文字提示放在 Document 之後**，能達到最佳的視覺關聯效果。
