"""
app_telegram_bot.py
實務應用整合：Telegram 食譜結構化提取機器人
功能：用戶隨意傳送菜餚名稱或凌亂文字，機器人自動提取為排版優雅的結構化食譜與食材清單
"""

import json
import os
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


class Ingredient(BaseModel):
    name: str = Field(description="食材名稱")
    quantity: str = Field(description="份量")


class Recipe(BaseModel):
    recipe_name: str = Field(description="食譜名稱")
    cooking_time_minutes: int = Field(description="預估時間（分鐘）")
    ingredients: List[Ingredient] = Field(description="食材列表")
    steps: List[str] = Field(description="步驟清單")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🍳 **歡迎使用 Gemini 結構化食譜小幫手**！\n\n"
        "請傳送一道菜餚名稱或一段包含食材做法的文字，我會為您提取結構化食譜！"
    )
    if update.message:
        await update.message.reply_text(msg, parse_mode="Markdown")


async def handle_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_input = update.message.text

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Recipe,
            )
        )
        data = json.loads(response.text)

        # 排版為美觀的 Markdown 回應
        reply = f"🍳 **【{data['recipe_name']}】**\n⏱️ 烹飪時間：約 {data['cooking_time_minutes']} 分鐘\n\n"
        reply += "🛒 **所需食材：**\n"
        for ing in data["ingredients"]:
            reply += f"• {ing['name']}：{ing['quantity']}\n"
        reply += "\n📝 **料理步驟：**\n"
        for i, step in enumerate(data["steps"], 1):
            reply += f"{i}. {step}\n"

        await update.message.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ 結構化提取失敗：{str(e)}")


def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("❌ 請在 .env 設定 TELEGRAM_BOT_TOKEN 與 GEMINI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_recipe))

    print("🚀 Telegram 結構化小幫手運行中...")
    app.run_polling()


if __name__ == "__main__":
    main()
