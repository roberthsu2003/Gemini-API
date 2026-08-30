"""
app_telegram_bot.py
實務應用整合：Telegram 企業知識庫 RAG 檢索機器人
功能：接收用戶提問，透過 Gemini Embedding 檢索知識庫並產出解答
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


KNOWLEDGE_BASE = [
    "退換貨政策：商品收訖後享有 7 天猶豫期，商品需維持全新完整包裝方可辦理退貨。",
    "保固條款：主機本體提供 1 年免費原廠保固，人為外力損壞或泡水不在保固範圍內。",
    "運費說明：全館單筆訂單滿 1,000 元即享免運費優惠，未滿則酌收 80 元物流運費。",
    "客服時間：週一至週五 09:00~18:00，國定假日與例假日暫停線上客服服務。"
]

doc_embeddings = []


def init_embeddings():
    global doc_embeddings
    if not GEMINI_API_KEY:
        return
    res = client.models.embed_content(
        model="gemini-embedding-001",
        contents=KNOWLEDGE_BASE,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    doc_embeddings = [np.array(e.values) for e in res.embeddings]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📚 **歡迎使用 Gemini 知識庫檢索機器人**！\n\n"
        "你可以向我詢問關於退換貨、保固、運費與客服時間等問題，我會透過語意向量檢索知識庫為您回答！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def search_qa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    query = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        q_res = client.models.embed_content(
            model="gemini-embedding-001",
            contents=query,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        q_emb = np.array(q_res.embeddings[0].values)

        scores = [cosine_similarity(q_emb, d_emb) for d_emb in doc_embeddings]
        best_idx = int(np.argmax(scores))

        reply = f"🎯 **檢索到的知識庫條目（相關度: {scores[best_idx]:.2f}）：**\n\n{KNOWLEDGE_BASE[best_idx]}"
        await update.message.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ 檢索失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    init_embeddings()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_qa))

    print("🚀 Telegram 知識庫檢索機器人運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
