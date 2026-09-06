"""
Telegram 群組主動推播訊息範例 (Broadcast / Push Notification)
功能：無需等群友發話，由程式主動向指定群組發送推播訊息或 Gemini 生成的內容
"""

import asyncio
import os
from dotenv import load_dotenv
from google import genai
from telegram import Bot

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 請替換為您的群組 Chat ID (群組 ID 通常是負整數，例如 -1001234567890 或 -987654321)
# 可以在群組發送任何訊息後，執行本檔案的 get_recent_chat_ids() 查詢
GROUP_CHAT_ID = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "-1001234567890")


async def get_recent_chat_ids():
    """輔助工具：查詢 Bot 最近收到的群組與對話 ID"""
    bot = Bot(token=TELEGRAM_TOKEN)
    updates = await bot.get_updates()
    print("🔍 最近收到的對話清單：")
    for u in updates:
        if u.effective_chat:
            chat = u.effective_chat
            print(f"👉 類型: {chat.type:10} | ID: {chat.id:<15} | 名稱: {chat.title or chat.first_name}")


async def send_text_to_group(text: str):
    """主動發送文字訊息至群組"""
    bot = Bot(token=TELEGRAM_TOKEN)
    message = await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
    print(f"✅ 訊息已發送至群組 (Message ID: {message.message_id})")


async def send_gemini_daily_to_group():
    """主動讓 Gemini 生成內容（如每日問候、重點摘要）並推播至群組"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.interactions.create(
        model="gemini-3.7-flash",
        input="請給群組成員寫一段簡短、元氣滿滿的今日問候與一句科技勵志名言。",
        system_instruction="你是一個活潑親切的社群助理。"
    )

    ai_text = response.output_text or "早安大家！祝今天一切順利！"
    await send_text_to_group(f"📢 **AI 晨間推播**\n\n{ai_text}")


async def main():
    if not TELEGRAM_TOKEN:
        print("❌ 請先在 .env 設定 TELEGRAM_BOT_TOKEN")
        return

    # 若尚未知道群組 ID，可先執行此行查詢：
    # await get_recent_chat_ids()

    print("🚀 正在主動向群組發送訊息...")
    # 方式 1：發送自訂文字通知
    await send_text_to_group("📢 大家好！這是來自 Bot 的主動廣播通知。")

    # 方式 2：結合 Gemini 自動生成推播
    # if GEMINI_API_KEY:
    #     await send_gemini_daily_to_group()


if __name__ == "__main__":
    asyncio.run(main())
