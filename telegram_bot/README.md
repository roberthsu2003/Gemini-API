# 📱 Telegram Bot 連線方式與機器人開發

使用 Python 開發 Telegram Bot 非常簡單且好寫，開發體驗比多數通訊軟體（如 LINE 或 Messenger）更輕量，原因在於：

- ⚡ **免伺服器與 Webhook 設定**：開發階段使用內建的 **Polling（輪詢）** 機制即可直接在本地端（本機電腦）運行，不需要公開 IP 或 ngrok 穿牆。
- ⏱️ **申請流程極快**：在 Telegram 搜尋 `@BotFather`，發送 `/newbot` 指令，30 秒內即可取得 API Token。
- 📦 **生態系成熟**：主流套件如 `python-telegram-bot`（支援非同步 `async`/`await`）與 `telebot`（`pyTelegramBotAPI`，語法極度精簡）封裝非常完善。

---

## 🔑 快速申請 Telegram Bot Token

1. 在 Telegram 搜尋官方機器人管理員 **[@BotFather](https://t.me/BotFather)**。
2. 發送 `/start`，接著點擊或輸入 `/newbot`。
3. 依序輸入機器人的 **顯示名稱 (Name)** 與 **唯一帳號 (Username)**（需以 `bot` 結尾，例如 `my_gemini_demo_bot`）。
4. 建立完成後，BotFather 會回傳專屬的 **HTTP API Token**（格式如 `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`）。
5. 將 Token 儲存於專案根目錄 `.env` 檔案中：
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 🛠️ 安裝套件

使用 `pip` 或 `uv` 安裝依賴：

```bash
# 使用 pip
pip install python-telegram-bot python-dotenv google-genai

# 或使用 uv
uv add python-telegram-bot python-dotenv google-genai
```

---

## 🚀 程式碼範例

### 範例 1：基礎連線與 Echo 文字回覆 (`basic_bot.py`)

接收 `/start` 招呼指令與回應用戶傳送的一般文字：

```python
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 處理 /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！我是你的 Telegram 機器人。")

# 回應一般文字訊息（Echo）
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"你說了：{user_text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot 運行中 (Polling 模式)...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

執行方式：
```bash
python telegram_bot/basic_bot.py
```

---

### 範例 2：串接 Gemini 3.7 Flash AI 對話助理 (`gemini_bot.py`)

結合 Google 官方推薦的 **Interactions API**，打造即時 AI 智慧客服/問答助理：

```python
import os
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 你好！我是串接 Gemini 3.7 Flash 的 Telegram AI 助理，請隨時向我提問！")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    # 顯示「輸入中」狀態
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # 呼叫 Gemini 3.7 Flash
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=update.message.text,
        system_instruction="你是一個繁體中文的 Telegram 智慧助理，請用繁體中文給出清晰、條理分明的回答。"
    )

    await update.message.reply_text(interaction.output_text or "抱歉，目前無法生成回應。")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Gemini Telegram Bot 運行中...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

執行方式：
```bash
python telegram_bot/gemini_bot.py
```

---

### 範例 3：加入群組 (Group) 的 AI 助理 (`gemini_group_bot.py`)

#### ⚠️ 群組前置設定：關閉 Group Privacy（必要步驟）
Telegram 預設會開啟 **Group Privacy（預設為 ON）**，這會限制 Bot 接收群組訊息，導致 `@機器人` 時沒有任何反應。因此加入群組前或加入後，**必須先將 Group Privacy 關閉 (Turn off)**：

1. 開啟 Telegram，私訊 **[@BotFather](https://t.me/BotFather)** 並輸入 `/mybots`。
2. 選擇你的機器人（例如 `@my_gemini_demo_bot`）。
3. 依序點擊：**Bot Settings** ➡️ **Group Privacy** ➡️ **Turn off**。
4. 看到 BotFather 回覆 `Privacy mode is disabled` 即代表成功關閉。
5. ⚠️ **注意**：若 Bot **已經加入群組**，修改設定後**必須先將 Bot 退出/踢出群組，再重新加入群組一次**，設定才會正式在群組中生效！

> 💡 **運作方式**：在程式端我們設定為 **「群友在訊息中 `@機器人` 或『回覆 (Reply)』機器人的訊息」** 時才觸發 Gemini，既能正常回覆，又避免在群聊日常時洗版。

```python
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
    bot_info = await context.bot.get_me()
    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text("👋 你好！直接發送訊息即可與我對話。")
    else:
        await update.message.reply_text(f"👋 大家好！在群組中請 @{bot_info.username} 或回覆我的訊息來提問。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    raw_text = update.message.text
    chat_type = update.effective_chat.type

    # 確保取得 Bot 的真實 Username (避免 context.bot.username 為 None)
    bot_info = await context.bot.get_me()
    bot_name = bot_info.username or ""

    is_private = chat_type == ChatType.PRIVATE
    is_mentioned = bool(bot_name and f"@{bot_name.lower()}" in raw_text.lower())
    is_reply_to_bot = bool(
        update.message.reply_to_message
        and update.message.reply_to_message.from_user
        and update.message.reply_to_message.from_user.id == bot_info.id
    )

    # 非私聊且沒有 @機器人 也沒有回覆機器人時，直接略過（避免洗版）
    if not is_private and not is_mentioned and not is_reply_to_bot:
        return

    # 去除 @BotUsername，留下純問題文字
    clean_text = raw_text.lower().replace(f"@{bot_name.lower()}", "").strip()
    if not clean_text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # 呼叫 Gemini 3.7 Flash
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=clean_text,
        system_instruction="你是一個 Telegram 群組 AI 助理，請用繁體中文給出簡潔有條理的回答。"
    )

    # 指定 reply_to_message_id 回覆該則訊息
    await update.message.reply_text(
        interaction.output_text or "抱歉，無法生成回應。",
        reply_to_message_id=update.message.message_id
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Gemini 群組 Telegram Bot 運行中...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

執行方式：
```bash
python telegram_bot/gemini_group_bot.py
```

> ⚠️ **群組中 `@bot` 沒反應的常見原因與解法**：
> 1. **程式端 `context.bot.username` 為 `None`**：在 `python-telegram-bot` v20+ 中，若未調用 `await context.bot.get_me()`，機器人帳號可能未載入導致判定失敗（本範例已修正此問題）。
> 2. **Telegram 隱私模式 (Group Privacy)**：
>    - **方法一（最推薦）**：在群組內直接把 Bot **設為管理員 (Admin)**，Bot 便能即時接收所有訊息與 @提及。
>    - **方法二**：私訊 `@BotFather` 輸入 `/mybots` ➡️ 選擇你的 Bot ➡️ **Bot Settings** ➡️ **Group Privacy** ➡️ 點選 **Turn off**。**注意：設定完成後，必須將 Bot 退出群組並重新拉進群組**，設定才會生效！

---

### 範例 4：Bot 主動推播訊息（支援個人、群組與頻道）(`send_group_message.py`)

主動推播不需要等待使用者先提問，適用於：**系統告警、定時通知、每日晨報、Gemini 自動推播**。

#### 📌 三種推播對象的前置條件與 ID 格式

| 推播對象 | 必備前置條件 | ID 格式範例 |
| :--- | :--- | :--- |
| **👤 個人 (User)** | 該用戶必須曾主動私訊過 Bot（至少點擊過一次 `/start`） | 正整數，如 `123456789` |
| **👥 群組 (Group)** | Bot 必須已加入該群組 | 負整數（通常帶有 `-100` 前綴），如 `-1001234567890` |
| **📢 頻道 (Channel)** | **必須將 Bot 設為該頻道的「管理員 (Admin)」**，且開啟發文權限 | 公開頻道填 `@channel_username`<br>私密頻道填負整數 ID（如 `-1009876543210`） |

> 🔍 **如何取得 Chat ID？**
> 1. 個人/群組/頻道發送任意訊息後，在瀏覽器打開：
>    `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
> 2. 在 JSON 內容中即可找到對應的 `"chat":{"id": ...}`。

---

#### 程式碼範例

使用 `telegram.Bot` 的 `send_message()`，傳入對應的 `chat_id` 即可發送給不同目標：

```python
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 設定不同推播目標
TARGET_USER_ID = 123456789                # 個人 (正整數，用戶需先私訊過 Bot)
TARGET_GROUP_ID = "-1001234567890"         # 群組 (負整數，Bot 需在群組內)
TARGET_CHANNEL = "@my_public_channel"      # 頻道 (公開填 @帳號，Bot 需為管理員)

async def send_broadcast(chat_id: str | int, message: str):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"✅ 成功發送至：{chat_id}")
    except Exception as e:
        print(f"❌ 發送至 {chat_id} 失敗：{e}")

async def main():
    text = "📢 大家好！這是來自 Telegram Bot 的跨平台主動推播通知。"

    # 可同時推送給多個目標
    targets = [
        # TARGET_USER_ID,
        # TARGET_GROUP_ID,
        # TARGET_CHANNEL,
    ]

    for chat_id in targets:
        await send_broadcast(chat_id, text)

if __name__ == "__main__":
    asyncio.run(main())
```

> 💡 **進階結合 Gemini 自動生成推播內容**：
> 先調用 Gemini 產生問候語或重點摘要，再呼叫 `await bot.send_message(chat_id=..., text=ai_text)`，即可打造全自動的 AI 晨報推播機器人！

執行方式：
```bash
python telegram_bot/send_group_message.py
```

---

## 💡 常見開發優勢與考量

### 優勢
- **多媒體與富文本**：支援 Markdown / HTML 格式排版、圖片、音訊、文件、語音、位置資訊。
- **豐富互動元件**：可輕鬆建立自訂鍵盤（Reply Keyboard）、訊息內嵌按鈕（Inline Keyboard）與回呼處理（Callback Query）。
- **完全免費與高限額**：官方 Bot API 免費使用且限制非常寬鬆，是個人推播通知、自動化監控與 LLM AI Agent 最理想的通道。

### 注意事項
- **本地開發 vs 生產部署**：
  - 本地測試推薦使用 **Polling 模式**（最簡單直接）。
  - 若需部署至雲端伺服器並承受高併發流量，可切換為 **Webhook 模式**（搭配 FastAPI、Flask 或 Cloud Functions 接收推送）。
