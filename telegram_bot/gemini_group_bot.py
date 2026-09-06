"""
Telegram 群組 + 私聊 Gemini 3.7 Flash AI 助理
支援：
1. 私聊：直接發問即可回覆
2. 群組：被 @提及 (Mention) 或 被回覆 (Reply) 時才觸發回覆
"""

import os
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.constants import ChatAction, ChatType
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎訊息"""
    if update.effective_chat.type == ChatType.PRIVATE:
        text = "👋 你好！我是 Gemini AI 助理，直接傳訊息向我提問即可！"
    else:
        text = f"👋 大家好！在群組中請 @{context.bot.username} 或回覆我的訊息，我就會為大家解答！"
    await update.message.reply_text(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理私聊與群組訊息"""
    if not update.message or not update.message.text:
        return

    raw_text = update.message.text
    chat_type = update.effective_chat.type
    bot_username = context.bot.username

    is_private = chat_type == ChatType.PRIVATE
    is_mentioned = bot_username and f"@{bot_username.lower()}" in raw_text.lower()
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user
        and update.message.reply_to_message.from_user.id == context.bot.id
    )

    # 群組中若未被 @ 或未被回覆，則略過（避免洗版）
    if not is_private and not is_mentioned and not is_reply_to_bot:
        return

    # 去除訊息中的 @BotUsername 留下提問內容
    clean_text = raw_text.replace(f"@{bot_username}", "").strip()
    if not clean_text:
        await update.message.reply_text("請問有什麼我可以為您服務的？")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # 呼叫 Gemini 3.7 Flash
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=clean_text,
        system_instruction="你是一個繁體中文的 Telegram 群組智慧助理，請用繁體中文給出清晰、條理分明的回答。"
    )

    reply_text = interaction.output_text or "抱歉，目前無法生成回應。"
    await update.message.reply_text(reply_text, reply_to_message_id=update.message.message_id)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Gemini 群組 Telegram Bot 運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
