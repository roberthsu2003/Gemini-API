"""
app_telegram_bot.py
實務應用整合：Telegram Python 運算解題機器人
功能：接收數學計算、字串處理或演算法問題，在沙盒中執行 Python 程式碼並回傳精確解答歷程
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
        "🧮 **歡迎使用 Gemini Python 程式運算機器人**！\n\n"
        "你可以向我提問任何數學計算、質數計算、日期換算或演算法問題，我會在 Python 沙盒中精確運算並解答！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def math_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    query = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=query + "\n（請使用 Python 程式碼演算，並使用繁體中文解釋）",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution())],
            ),
        )

        reply_text = response.text or "運算完成（無文字回覆）"
        await update.message.reply_text(reply_text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ 運算失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, math_calc))

    print("🚀 Telegram 程式碼運算機器人運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
