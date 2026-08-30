"""
app_telegram_bot.py
實務應用整合：Telegram 智慧助理與函式呼叫機器人
功能：接收自然語言指令，自動調用天氣查詢與會議預約函式並回應用戶
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


def get_weather(city: str) -> dict:
    """查詢即時天氣。"""
    return {"city": city, "temperature": "26°C", "condition": "晴朗溫暖", "tip": "適合戶外活動"}


def schedule_reminder(title: str, time_str: str) -> dict:
    """設定定時提醒。"""
    return {"status": "success", "reminder": title, "scheduled_time": time_str}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **歡迎使用 Gemini 函式呼叫智慧管家**！\n\n"
        "你可以用自然語言跟我說：\n"
        "• `請問高雄現在天氣如何？`\n"
        "• `幫我設定下午三點提醒喝水`"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_text + "\n（請使用繁體中文親切回答）",
            config=types.GenerateContentConfig(
                tools=[get_weather, schedule_reminder],
            ),
        )
        reply = response.text or "已為您處理完成！"
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"❌ 執行失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_action))

    print("🚀 Telegram Function Calling 機器人運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
