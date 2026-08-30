"""
app_telegram_bot.py
實務應用整合：Telegram PDF 文件智能問答機器人
功能：接收用戶上傳的 PDF 文件，自動進行研讀，並支援後續對話提問
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# 儲存每個聊天室最新上傳的 PDF bytes
user_pdf_map = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📄 **歡迎使用 Gemini PDF 智能研讀機器人**！\n\n"
        "1. 請傳送一份 PDF 文件給我（如說明書、報告、論文）\n"
        "2. 文件接收後，您可以直接提問任何問題！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.document:
        return

    doc = update.message.document
    chat_id = update.effective_chat.id

    if not doc.file_name.lower().endswith(".pdf"):
        await update.message.reply_text("⚠️ 目前僅支援 PDF 文件格式！")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await update.message.reply_text(f"📥 正在下載並解析 `{doc.file_name}`，請稍候...", parse_mode="Markdown")

    try:
        tg_file = await doc.get_file()
        pdf_bytes = await tg_file.download_as_bytearray()
        user_pdf_map[chat_id] = bytes(pdf_bytes)

        # 進行初始摘要
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                types.Part.from_bytes(data=user_pdf_map[chat_id], mime_type="application/pdf"),
                "請用繁體中文以三點簡短說明這份 PDF 文件的主要主題與核心大綱。"
            ]
        )
        await update.message.reply_text(f"✅ 文件解析完成！\n\n**核心大綱：**\n{interaction.output_text}\n\n💡 您現在可以直接發送訊息提問！")
    except Exception as e:
        await update.message.reply_text(f"❌ 解析失敗：{str(e)}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    query = update.message.text

    if chat_id not in user_pdf_map:
        await update.message.reply_text("💡 請先傳送一份 PDF 文件給我，我才能為您解答文件相關問題喔！")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[
                types.Part.from_bytes(data=user_pdf_map[chat_id], mime_type="application/pdf"),
                f"請依據文件內容回答問題：{query}\n（請一律使用繁體中文，若文件未提及請誠實說明）"
            ]
        )
        await update.message.reply_text(interaction.output_text or "（無文字回應）")
    except Exception as e:
        await update.message.reply_text(f"❌ 查詢失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Telegram PDF 研讀機器人運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
