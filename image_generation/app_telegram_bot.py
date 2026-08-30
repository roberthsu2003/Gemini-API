"""
app_telegram_bot.py
實務應用整合：Telegram AI 算圖機器人
功能：接收用戶描述文字（或 /draw 指令），呼叫 Imagen 3 生成圖片並直接在 Telegram 回傳圖檔
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🎨 **歡迎使用 Gemini / Imagen 3 算圖機器人**！\n\n"
        "請直接傳送你想要生成的畫面描述（例如：`一隻穿著西裝在海邊看夕陽的柴犬`），我會立即為你繪製！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def generate_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    prompt = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)

    try:
        # 呼叫 Imagen 3
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png",
            ),
        )

        for gen_image in response.generated_images:
            photo_stream = io.BytesIO(gen_image.image.image_bytes)
            photo_stream.name = "generated_image.png"
            await update.message.reply_photo(photo=photo_stream, caption=f"✨ 產圖完成：{prompt}")

    except Exception as e:
        await update.message.reply_text(f"❌ 產圖失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請先在 .env 中設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image_handler))

    print("🚀 Telegram 算圖機器人運行中 (Polling 模式)...")
    app.run_polling()


if __name__ == "__main__":
    main()
