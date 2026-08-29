import io
import os
from dotenv import load_dotenv
from google import genai
import httpx

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 論文或遠端 PDF 網址
paper_url = "https://arxiv.org/pdf/2312.11805"
print(f"正在從遠端下載 PDF: {paper_url} ...")

pdf_content = httpx.get(paper_url, follow_redirects=True).content
doc_io = io.BytesIO(pdf_content)

# 上傳至 Files API
uploaded_paper = client.files.upload(
    file=doc_io,
    config={"mime_type": "application/pdf"},
)
print(f"論文已上傳至 Files API (URI: {uploaded_paper.uri})")

prompt = """
請閱讀這篇 Gemini 論文，針對以下三點提供繁體中文的深入分析：
1. 核心模型架構與多模態設計理念
2. 在 MMLU 等主流基準測試上的關鍵表現
3. 未來的應用展望
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

print("\n=== 遠端論文研讀分析結果 ===")
print(interaction.output_text)
