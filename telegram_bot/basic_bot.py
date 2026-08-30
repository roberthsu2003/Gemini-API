"""
Telegram 基礎機器人範例
使用 python-telegram-bot v20+ (非同步 async/await)
功能：處理 /start 指令與 Echo 文字回應
"""

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# 載入環境變數
load_dotenv()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")


# 處理 /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """當使用者發送 /start 時觸發"""
    if update.message:
        await update.message.reply_text("你好！我是你的 Telegram 機器人。請隨意傳送文字訊息給我！")


# 回應一般文字訊息（Echo）
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """將使用者發送的文字原樣回傳"""
    if update.message and update.message.text:
        user_text = update.message.text
        await update.message.reply_text(f"你說了：{user_text}")


def main():
    if TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("請先在 .env 中設定 TELEGRAM_BOT_TOKEN 或修改程式碼中的 TOKEN！")
        return

    # 建立 Telegram 應用程式
    app = ApplicationBuilder().token(TOKEN).build()

    # 註冊指令與訊息處理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Telegram Bot 運行中 (Polling 模式)... 按 Ctrl+C 結束")
    app.run_polling()


if __name__ == "__main__":
    main()
