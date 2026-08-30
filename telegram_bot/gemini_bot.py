"""
Telegram + Gemini 3.7 Flash AI 智慧對話機器人
使用 python-telegram-bot 與 Google GenAI SDK (Interactions API)
"""

import os
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 載入環境變數
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化 Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎訊息"""
    welcome_text = (
        "👋 你好！我是串接 Google 最新 Gemini 3.7 Flash 的 Telegram AI 助理。\n\n"
        "你可以直接向我提問任何問題、請我寫程式、翻譯或總結文章！"
    )
    if update.message:
        await update.message.reply_text(welcome_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """接收訊息並調用 Gemini API 生成回覆"""
    if not update.message or not update.message.text:
        return

    user_query = update.message.text
    chat_id = update.effective_chat.id

    # 傳送正在輸入狀態
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # 使用 Interactions API 呼叫 Gemini 3.7 Flash
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=user_query,
            system_instruction="你是一個繁體中文的 Telegram 智慧助理，請用繁體中文給出清晰、條理分明的回答。"
        )

        reply_text = interaction.output_text or "抱歉，目前無法生成回應。"
        await update.message.reply_text(reply_text)

    except Exception as e:
        error_msg = f"發生錯誤：{str(e)}"
        await update.message.reply_text(error_msg)


def main():
    if not TELEGRAM_TOKEN:
        print("❌ 錯誤：請先在 .env 中設定 TELEGRAM_BOT_TOKEN")
        return
    if not GEMINI_API_KEY:
        print("❌ 錯誤：請先在 .env 中設定 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Gemini Telegram Bot 運行中 (Polling 模式)... 按 Ctrl+C 結束")
    app.run_polling()


if __name__ == "__main__":
    main()
