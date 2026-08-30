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

## 💡 常見開發優勢與考量

### 優勢
- **多媒體與富文本**：支援 Markdown / HTML 格式排版、圖片、音訊、文件、語音、位置資訊。
- **豐富互動元件**：可輕鬆建立自訂鍵盤（Reply Keyboard）、訊息內嵌按鈕（Inline Keyboard）與回呼處理（Callback Query）。
- **完全免費與高限額**：官方 Bot API 免費使用且限制非常寬鬆，是個人推播通知、自動化監控與 LLM AI Agent 最理想的通道。

### 注意事項
- **本地開發 vs 生產部署**：
  - 本地測試推薦使用 **Polling 模式**（最簡單直接）。
  - 若需部署至雲端伺服器並承受高併發流量，可切換為 **Webhook 模式**（搭配 FastAPI、Flask 或 Cloud Functions 接收推送）。
