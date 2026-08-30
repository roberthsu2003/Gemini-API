"""
app_telegram_bot.py
實務應用整合：Telegram 智慧對話機器人
整合 python-telegram-bot (v20+) 與 Google Interactions API
功能：
1. /start 歡迎指令
2. 接收文字問題並呼叫 Gemini 3.7 Flash 回覆
3. 接收照片並自動進行多模態圖文視覺分析
"""

import io
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化 Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """歡迎指令"""
    msg = (
        "🤖 **歡迎使用 Gemini 智慧助理機器人**！\n\n"
        "你可以：\n"
        "• 傳送任何問題給我（支援程式碼、翻譯、解題）\n"
        "• 直接傳送一張圖片並加上文字說明，我會幫你分析！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理文字訊息"""
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_text = update.message.text

    # 顯示打字中狀態
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=user_text,
            system_instruction="你是一位專業、友善的繁體中文 Telegram 智慧助理。"
        )
        reply = interaction.output_text or "（無文字回應）"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ 發生錯誤：{str(e)}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理圖片與多模態分析"""
    if not update.message or not update.message.photo:
        return

    chat_id = update.effective_chat.id
    caption = update.message.caption or "請詳細描述這張圖片的內容與特色，以繁體中文回答。"

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # 下載最高解析度照片
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(photo_bytes))

        # 呼叫 Gemini 多模態分析
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=[caption, image]
        )
        reply = interaction.output_text or "（無分析結果）"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ 圖片分析錯誤：{str(e)}")


def main():
    if not TELEGRAM_TOKEN:
        print("❌ 請先在專案根目錄 .env 中設定 TELEGRAM_BOT_TOKEN")
        return
    if not GEMINI_API_KEY:
        print("❌ 請先在專案根目錄 .env 中設定 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Telegram Bot 啟動成功 (Polling 模式)... 按 Ctrl+C 停止")
    app.run_polling()


if __name__ == "__main__":
    main()
