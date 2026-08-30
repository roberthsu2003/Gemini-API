"""
app_telegram_bot.py
實務應用整合：Telegram 即時聯網查證新聞機器人
功能：接收用戶時事、股價、賽事提問，自主調用 Google Search 聯網搜尋並附帶引用來源回答
"""

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🌐 **歡迎使用 Gemini 即時聯網查證機器人**！\n\n"
        "你可以向我詢問任何最新時事、新聞、體育賽事比分或科技動態，我會立即聯網搜尋為您解答！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def search_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_query = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_query + "\n（請使用繁體中文回答）",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
            ),
        )

        reply_text = response.text or "查無結果"

        # 附帶引用來源
        if response.candidates and response.candidates[0].grounding_metadata:
            meta = response.candidates[0].grounding_metadata
            if meta.grounding_chunks:
                sources = []
                for chunk in meta.grounding_chunks[:3]:
                    if chunk.web:
                        sources.append(f"• [{chunk.web.title}]({chunk.web.uri})")
                if sources:
                    reply_text += "\n\n🔗 **參考來源：**\n" + "\n".join(sources)

        await update.message.reply_text(reply_text, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"❌ 搜尋出錯：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_query))

    print("🚀 Telegram 聯網搜尋機器人運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
