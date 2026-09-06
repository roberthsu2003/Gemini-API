"""
Telegram 主動推播訊息範例 (Broadcast / Push Notification)
支援目標：
1. 個人 (User ID - 正整數)
2. 群組 (Group Chat ID - 負整數)
3. 頻道 (Channel - @公開名稱 或 -100開頭的私密ID)
"""

import asyncio
import os
from dotenv import load_dotenv
from google import genai
from telegram import Bot

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ==============================================================================
# 推播目標設定 (可填寫單一目標或多個目標)
# ==============================================================================
# 1. 個人 (User ID)：正整數，對方必須曾私訊過 Bot (至少點過 /start)
USER_CHAT_ID = os.environ.get("TELEGRAM_USER_CHAT_ID", "123456789")

# 2. 群組 (Group ID)：負整數 (通常是 - 或 -100 開頭)，Bot 需先加入群組
GROUP_CHAT_ID = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "-1001234567890")

# 3. 頻道 (Channel)：
#    - 公開頻道：直接填寫頻道帳號 "@channel_username"
#    - 私密頻道：填寫以 -100 開頭的 Chat ID
#    - ⚠️ 注意：Bot 必須被加入頻道，並設為「管理員 (Admin)」具備發布訊息權限！
CHANNEL_CHAT_ID = os.environ.get("TELEGRAM_CHANNEL_CHAT_ID", "@your_channel_username")


async def broadcast_message(chat_id: str | int, text: str):
    """發送訊息至指定對象 (個人、群組或頻道)"""
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        msg = await bot.send_message(chat_id=chat_id, text=text)
        print(f"✅ 成功發送至 [{chat_id}] (Message ID: {msg.message_id})")
    except Exception as e:
        print(f"❌ 發送至 [{chat_id}] 失敗：{e}")


async def main():
    if not TELEGRAM_TOKEN:
        print("❌ 請先在 .env 設定 TELEGRAM_BOT_TOKEN")
        return

    # 推播內容（也可以串接 Gemini 生成）
    notification_text = "📢 大家好！這是來自機器人的全方位主動推播通知。"

    # 目標清單：可同時推播給個人、群組與頻道
    targets = [
        # USER_CHAT_ID,      # 個人
        # GROUP_CHAT_ID,     # 群組
        # CHANNEL_CHAT_ID,   # 頻道
    ]

    print("🚀 開始執行主動推播...")
    if not targets:
        print("💡 請在程式中取消註解 targets 清單，或替換為您真實的 Chat ID / 頻道名稱！")
        return

    for target in targets:
        await broadcast_message(target, notification_text)


if __name__ == "__main__":
    asyncio.run(main())
